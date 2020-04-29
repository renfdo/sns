from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class BasRegionalUnidade:
    singleton = None

    @staticmethod
    def __new__(cls):
        if BasRegionalUnidade.singleton is None:
            BasRegionalUnidade.singleton = MysqlDAO().read_table('bas_regional_unidade')

        return BasRegionalUnidade.singleton
