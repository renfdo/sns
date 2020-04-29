from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysMotivos:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysMotivos.singleton is None:
            SysMotivos.singleton = MysqlDAO().read_table('sys_motivos')

        return SysMotivos.singleton
