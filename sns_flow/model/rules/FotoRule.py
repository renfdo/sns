import numpy as np
import pandas as pd
from sns_flow.helpers.dataset import Dataset


class FotoRule:
    # Statuses
    PEDIDO_NORMAL = 'Pedido Normal'
    FALTA_PRODUTO = 'Falta de Produto'

    def process(self, foto: pd.DataFrame) -> pd.DataFrame:

        # --------- Adição do MOTIVO ---------------
        foto['cod_bo'] = pd.to_numeric(foto.cod_bo, errors='coerce')
        foto['cod_justificativa'] = pd.to_numeric(foto.cod_justificativa, errors='coerce').fillna(0)
        foto['cod_justificativa_bo'] = pd.to_numeric(foto.cod_justificativa_bo, errors='coerce').fillna(0)
        foto['dsc_motivo'] = np.nan

        sys_justificativa = Dataset.load('sys_justificativa').query('val_flag_indisp == 1')

        join = (
            foto
            .merge(sys_justificativa, on='cod_justificativa', right_index=True)
            .merge(Dataset.load('sys_motivos'), on='cod_motivo', right_index=True)
        )

        foto.loc[join.index, 'dsc_motivo'] = join.dsc_motivo_y
        # -----------------------------
        sys_justificativa_bo = (
            Dataset.load('sys_justificativa_bo')
            .query('val_flag_indisp == 1 and cod_justificativa != 0')
            .rename(columns={'cod_justificativa': 'cod_justificativa_bo'})
        )

        join = (
            foto
            .merge(sys_justificativa_bo, on='cod_justificativa_bo', right_index=True)
            .merge(Dataset.load('sys_motivos'), on='cod_motivo', right_index=True)
        )

        foto.loc[join.index, 'dsc_motivo'] = join.dsc_motivo_y

        foto.loc[(foto.cod_justificativa == 0) & (foto.cod_justificativa_bo == 0), 'dsc_motivo'] = 'Pedido Normal'

        # --------------------

        bo = foto[foto.cod_bo.notnull()]
        foto = foto[foto.cod_bo.isnull()]

        # Merge back together
        foto['total_cars'] = 0
        foto = pd.concat([foto, self.generate_bo(bo)], sort=False)

        return foto

    # Calc products presence in cars, maintaining preference for last one
    def generate_bo(self, bo: pd.DataFrame) -> pd.DataFrame:

        # Agg BO
        bo_agg = (
            bo
            .groupby(['cod_bo', 'cod_cliente', 'num_carro', 'dat_puxada', 'cod_produto'], as_index=False)
            .agg({
                'val_qtd_prod_hl': 'sum'
            })
            .groupby(['cod_bo', 'cod_cliente', 'dat_puxada', 'cod_produto'], as_index=False)
            .agg({
                'num_carro': list,
                'val_qtd_prod_hl': list
            })
        )

        bo_agg['total_cars'] = bo_agg.num_carro.apply(len)
        # ---------------------------------------------------

        bo_agg['car'] = np.nan
        bo_agg['value'] = np.nan
        bo_agg['dsc_motivo'] = np.nan

        rows = []

        # --- Iterate to set
        for idx, row in bo_agg.iterrows():
            total = len(row['val_qtd_prod_hl'])
            output, car_out = [], []

            cars_count = len(row['num_carro'])
            second_car = row['num_carro'][1] if cars_count > 1 else row['num_carro'][0]

            if total == 1:  # Caso o produto aparece apenas em 1 carro
                output.append(row['val_qtd_prod_hl'][0])
                car_out.append(row['num_carro'][0])
                motivo = self.PEDIDO_NORMAL if second_car == row['num_carro'][0] else self.FALTA_PRODUTO
                motivo = 'UPDATE' if cars_count == 1 else motivo  # P/ atualizacao posterior
            elif total > 1:  # Caso 2+ carros
                calc = row['val_qtd_prod_hl'][1] - row['val_qtd_prod_hl'][0]

                output = row['val_qtd_prod_hl'][1]
                car_out = row['num_carro'][1]
                motivo = self.PEDIDO_NORMAL

                if calc < 0:
                    # Linhas c/ Falta de Produto - Resto do cálculo
                    row['car'] = row['num_carro'][0]
                    row['value'] = abs(calc)
                    row['dsc_motivo'] = self.FALTA_PRODUTO
                    rows.append(row)

            bo_agg.loc[idx, ['car']] = car_out
            bo_agg.loc[idx, ['value']] = output
            bo_agg.loc[idx, ['dsc_motivo']] = motivo

        # Add the extra rows
        bo_agg = pd.concat([bo_agg, pd.DataFrame(rows)], sort=False)
        # ----------------------------------------

        # Merge back with inital dataframe
        join_bo = (
            bo
            .drop_duplicates(subset=['cod_bo', 'cod_cliente', 'cod_produto', 'dat_puxada'], keep='last')
            .merge(bo_agg, on=['cod_bo', 'cod_cliente', 'cod_produto', 'dat_puxada'], suffixes=('', '_y'))
        )

        # Update with new values
        join_bo['num_carro'] = join_bo.car
        join_bo['val_qtd_prod_hl'] = join_bo.value
        join_bo['dsc_motivo'] = np.where(join_bo.dsc_motivo_y == 'UPDATE', join_bo.dsc_motivo, join_bo.dsc_motivo_y)

        return join_bo[bo.columns]


