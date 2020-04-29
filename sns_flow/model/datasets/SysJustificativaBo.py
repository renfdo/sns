from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysJustificativaBo:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysJustificativaBo.singleton is None:
            SysJustificativaBo.singleton = MysqlDAO().read_table('sys_justificativa_bo') \
                .drop_duplicates(subset='cod_justificativa')

        return SysJustificativaBo.singleton
