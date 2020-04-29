from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class EgVUnidadeBasica:
    singleton = None

    @staticmethod
    def __new__(cls):
        if EgVUnidadeBasica.singleton is None:
            EgVUnidadeBasica.singleton = MysqlDAO().read_table('eg_v_unidade_basica')

        return EgVUnidadeBasica.singleton
