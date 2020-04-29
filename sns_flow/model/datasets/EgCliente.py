from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class EgCliente:
    singleton = None

    @staticmethod
    def __new__(cls):
        if EgCliente.singleton is None:
            EgCliente.singleton = MysqlDAO().read_table('eg_cliente')

        return EgCliente.singleton
