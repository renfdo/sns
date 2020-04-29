from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class EgVProduto:
    singleton = None

    @staticmethod
    def __new__(cls):
        if EgVProduto.singleton is None:
            eg_v_produto = MysqlDAO().read_table('eg_v_produto')
            eg_v_produto = eg_v_produto[eg_v_produto.dat_exc.isnull()].drop_duplicates(subset='cod_prod')
            # eg_v_produto = eg_v_produto.drop_duplicates(subset='cod_prod')

            EgVProduto.singleton = eg_v_produto

        return EgVProduto.singleton
