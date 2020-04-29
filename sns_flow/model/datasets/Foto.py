from sns_flow.mysql_db.MysqlDAO import MysqlDAO
from .InsumoLog import InsumoLog

import numpy as np
import pandas as pd

from sns_flow.helpers.dataset import Dataset


class Foto:
    singleton = None
    load_date = None

    @staticmethod
    def __new__(cls, load_date=load_date):

        if Foto.singleton is None or load_date != Foto.load_date:
            insumos = InsumoLog()
            df = insumos[insumos.type_file == 'FOTO'].nlargest(1, 'processed_date')
            foto = MysqlDAO().read_table('insumo_insumorastreabilidade', filters=f'id_file_id = {df.id.values[0]}')
            foto.drop(['id', 'id_file_id'], axis=1, inplace=True)

            foto['cod_cliente'] = pd.to_numeric(foto.cod_cliente.astype(pd.Int32Dtype()).astype(str).str[:-1],
                                                errors='coerce')
            foto['dat_importacao'] = pd.to_datetime(foto.dat_importacao, format='%d/%m/%Y', errors='coerce')
            foto['dat_puxada'] = pd.to_datetime(foto.dat_puxada, format='%d/%m/%Y', errors='coerce')

            foto.query(f'dat_puxada == "{load_date}"', inplace=True)

            foto = foto.merge(Dataset.load('sys_clientes'), on='cod_cliente', how='left')

            foto = foto[foto.cod_tipo_cli != 1]  # Cod 1 = Revenda

            foto['cod_cliente_orig'] = foto.cod_cliente

            foto['dsc_tipo_cliente'] = pd.to_numeric(foto.dsc_tipo_cliente, errors='coerce')  # Adicionado

            foto['cod_cliente'] = np.where(foto.dsc_tipo_cliente == 2, foto.cod_unb_comercial, foto.cod_cliente)

            foto['cod_cliente'] = pd.to_numeric(foto.cod_cliente, errors='coerce')  # Adicionado

            foto = foto[~foto.cod_tipo.isin([1, 99])]

            foto.rename(columns={
                'cod_justificativa_ca': 'cod_justificativa',
                'cod_unb_origem': 'cod_unb'
            }, inplace=True)

            foto = foto.merge(Dataset.load('sys_produtos'), suffixes=('', '_y'), on='cod_produto', how='left')
            foto = foto[foto.cod_tipo_produto.isin([1, 2, 10, 12])]

            foto = foto[~((foto.sgl_status_item == '') & (foto.sgl_status_item.isnull()))]

            # Removendo duplicados
            cols = ['num_carro', 'num_item', 'cod_produto', 'val_qtd_prod_hl', 'sgl_status_item', 'dat_puxada',
                    'num_pedido']
            foto = foto[foto.cod_cliente.notnull()].drop_duplicates(subset=cols)

            # ------
            Foto.load_date = load_date
            Foto.singleton = foto

        return Foto.singleton
