from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysDeParaGeo:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysDeParaGeo.singleton is None:
            SysDeParaGeo.singleton = MysqlDAO().read_table('sys_de_para_geo')

        return SysDeParaGeo.singleton
