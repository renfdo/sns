from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class BasEmbalagemGrupo:
    singleton = None

    @staticmethod
    def __new__(cls):
        if BasEmbalagemGrupo.singleton is None:
            BasEmbalagemGrupo.singleton = MysqlDAO().read_table('bas_embalagem_grupo')

        return BasEmbalagemGrupo.singleton
