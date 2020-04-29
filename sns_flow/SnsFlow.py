import numpy as np
import pandas as pd

from sns_flow.mysql_db.Connection import Connection

from sns_flow.helpers.dates import Dates
from sns_flow.helpers.dataset import Dataset

from sns_flow.model.rules.FotoRule import FotoRule
from sns_flow.model.rules.PromaxRule import PromaxRule
from sns_flow.model.rules.AlocacaoNormal import AlocacaoNormal
from sns_flow.model.rules.Rateio import Rateio
from sns_flow.model.rules.VoltaPerna import VoltaPerna


class SnsFlow:

    config = None

    def run(self, load_date: str, config: dict) -> pd.DataFrame:
        if 'connection' not in config:
            raise IndexError('Config should have the key "connection" with database connection info.')

        self.config = config
        # Setup db connection
        Connection.set_connection_dict(self.config['connection'])

        last7 = [str(dt) for dt in Dates.last7days(load_date)]
        # last7 = [load_date]

        append = pd.DataFrame()

        for dt in last7:
            print(f'========= RUNNING DATE -> {dt} =============')
            output = self.run_date(dt)
            append = pd.concat([output, append], sort=False)

        report = self.prepare_report(append)
        # report = append
        return report


    def run_date(self, load_date: str) -> pd.DataFrame:

        foto = Dataset.load('foto', load_date=load_date)
        promax = Dataset.load('promax', load_date=load_date)
        malha = Dataset.load('malha', load_date=load_date, limit=45)

        foto_rule = FotoRule()
        foto = foto_rule.process(foto)

        # FOTO + PROMAX
        union = self.unite(foto, promax)
        cols = union.columns.tolist()

        # Removendo demais dias
        union.query(f'dat_original == "{load_date}"', inplace=True)

        # print('=== UNION ===')
        # print(union.shape)
        # print(union.marcacao.sum(), union.ns_gross.sum())

        result, remnant = union, None

        # Configs
        alocacao_conf = self.config['rules']['alocacao_normal']
        rateio_conf = self.config['rules']['rateio']
        voltaperna_conf = self.config['rules']['volta_perna']

        # === ALOCACAO NORMAL RULE ===
        if alocacao_conf['on']:
            alocacao_rule = AlocacaoNormal()
            result, remnant = alocacao_rule.process(union, malha,
                                                    load_date=load_date,
                                                    num_semanas=alocacao_conf['semanas'])

        # print('=== ALOCACAO ===')
        # print(result.shape)
        # print(result.marcacao.sum(), result.ns_gross.sum())

        # === RATEIO RULE ===
        if rateio_conf['on']:
            rateio_rule = Rateio()
            # Caso tenha resto
            if not remnant.empty:
                result2 = rateio_rule.process(remnant, malha, load_date, num_semanas=rateio_conf['semanas'])
                union = pd.concat([result[cols], result2[cols]], sort=False).reset_index(drop=True)
            else:
                union = rateio_rule.process(result, malha, load_date, num_semanas=rateio_conf['semanas'])
                union = union[cols]

        union['ns_gross'] = np.where(union.dsc_motivo == 'Pedido Normal', 0, union.marcacao)

        # print('=== RATEIO ===')
        # print(union.shape)
        # print(union.marcacao.sum(), union.ns_gross.sum())

        # === REGRA DO FURO ===
        filter = (union.dsc_motivo == 'Pedido Normal') & (union.cod_justificativa == 0) & \
                 (union.cod_justificativa_bo == 0) & (union.bln_pedido_faturado == 'N') & \
                 (union.sgl_status_item == 'EX')

        union.loc[filter, 'dsc_motivo'] = 'Furo'
        union.loc[union.dsc_motivo == 'Furo', 'ns_gross'] = union.marcacao
        # ===================

        # print('=== UNION 2 ===')
        # print(union.shape)
        # print(union.marcacao.sum(), union.ns_gross.sum())

        # === VOLTA PERNA ===
        if voltaperna_conf['on']:
            volta_perna_rule = VoltaPerna()

            # Status p/ volta da perna
            union = volta_perna_rule.process(union, malha,
                                             load_date=load_date,
                                             num_voltas=1,
                                             num_semanas=voltaperna_conf['semanas'],
                                             motivos=voltaperna_conf.get('motivos'))

        # print('=== VOLTA PERNA ===')
        # print(union.shape)
        # print(union.marcacao.sum(), union.ns_gross.sum())

        # ====== Marca última fábrica  sem volta da perna
        union['cod_fab'] = np.where(union.cod_fab.isnull(), union.cod_cliente, union.cod_fab)
        union['dsc_canal'] = np.where(union.dsc_canal == 'foto', 'ASVD', union.dsc_canal.str.strip())

        union['cod_cliente'] = np.where(union.dsc_canal != 'ASVD', union.cod_fab, union.cod_cliente)
        union['cod_cliente'] = np.where(union.dsc_canal == 'ASVD', union.cod_unidade, union.cod_cliente)

        output = self.append_marginal_tables(union)

        # ====== Regra do Carro Unico
        filter = (output.cod_bo.notnull()) & (output.sgl_status_item == 'EX') & (output.bln_pedido_faturado == 'S') & \
                 (output.total_cars == 1)

        output.loc[filter, 'ns_gross'] = 0
        output.loc[filter, 'dsc_motivo'] = 'Pedido Normal'

        return output

    # First union of FOTO and PROMAX
    def unite(self, foto: pd.DataFrame, promax: pd.DataFrame) -> pd.DataFrame:
        final_cols = ['cod_unidade', 'cod_cliente', 'cod_cliente_orig', 'cod_produto', 'dat_puxada', 'dsc_motivo',
                      'marcacao', 'num_carro', 'num_item', 'num_pedido', 'cod_justificativa', 'cod_justificativa_bo',
                      'sgl_status_item', 'bln_pedido_faturado', 'cod_bo', 'dsc_canal',  'total_cars', 'origin']

        # -------------
        foto['cod_unidade'] = foto.cod_unb
        foto['marcacao'] = foto.val_qtd_prod_hl
        foto['dsc_canal'] = 'foto'
        foto['origin'] = 'foto'

        foto = foto[final_cols]
        # -------------
        promax['cod_cliente'] = promax.cod_unidade
        promax['cod_cliente_orig'] = promax.cod_unidade
        promax['num_carro'] = np.nan
        promax['num_item'] = np.nan
        promax['num_pedido'] = np.nan
        promax['dat_puxada'] = promax.dat_pedido
        promax['marcacao'] = promax.qtd_sku
        promax['cod_justificativa'] = 0
        promax['cod_justificativa_bo'] = 0
        promax['sgl_status_item'] = np.nan
        promax['bln_pedido_faturado'] = np.nan
        promax['cod_bo'] = np.nan
        promax['total_cars'] = np.nan
        promax['origin'] = 'promax'

        promax = promax[final_cols]
        # -------------

        union = pd.concat([foto, promax], sort=False)
        union['dat_original'] = union.dat_puxada
        union['dat_puxada'] = union.dat_puxada.apply(lambda x: pd.Timestamp(Dates.last_monday(x)))
        union['marcacao'] = pd.to_numeric(union.marcacao, errors='coerce')
        union = union.reset_index(drop=True).reset_index().rename(columns={'index': 'id_rastreio'})

        # Campos da Malha
        union['cod_fab'] = np.nan

        # Campos a Adicionar
        union['ns_gross'] = 0

        return union

    # Marginal Tables Data
    def append_marginal_tables(self, df: pd.DataFrame):
        df.reset_index(drop=True, inplace=True)

        join = (
            df
                .merge(Dataset.load('eg_cliente')[['cod_cliente', 'nom_fantasia_cliente']],
                       left_on='cod_cliente_orig',
                       right_on='cod_cliente', suffixes=('', '_1'), how='left')
                .merge(
                Dataset.load('eg_v_produto')[['cod_prod', 'nom_abrev_prod', 'cod_sub_categ_lin_emb',
                                              'nom_sub_categ_lin_emb']],
                left_on='cod_produto',
                right_on='cod_prod',
                suffixes=('', '_2'),
                how='left')
                .merge(Dataset.load('sys_unidades')[['cod_unb_sys', 'cod_unidade']],
                       left_on='cod_fab',
                       right_on='cod_unidade',
                       suffixes=('', '_3'),
                       how='left')
                .merge(Dataset.load('sys_de_para_geo')[['cod_cliente', 'dsc_geo']],
                       left_on='cod_cliente_orig',
                       right_on='cod_cliente',
                       suffixes=('', '_4'),
                       how='left')
                .merge(Dataset.load('bas_regional_unidade'), on='cod_unb_sys', suffixes=('', '_5'), how='left')
                .merge(Dataset.load('bas_regional'), on='cod_regional', suffixes=('', '_6'), how='left')
                .merge(Dataset.load('eg_v_unidade_basica')[['cod_unb', 'nom_abr_unb']],
                       left_on='cod_fab',
                       right_on='cod_unb',
                       suffixes=('', '_7'),
                       how='left')
                .merge(Dataset.load('v_produto_tipo_emb')[['cod_prod', 'cod_tipo']],
                       left_on='cod_produto',
                       right_on='cod_prod',
                       suffixes=('', '_8'),
                       how='left')
                .merge(Dataset.load('sys_justificativa')[['cod_justificativa', 'dsc_justificativa']],
                       on='cod_justificativa',
                       suffixes=('', '_9'),
                       how='left')
                .merge(Dataset.load('sys_justificativa_bo')[['cod_justificativa', 'dsc_justificativa']],
                       left_on='cod_justificativa_bo',
                       right_on='cod_justificativa',
                       suffixes=('', '_10'),
                       how='left')
                .merge(Dataset.load('bas_embalagem_grupo'),
                       left_on='cod_sub_categ_lin_emb',
                       right_on='cod_embalagem',
                       suffixes=('', '_11'),
                       how='left')
                .merge(Dataset.load('bas_embalagem_fechada'), on='cod_embalagem_fechada', suffixes=('', '_12'),
                       how='left')
        )

        join['liquido'] = np.where(join.cod_tipo.isin([1, 28]), 'CERVEJA', 'REFRIGENANC')
        join['dsc_justificativa_bo'] = join.dsc_justificativa_10
        join['entrada'] = np.where(join.origin == 'foto', '1ST TIER', '2ND TIER')
        join['embalagem_aberta'] = join.nom_sub_categ_lin_emb
        join['embalagem_fechada'] = join.dsc_embalagem

        return join

    # REPORT preparation
    def prepare_report(self, df: pd.DataFrame):

        df['cod_fab'] = pd.to_numeric(df.cod_fab, errors='coerce').astype(pd.Int32Dtype())
        df['cod_cliente'] = pd.to_numeric(df.cod_cliente, errors='coerce').astype(pd.Int32Dtype())
        df['cod_cliente_orig'] = pd.to_numeric(df.cod_cliente_orig, errors='coerce').astype(pd.Int32Dtype())
        df['marcacao'] = df.marcacao.apply(lambda x: str(x).replace('.', ','))
        df['ns_gross'] = df.ns_gross.apply(lambda x: str(x).replace('.', ','))
        df['cod_justificativa'] = pd.to_numeric(df.cod_justificativa, errors='coerce').astype(pd.Int32Dtype())
        df['cod_justificativa_bo'] = pd.to_numeric(df.cod_justificativa_bo, errors='coerce').astype(pd.Int32Dtype())

        cols = {
            'cod_fab': 'Cod Unidade',
            'nom_abr_unb': 'NomeUnidade',
            'cod_cliente': 'Cod Unidade Orig',
            'dsc_regional': 'Regional',
            'cod_cliente_orig': 'Cod Cliente',
            'nom_fantasia_cliente': 'Nome Cliente',
            'dsc_geo': 'Geografia',
            'liquido': 'Categoria',
            'embalagem_aberta': 'Emb. Aberta',
            'embalagem_fechada': 'Emb. Fechada',
            'cod_produto': 'CodProduto',
            'nom_abrev_prod': 'Nome Prod',
            'dat_original': 'Data Puxada',
            'marcacao': 'Marcacao',
            'ns_gross': 'NS GROSS',
            'sgl_status_item': 'Status Item',
            'dsc_motivo': 'Motivo',
            'num_carro': 'Numero Carro',
            'cod_justificativa': 'Cod Justificativa',
            'dsc_justificativa': 'Justificativa',
            'cod_justificativa_bo': 'Cod Justificativa BO',
            'dsc_justificativa_bo': 'Justificativa BO',
            'dsc_canal': 'Canal Marcacao',
            'entrada': 'Entrada'
        }

        output = df.loc[:, list(cols.keys())].rename(columns=cols)
        return output