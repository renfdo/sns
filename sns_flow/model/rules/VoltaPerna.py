import numpy as np
import pandas as pd

from sns_flow.helpers.dates import Dates


class VoltaPerna:

    def process(self, result: pd.DataFrame, malha: pd.DataFrame, load_date: str,
                num_voltas=1, num_semanas=4, motivos=None) -> pd.DataFrame:

        if motivos is None:
            motivos = ['Falta Real', 'Falta de Produto', 'Falta Teórica']

        last_monday = Dates.last_monday(load_date)

        append = pd.DataFrame()

        final = result[~result.dsc_motivo.isin(motivos)].copy()
        aux = result[result.dsc_motivo.isin(motivos)].copy()

        aux.reset_index(drop=True, inplace=True)
        aux.rename(columns={'cod_cliente': 'cod_cliente_init'}, inplace=True)

        for _ in range(num_voltas):
            for _ in range(num_semanas):
                aux['cod_cliente'] = aux.cod_fab

                join = aux.merge(malha.query(f'dat_puxada == "{last_monday}"'), on=['cod_cliente', 'cod_produto'],
                                 suffixes=('', '_y'), right_index=True)

                join['cod_fab'] = join.cod_fab_y
                aux.drop(join.index, inplace=True)
                append = pd.concat([append, join], sort=False)
                last_monday = Dates.last_monday(Dates.back_days(last_monday, days=1))

        aux = aux[final.columns]
        append = append[final.columns]
        final = pd.concat([final, append, aux], sort=False)

        return final


