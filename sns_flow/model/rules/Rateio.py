import numpy as np
import pandas as pd

from sns_flow.helpers.dates import Dates


class Rateio:

    def process(self, result: pd.DataFrame, malha: pd.DataFrame, load_date: str, num_semanas=4) -> pd.DataFrame:
        last_monday = Dates.last_monday(load_date)

        final = pd.DataFrame()
        aux = result.copy()
        aux = aux.reset_index(drop=True)

        aux['marcacao'] = aux.marcacao.fillna(0)
        aux['rateio'] = 1

        for _ in range(num_semanas):
            join = aux.merge(malha.query(f'dat_puxada == "{last_monday}"'), on='cod_cliente', suffixes=('', '_z'),
                             right_index=True)

            join['cod_fab'] = join.cod_fab_z

            aux.drop(join.index, inplace=True)
            final = pd.concat([final, join], sort=False)
            last_monday = Dates.last_monday(Dates.back_days(last_monday, days=1))

        count_df = (
            final
            .groupby(['cod_cliente', 'dat_puxada'], as_index=False)
            .agg({'cod_fab': 'nunique'})
            .rename(columns={'cod_fab': 'ct'})
        )

        subset = ['cod_cliente', 'cod_produto', 'marcacao', 'dsc_motivo', 'dat_original', 'num_carro',
                  'num_item', 'num_pedido', 'cod_fab', 'dsc_canal']

        final = final.drop_duplicates(subset=subset).merge(count_df, on=['cod_cliente', 'dat_puxada'])

        aux['ct'] = 1
        aux['cod_fab'] = np.nan

        # final = pd.concat([final, aux], sort=False) # Apenda o que nao achou malha (adiciona cod_fab nulos)
        final['marcacao'] = final.marcacao / final.ct

        return final
