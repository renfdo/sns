from rest_framework import serializers
from .models import *


class InsumoPromaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoPromax
        fields = (
            'cod_unidade',
            'nom_unidade',
            'nom_geo',
            'dat_pedido',
            'cod_produto',
            'nom_produto',
            'dsc_motivo',
            'qtd_sku',
            'dsc_canal'
        )


class InsumoConsolidadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoConsolidado
        fields = (
            'coddir',
            'nomedir',
            'codcom',
            'nomecom',
            'codfab',
            'nomefab',
            'cod_cliente',
            'nomecliente',
            'codpro',
            'nomepro',
            'marca',
            'linemb',
            'tipomarcaprod',
            'semana',
            'tipo_malha',
            'malha',
            'malhaajustada',
            'real',
            'comprometido',
            'devolucoes',
            'tendnumerica',
            'tendlinear',
            'dispersao',
            'fatorhl',
            'processed_date',
            'data_puxada'
        )

class InsumoRastreabilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoRastreabilidade
        fields = (
            'cod_tipo',
            'cod_cliente',
            'dat_exportacao',
            'dat_importacao',
            'dat_aprovacao',
            'dat_tratamento_pedido',
            'dat_inclusao_pendencia',
            'dat_puxada',
            'dat_cancelamento_nf',
            'etapa_g2',
            'hra_puxada',
            'hra_aprovacao_pendencia',
            'hra_inclusao_pendencia',
            'hra_exportacao_pedido',
            'hra_inclusao_pedido',
            'hra_tratamento_pedido',
            'cod_justificativa_bo',
            'cod_justificativa_ca',
            'cod_nota_fiscal',
            'val_item_nota_fiscal',
            'cod_produto_nf',
            'val_qtd_sku_prod_nf',
            'val_qtd_HL_prod_nf',
            'cod_bo',
            'num_carro',
            'num_item',
            'num_pedido',
            'bln_pedido_faturado',
            'cod_pendencia_pedido',
            'cod_produto',
            'val_qtd_prod_hl',
            'val_qtd_prod_sku',
            'sgl_status_carro',
            'sgl_status_item',
            'dsc_tipo_cliente',
            'sgl_tipo_nota_fiscal',
            'cod_unb_comercial',
            'cod_unb_destino',
            'bln_unb_fora_malha',
            'cod_unb_origem',
            'cod_geo',
            'sgl_tipo_canal',
            'dsc_status_bo',
            'dat_carregamento',
            'dat_emissao_nf',
            'cod_tipo_categ_bo',
            'cod_tipo_subcateg_bo',
            'dat_puxada_original',
            'num_carro_original',
            'Processed_date',
            'data_puxada',
        )


class InsumoADHOCCUBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoADHOCCUBO
        fields = '__all__'
