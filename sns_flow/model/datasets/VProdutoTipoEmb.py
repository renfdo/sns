from sns_flow.mysql_db.MysqlDAO import MysqlDAO


class VProdutoTipoEmb:
    singleton = None

    @staticmethod
    def __new__(cls):
        if VProdutoTipoEmb.singleton is None:
            VProdutoTipoEmb.singleton = MysqlDAO().read_table('v_produto_tipo_emb')

        return VProdutoTipoEmb.singleton
