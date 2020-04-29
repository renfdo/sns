from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class InsumoLog:
    singleton = None

    @staticmethod
    def __new__(cls):
        if InsumoLog.singleton is None:
            insumos = MysqlDAO().read_table('insumo_insumolog')

            insumos.loc[insumos.type_file == 'PROMAX', 'fixed_name'] = \
                insumos[insumos.type_file == 'PROMAX'].file_name.str.split('_').str[:2].str.join('_')

            InsumoLog.singleton = insumos

        return InsumoLog.singleton
