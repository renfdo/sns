from django.db import models
from .models import InsumoADHOCCUBO

def gen_columns_from_model(model: models.Model):
    r = []
    fields = model._meta.get_fields()
    for field in fields:
        if field.name in ["id", "id_file"]:
            continue
        r.append({ "data": field.name, "searchable": True, "sortable": True })
    return r


TABLES = {
    "promax": {
        "title": "Promax",
        "url": "/insumos/api/protomax/{id}/?format=datatables",
        "columns": [
            { "data": "cod_unidade", "searchable": True, "sortable": True },
            { "data": "nom_unidade", "searchable": True, "sortable": True },
            { "data": "nom_geo", "searchable": True, "sortable": True },
            { "data": "dat_pedido", "searchable": True, "sortable": True },
            { "data": "cod_produto", "searchable": True, "sortable": True },
            { "data": "nom_produto", "searchable": True, "sortable": True },
            { "data": "dsc_motivo", "searchable": True, "sortable": True },
            { "data": "qtd_sku", "searchable": True, "sortable": True },
            { "data": "dsc_canal", "searchable": True, "sortable": True },
        ] 
    },

    "malha": {
        "title": "Malha",
        "url": "/insumos/api/malha/{id}/?format=datatables",
        "columns": [
            { "data": "coddir", "searchable": True, "sortable": True },
            { "data": "nomedir", "searchable": True, "sortable": True },
            { "data": "codcom", "searchable": True, "sortable": True },
            { "data": "nomecom", "searchable": True, "sortable": True },
            { "data": "codfab", "searchable": True, "sortable": True },
            { "data": "nomefab", "searchable": True, "sortable": True },
            { "data": "cod_cliente", "searchable": True, "sortable": True },
            { "data": "nomecliente", "searchable": True, "sortable": True },
            { "data": "codpro", "searchable": True, "sortable": True },
            { "data": "nomepro", "searchable": True, "sortable": True },
            { "data": "marca", "searchable": True, "sortable": True },
            { "data": "linemb", "searchable": True, "sortable": True },
            { "data": "tipomarcaprod", "searchable": True, "sortable": True },
            { "data": "semana", "searchable": True, "sortable": True },
            { "data": "tipo_malha", "searchable": True, "sortable": True },
            { "data": "malha", "searchable": True, "sortable": True },
            { "data": "malhaajustada", "searchable": True, "sortable": True },
            { "data": "real", "searchable": True, "sortable": True },
            { "data": "comprometido", "searchable": True, "sortable": True },
            { "data": "devolucoes", "searchable": True, "sortable": True },
            { "data": "tendnumerica", "searchable": True, "sortable": True },
            { "data": "tendlinear", "searchable": True, "sortable": True },
            { "data": "dispersao", "searchable": True, "sortable": True },
            { "data": "fatorhl", "searchable": True, "sortable": True },
            { "data": "processed_date", "searchable": True, "sortable": True },
            { "data": "data_puxada", "searchable": True, "sortable": True },
        ]
    },

    "foto": {
        "title": "foto",
        "url": "/insumos/api/foto/{id}/?format=datatables",
        "columns": [
            { "data": 'cod_tipo', "searchable": True, "sortable": True },
            { "data": 'cod_cliente', "searchable": True, "sortable": True },
            { "data": 'dat_exportacao', "searchable": True, "sortable": True },
            { "data": 'dat_importacao', "searchable": True, "sortable": True },
            { "data": 'dat_aprovacao', "searchable": True, "sortable": True },
            { "data": 'dat_tratamento_pedido', "searchable": True, "sortable": True },
            { "data": 'dat_inclusao_pendencia', "searchable": True, "sortable": True },
            { "data": 'dat_puxada', "searchable": True, "sortable": True },
            { "data": 'dat_cancelamento_nf', "searchable": True, "sortable": True },
            { "data": 'etapa_g2', "searchable": True, "sortable": True },
            { "data": 'hra_puxada', "searchable": True, "sortable": True },
            { "data": 'hra_aprovacao_pendencia', "searchable": True, "sortable": True },
            { "data": 'hra_inclusao_pendencia', "searchable": True, "sortable": True },
            { "data": 'hra_exportacao_pedido', "searchable": True, "sortable": True },
            { "data": 'hra_inclusao_pedido', "searchable": True, "sortable": True },
            { "data": 'hra_tratamento_pedido', "searchable": True, "sortable": True },
            { "data": 'cod_justificativa_bo', "searchable": True, "sortable": True },
            { "data": 'cod_justificativa_ca', "searchable": True, "sortable": True },
            { "data": 'cod_nota_fiscal', "searchable": True, "sortable": True },
            { "data": 'val_item_nota_fiscal', "searchable": True, "sortable": True },
            { "data": 'cod_produto_nf', "searchable": True, "sortable": True },
            { "data": 'val_qtd_sku_prod_nf', "searchable": True, "sortable": True },
            { "data": 'val_qtd_HL_prod_nf', "searchable": True, "sortable": True },
            { "data": 'cod_bo', "searchable": True, "sortable": True },
            { "data": 'num_carro', "searchable": True, "sortable": True },
            { "data": 'num_item', "searchable": True, "sortable": True },
            { "data": 'num_pedido', "searchable": True, "sortable": True },
            { "data": 'bln_pedido_faturado', "searchable": True, "sortable": True },
            { "data": 'cod_pendencia_pedido', "searchable": True, "sortable": True },
            { "data": 'cod_produto', "searchable": True, "sortable": True },
            { "data": 'val_qtd_prod_hl', "searchable": True, "sortable": True },
            { "data": 'val_qtd_prod_sku', "searchable": True, "sortable": True },
            { "data": 'sgl_status_carro', "searchable": True, "sortable": True },
            { "data": 'sgl_status_item', "searchable": True, "sortable": True },
            { "data": 'dsc_tipo_cliente', "searchable": True, "sortable": True },
            { "data": 'sgl_tipo_nota_fiscal', "searchable": True, "sortable": True },
            { "data": 'cod_unb_comercial', "searchable": True, "sortable": True },
            { "data": 'cod_unb_destino', "searchable": True, "sortable": True },
            { "data": 'bln_unb_fora_malha', "searchable": True, "sortable": True },
            { "data": 'cod_unb_origem', "searchable": True, "sortable": True },
            { "data": 'cod_geo', "searchable": True, "sortable": True },
            { "data": 'sgl_tipo_canal', "searchable": True, "sortable": True },
            { "data": 'dsc_status_bo', "searchable": True, "sortable": True },
            { "data": 'dat_carregamento', "searchable": True, "sortable": True },
            { "data": 'dat_emissao_nf', "searchable": True, "sortable": True },
            { "data": 'cod_tipo_categ_bo', "searchable": True, "sortable": True },
            { "data": 'cod_tipo_subcateg_bo', "searchable": True, "sortable": True },
            { "data": 'dat_puxada_original', "searchable": True, "sortable": True },
            { "data": 'num_carro_original', "searchable": True, "sortable": True },
            { "data": 'Processed_date', "searchable": True, "sortable": True },
            { "data": 'data_puxada', "searchable": True, "sortable": True },
        ]
    },

    "adhoc": {
        "title": "ADHOC",
        "url": "/insumos/api/adhoc/{id}/?format=datatables",
        "columns": gen_columns_from_model(InsumoADHOCCUBO)
    },

    "cube": {
        "title": "CUBE",
        "url": "/insumos/api/cube/{id}/?format=datatables",
        "columns": gen_columns_from_model(InsumoADHOCCUBO)
    }

}