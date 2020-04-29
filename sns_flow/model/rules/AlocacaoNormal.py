import numpy as np
import pandas as pd

from sns_flow.helpers.dates import Dates


class AlocacaoNormal:

    def process(self, union: pd.DataFrame, malha: pd.DataFrame, load_date: str,
                num_semanas=5) -> (pd.DataFrame, pd.DataFrame):

        # limit_days = Dates.back_days(load_date, days=limit)  # Normalmente 45 dias atras

        union['ns_gross'] = np.where(union.dsc_motivo.str.strip() == 'Pedido Normal', 0, union.marcacao)

        final = pd.DataFrame()
        aux = union.copy()

        aux = aux[aux.cod_cliente.notnull()]

        last_monday = Dates.last_monday(load_date)

        for _ in range(num_semanas):
            join = aux.merge(malha.query(f'dat_puxada == "{last_monday}"'), on=['cod_cliente', 'cod_produto'],
                             suffixes=('', '_y'), right_index=True)

            join['cod_fab'] = join.cod_fab_y
            aux.drop(join.index, inplace=True)
            final = pd.concat([final, join], sort=False)
            last_monday = Dates.last_monday(Dates.back_days(last_monday, days=1))

        return final, aux
