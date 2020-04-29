from sns_flow.mysql_db.MysqlDAO import MysqlDAO
from sns_flow.helpers.dates import Dates
from .InsumoLog import InsumoLog

import pandas as pd


class Malha:
    singleton = None
    load_date = None

    @staticmethod
    def __new__(cls, load_date=None, limit=45):

        if Malha.singleton is None or Malha.load_date != load_date:
            insumos = InsumoLog()

            cols = {
                'id_file_id': 'id_file_id',
                'CodDir': 'cod_unb_dir',
                'CodCom': 'cod_com',
                'CodFab': 'cod_fab',
                'Cod_Cliente': 'cod_cliente',
                'CodPro': 'cod_produto',
                'Semana': 'dat_puxada',
                'Tipo_Malha': 'dsc_tipo_malha',
                'Malha': 'val_malha',
                'MalhaAjustada': 'val_malha_ajustada',
                'Real': 'val_real'
            }

            limit_day = Dates.back_days(load_date, days=limit)
            df = insumos.query(f'type_file == "MALHA" and data_max >= "{limit_day}"')

            ids = [str(s) for s in df.id.values]

            malha = MysqlDAO().read_table('insumo_insumoconsolidado',
                                          columns=list(cols.keys()),
                                          filters=f'id_file_id IN({",".join(ids)})')

            malha = malha.rename(columns=cols)[cols.values()]

            malha['cod_cliente'] = malha.cod_cliente.str.replace('-.*', '', regex=True).astype(int)
            malha['dat_puxada'] = pd.to_datetime(malha.dat_puxada, format='%d/%m/%Y')
            malha['dsc_tipo_malha'] = malha.dsc_tipo_malha.apply(lambda x: x.strip()[:4])
            malha[['val_malha', 'val_malha_ajustada', 'val_real']] = \
                malha[['val_malha', 'val_malha_ajustada', 'val_real']].replace(',', '.', regex=True).astype(float)

            malha.query(f'dat_puxada >= "{limit_day}" and val_malha != 0', inplace=True)
            malha.sort_values('id_file_id', ascending=False, inplace=True)

            malha.drop('id_file_id', axis=1, inplace=True)

            # Removendo duplicados na Malha - (Só para Alocação Normal AS IS)
            malha.drop_duplicates(subset=['cod_cliente', 'cod_produto', 'dat_puxada'], inplace=True)

            # ----------------------
            Malha.load_date = load_date
            Malha.singleton = malha

        return Malha.singleton
