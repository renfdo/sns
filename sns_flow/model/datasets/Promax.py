from sns_flow.mysql_db.MysqlDAO import MysqlDAO
from .InsumoLog import InsumoLog

from sns_flow.helpers.dataset import Dataset
from sns_flow.helpers.dates import Dates

import numpy as np
import pandas as pd


class Promax:
    singleton = None
    load_date = None

    @staticmethod
    def __new__(cls, load_date=load_date):

        if Promax.singleton is None or Promax.load_date != load_date:
            insumos = InsumoLog()

            d7 = Dates.back_days(load_date, days=7)

            insumos.loc[insumos.type_file == 'PROMAX', 'fixed_name'] = \
                insumos[insumos.type_file == 'PROMAX'].file_name.str.split('_').str[:2].str.join('_')

            df = insumos[insumos.type_file == 'PROMAX'].nlargest(32, 'processed_date') \
                .drop_duplicates(subset='fixed_name')

            ids = [str(s) for s in df.id.values]

            promax = MysqlDAO().read_table('insumo_insumopromax', filters=f'id_file_id IN({",".join(ids)})')

            promax.drop(['id', 'id_file_id'], axis=1, inplace=True)

            promax['dat_pedido'] = pd.to_datetime(promax.dat_pedido, format='%d/%m/%Y', errors='coerce')
            promax['qtd_sku'] = pd.to_numeric(promax.qtd_sku.str.replace(',', '.'), errors='coerce')
            promax = promax[(promax.dat_pedido.notnull()) & (promax.dat_pedido >= pd.Timestamp(d7))]

            promax['cod_unidade'] = np.where(
                promax.dsc_canal == 'Revenda',
                pd.to_numeric(promax.cod_unidade.astype(pd.Int32Dtype()).astype(str).str[:-1], errors='coerce'),
                promax.cod_unidade
            )

            promax['cod_produto'] = promax.cod_produto.astype(int)

            promax = promax.merge(
                Dataset.load('sys_produtos'), left_on='cod_produto', right_on='cod_prod_promax', how='left'
            )

            promax['cod_produto'] = np.where(promax.cod_produto_y.notnull(), promax.cod_produto_y, promax.cod_produto_x)

            promax['dsc_motivo'] = promax.dsc_motivo.str.strip()

            promax = (
                promax[promax.cod_unidade.notnull()]
                .groupby(['cod_unidade', 'dat_pedido', 'cod_produto', 'dsc_motivo', 'dsc_canal'], as_index=False)
                .agg({
                    'qtd_sku': 'sum'
                })
            )

            # -----
            Promax.load_date = load_date
            Promax.singleton = promax

        return Promax.singleton
