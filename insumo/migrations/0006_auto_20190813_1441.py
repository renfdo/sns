# Generated by Django 2.2.1 on 2019-08-13 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0005_auto_20190813_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumoconsolidado',
            name='codpro',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
