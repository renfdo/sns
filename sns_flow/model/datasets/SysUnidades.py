from sns_flow.mysql_db.MysqlDAO import MysqlDAO
import pandas as pd


class SysUnidades:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysUnidades.singleton is None:
            df = MysqlDAO().read_table('sys_unidades')
            df['cod_unidade'] = pd.to_numeric(df.cod_unidade, errors='coerce')
            SysUnidades.singleton = df

        return SysUnidades.singleton
