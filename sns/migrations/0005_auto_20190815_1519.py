# Generated by Django 2.2.1 on 2019-08-15 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0004_auto_20190815_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jusfiticativabo',
            old_name='codigo_justificativa',
            new_name='cod_justificativa',
        ),
        migrations.RenameField(
            model_name='jusfiticativabo',
            old_name='jusfiticativa',
            new_name='dsc_justificativa',
        ),
        migrations.RemoveField(
            model_name='jusfiticativabo',
            name='indisponibilidade',
        ),
        migrations.RemoveField(
            model_name='jusfiticativabo',
            name='modelo_atrelado',
        ),
        migrations.AddField(
            model_name='jusfiticativabo',
            name='cod_motivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sns.Motivos'),
        ),
        migrations.AddField(
            model_name='jusfiticativabo',
            name='val_flag_indisp',
            field=models.BooleanField(choices=[(True, 'Sim'), (False, 'Nao')], default=False),
        ),
        migrations.AlterField(
            model_name='jusfiticativabo',
            name='data_inclusao',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]