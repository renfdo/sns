# Generated by Django 2.2.1 on 2019-08-15 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0005_auto_20190815_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jusfiticativabo',
            name='cod_motivo',
            field=models.ForeignKey(db_column='cod_motivo', null=True, on_delete=django.db.models.deletion.CASCADE, to='sns.Motivos'),
        ),
        migrations.AlterField(
            model_name='jusfiticativaca',
            name='cod_motivo',
            field=models.ForeignKey(db_column='cod_motivo', null=True, on_delete=django.db.models.deletion.CASCADE, to='sns.Motivos'),
        ),
    ]