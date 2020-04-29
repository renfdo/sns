from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class BasEmbalagemFechada:
    singleton = None

    @staticmethod
    def __new__(cls):
        if BasEmbalagemFechada.singleton is None:
            BasEmbalagemFechada.singleton = MysqlDAO().read_table('bas_embalagem_fechada')

        return BasEmbalagemFechada.singleton
