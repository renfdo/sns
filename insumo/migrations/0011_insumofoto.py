# Generated by Django 2.2.1 on 2019-10-13 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0010_auto_20190815_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsumoFoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_tipo', models.BigIntegerField(null=True)),
                ('cod_cliente', models.FloatField(null=True)),
                ('dat_exportacao', models.CharField(max_length=200, null=True)),
                ('dat_importacao', models.CharField(max_length=200, null=True)),
                ('dat_aprovacao', models.CharField(max_length=200, null=True)),
                ('dat_tratamento_pedido', models.CharField(max_length=200, null=True)),
                ('dat_inclusao_pendencia', models.CharField(max_length=200, null=True)),
                ('dat_puxada', models.CharField(max_length=200, null=True)),
                ('dat_cancelamento_nf', models.CharField(max_length=200, null=True)),
                ('etapa_g2', models.FloatField(null=True)),
                ('hra_puxada', models.FloatField(null=True)),
                ('hra_aprovacao_pendencia', models.CharField(max_length=200, null=True)),
                ('hra_inclusao_pendencia', models.CharField(max_length=200, null=True)),
                ('hra_exportacao_pedido', models.CharField(max_length=200, null=True)),
                ('hra_inclusao_pedido', models.CharField(max_length=200, null=True)),
                ('hra_tratamento_pedido', models.CharField(max_length=200, null=True)),
                ('cod_justificativa_bo', models.FloatField(null=True)),
                ('cod_justificativa_ca', models.FloatField(null=True)),
                ('cod_nota_fiscal', models.FloatField(null=True)),
                ('val_item_nota_fiscal', models.FloatField(null=True)),
                ('cod_produto_nf', models.FloatField(null=True)),
                ('val_qtd_sku_prod_nf', models.FloatField(null=True)),
                ('val_qtd_HL_prod_nf', models.FloatField(null=True)),
                ('cod_bo', models.FloatField(null=True)),
                ('num_carro', models.FloatField(null=True)),
                ('num_item', models.FloatField(null=True)),
                ('num_pedido', models.FloatField(null=True)),
                ('bln_pedido_faturado', models.CharField(max_length=200, null=True)),
                ('cod_pendencia_pedido', models.FloatField(null=True)),
                ('cod_produto', models.FloatField(null=True)),
                ('val_qtd_prod_hl', models.FloatField(null=True)),
                ('val_qtd_prod_sku', models.FloatField(null=True)),
                ('sgl_status_carro', models.CharField(max_length=200, null=True)),
                ('sgl_status_item', models.CharField(max_length=200, null=True)),
                ('dsc_tipo_cliente', models.FloatField(null=True)),
                ('sgl_tipo_nota_fiscal', models.CharField(max_length=200, null=True)),
                ('cod_unb_comercial', models.FloatField(null=True)),
                ('cod_unb_destino', models.FloatField(null=True)),
                ('bln_unb_fora_malha', models.CharField(max_length=200, null=True)),
                ('cod_unb_origem', models.FloatField(null=True)),
                ('cod_geo', models.FloatField(null=True)),
                ('sgl_tipo_canal', models.FloatField(null=True)),
                ('dsc_status_bo', models.CharField(max_length=200, null=True)),
                ('dat_carregamento', models.CharField(max_length=200, null=True)),
                ('dat_emissao_nf', models.CharField(max_length=200, null=True)),
                ('cod_tipo_categ_bo', models.FloatField(null=True)),
                ('cod_tipo_subcateg_bo', models.FloatField(null=True)),
                ('dat_puxada_original', models.CharField(max_length=200, null=True)),
                ('num_carro_original', models.FloatField(null=True)),
                ('id_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumo.InsumoLog')),
            ],
        ),
    ]
