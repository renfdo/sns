from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysJustificativa:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysJustificativa.singleton is None:
            SysJustificativa.singleton = MysqlDAO().read_table('sys_justificativa') \
                .drop_duplicates(subset='cod_justificativa')

        return SysJustificativa.singleton
