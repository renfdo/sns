from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class BasRegional:
    singleton = None

    @staticmethod
    def __new__(cls):
        if BasRegional.singleton is None:
            BasRegional.singleton = MysqlDAO().read_table('bas_regional')

        return BasRegional.singleton
