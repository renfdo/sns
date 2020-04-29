from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class SysProdutos:
    singleton = None

    @staticmethod
    def __new__(cls):
        if SysProdutos.singleton is None:
            sys_produtos = MysqlDAO().read_table('sys_produtos')
            sys_produtos['cod_prod_promax'] = sys_produtos.cod_prod_promax.astype(int)
            SysProdutos.singleton = sys_produtos

        return SysProdutos.singleton
