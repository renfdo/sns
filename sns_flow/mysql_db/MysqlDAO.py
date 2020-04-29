import pandas as pd
import sqlalchemy

from .Connection import Connection


class MysqlDAO:

    @staticmethod
    def read_table(table, columns='*', filters='') -> pd.DataFrame:
        print(f'========  CARREGANDO TABELA {table} ========')

        if isinstance(columns, list):
            columns = [f'`{c}`' for c in columns]
            columns = ','.join(columns)

        if filters != '':
            filters = f'WHERE {filters}'

        engine = MysqlDAO.create_engine()
        df = pd.read_sql_query(f'SELECT {columns} FROM {table} {filters}', con=engine)
        engine.dispose()

        return df

    '''
        Mode can be: replace|append
    '''

    @staticmethod
    def write_table(table: str, df: pd.DataFrame, mode='replace'):

        if len(df) > 0:
            engine = MysqlDAO.create_engine()
            df.to_sql(table, con=engine, if_exists=mode, index=False, chunksize=1000)

            with engine.begin() as conn:
                conn.execute(f'ALTER TABLE {table} ENGINE = MYISAM')

            engine.dispose()

    @staticmethod
    def create_engine():
        host = Connection.host
        db = Connection.db
        user = Connection.user
        password = Connection.password

        return sqlalchemy.create_engine(
            f'mysql+mysqlconnector://{user}:{password}@{host}/{db}',
            encoding='latin1'
        )

