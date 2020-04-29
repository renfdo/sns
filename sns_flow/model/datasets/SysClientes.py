from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysClientes:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysClientes.singleton is None:
            SysClientes.singleton = MysqlDAO().read_table('sys_clientes')

        return SysClientes.singleton
