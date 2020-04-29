import numpy as np
import pandas as pd

from sns_flow.helpers.dataset import Dataset
from sns_flow.helpers.dates import Dates

class PromaxRule:

    def process(self, promax: pd.DataFrame, dat_puxada: str, days=7) -> pd.DataFrame:

        d7 = Dates.back_days(dat_puxada, days=days)
        promax = promax[(promax.dat_pedido.notnull()) & (promax.dat_pedido >= pd.Timestamp(d7))]

        promax = promax.merge(Dataset.load('sys_produtos'),
                              left_on='cod_produto', right_on='cod_prod_promax', how='left')

        promax['cod_produto'] = np.where(promax.cod_produto_y.notnull(), promax.cod_produto_y, promax.cod_produto_x)

        promax = (
            promax[promax.cod_unidade.notnull()]
            .groupby(['cod_unidade', 'dat_pedido', 'cod_produto', 'dsc_motivo', 'dsc_canal'], as_index=False)
            .agg({'qtd_sku': 'sum'})
        )

        return promax

