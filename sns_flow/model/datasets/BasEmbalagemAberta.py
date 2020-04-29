from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class BasEmbalagemAberta:
    singleton = None

    @staticmethod
    def __new__(cls):
        if BasEmbalagemAberta.singleton is None:
            BasEmbalagemAberta.singleton = MysqlDAO().read_table('bas_embalagem_aberta')

        return BasEmbalagemAberta.singleton
