from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta


class Motivos(models.Model):

    cod_motivo = models.AutoField(primary_key=True)
    dsc_motivo = models.CharField(blank=False, null=False, max_length=100)
    ind_ativo = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.dsc_motivo


# JUSTIFICATIVA BO
class JusfiticativaBo(models.Model):

    INDISPONIBILIDADE_BO_CHOICES = [
        (True, 'Sim'),
        (False, 'Nao'),
    ]

    cod_justificativa = models.IntegerField()
    dsc_justificativa = models.CharField(max_length=50)
    val_flag_indisp = models.BooleanField(choices=INDISPONIBILIDADE_BO_CHOICES, default=False)
    data_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    data_alteracao = models.DateTimeField(blank=True, null=True)

    cod_motivo = models.ForeignKey(
        'Motivos',
        name="cod_motivo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='cod_motivo'
    )

    def __str__(self):
        return self.dsc_justificativa


# JUSTIFICATIVA CA
class JusfiticativaCa(models.Model):

    INDISPONIBILIDADE_CA_CHOICES = [
        (True, 'Sim'),
        (False, 'Nao'),
    ]

    cod_justificativa = models.IntegerField(default=0, unique=True)
    cod_tipo_justificativa = models.IntegerField(default=0)
    dsc_justificativa = models.CharField(max_length=50, null=False, default="")
    ind_automatica = models.BooleanField(choices=INDISPONIBILIDADE_CA_CHOICES, default=False)
    ind_cancelamento = models.BooleanField(choices=INDISPONIBILIDADE_CA_CHOICES, default=False)
    val_flag_indisp = models.BooleanField(choices=INDISPONIBILIDADE_CA_CHOICES, default=False)

    data_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    data_alteracao = models.DateTimeField(blank=True, null=True)

    cod_motivo = models.ForeignKey(
        'Motivos',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='cod_motivo'
    )

    def __str__(self):
        return self.dsc_justificativa


# OUTPUT SNS
class SaidaSns(models.Model):
    # TODO: Traduzir nomes para o ingles?
    LIQUID_TYPE_CHOICES = [
        ('TODOS', 'Todos'),
        ('CERVEJA', 'Cerveja'),
        ('REFRIGENANC', 'Refrigerante'),
    ]

    INPUT_CHOICES = [
        ('ADHOC', 'AdHoc'),
        ('CDD', 'CDD'),
        ('REVENDA', 'Revenda'),
        ('FOTO', 'Foto'),
        ('CUBO', 'Cubo'),
        ('DE_PARA_GEO', 'De Para GEO'),
    ]

    CHANNEL_TYPE_CHOICES = [
        ('ASVD', 'ASVD'),
        ('ASCD', 'ASCD'),
        ('REVENDA', 'Revenda'),
        ('ROTA', 'Rota'),
    ]

    cod_fab = models.IntegerField()
    nom_abr_unb = models.CharField(max_length=256)
    cod_cliente = models.IntegerField()
    dsc_regional = models.CharField(max_length=256)
    cod_cliente_orig = models.IntegerField()
    nom_fantasia_cliente = models.CharField(max_length=256)
    dsc_geo = models.CharField(max_length=256)
    liquido = models.CharField(max_length=256, choices=LIQUID_TYPE_CHOICES, null=True)
    embalagem_fechada = models.CharField(max_length=256)
    embalagem_aberta = models.CharField(max_length=256)
    cod_produto = models.IntegerField()
    nom_abrev_prod = models.CharField(max_length=256)
    dat_original = models.DateField()
    marcacao = models.CharField(max_length=256)
    ns_gross = models.IntegerField()
    sgl_status_item = models.CharField(max_length=256)
    dsc_motivo = models.CharField(max_length=256)
    num_carro = models.IntegerField()
    cod_justificativa = models.IntegerField()
    dsc_justificativa = models.CharField(max_length=256)
    cod_justificativa_bo = models.IntegerField()
    dsc_justificativa_bo = models.CharField(max_length=256)
    canal = models.CharField(max_length=256)
    entrada = models.CharField(max_length=256)


    # liquid_type = models.CharField(
    #     max_length=12,
    #     choices=LIQUID_TYPE_CHOICES,
    #     default='TODOS',
    # )
    # # insumo
    # input_type = models.CharField(
    #     max_length=12,
    #     choices=INPUT_CHOICES,
    #     default='ADHOC',
    # )
    # channel_type = models.CharField(
    #     max_length=7,
    #     choices=CHANNEL_TYPE_CHOICES,
    #     default='ROTA',
    # )
    business_key = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.justificativa


class LogProcessoBatchManager(models.Manager):

    def is_running(self):
        self.finish_runing_process()
        query = super().get_queryset().filter(data_fim__isnull=True).count()
        return True if query > 0 else False

    def finish_runing_process(self):
        limit = datetime.now() - timedelta(minutes=5)
        batchs = super().get_queryset().filter(
                                                Q(data_fim__isnull=True) &
                                                Q(data_inicio__lt=limit)
                                            )
        ''' se existe registro com mais de 5 minutos rodando, o processo entende que foi deu erro e gera 
        um status CANCELADO '''
        batchs.update(
                data_fim=datetime.now(),
                status="CANCELADO",
                mensagem="Processo cancelado pelo sistema.",
        )


class LogProcessoBatch(models.Model):

    objects = LogProcessoBatchManager()

    STATUS_CHOICES = [
        ('CANCELADO', 'Cancelado'),
        ('EXECUCAO', 'Em execução'),
        ('ERRO', 'ERRO'),
        ('FINALIZADO', 'Finalizado'),
    ]

    data_inicio = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    data_fim = models.DateTimeField(blank=False, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='TODOS',
    )
    mensagem = models.CharField(max_length=500, null=True)


class SNSRuleManager(models.Manager):

    def get_last_rules(self):
        query_set = super().get_queryset().filter(~Q(rule='mto')).values('rule').annotate(models.Max('pk'))
        ids = [id['pk__max'] for id in query_set.values('pk__max')]

        query_set = super().get_queryset().filter(pk__in=ids)
        return query_set

    def to_dict(self):
        query = self.get_last_rules()

        rules = {}
        for row in query:
            rules[row.rule] = {
                                'on': row.is_active,
                                'semanas': row.value,
                                }
        return rules


class ParametrosSNSRule(models.Model):

    RULES_CHOICES = [
        ('rateio', 'Rateio'),
        ('volta_perna', 'Volta da Perna'),
        ('alocacao_normal', 'Alocação Normal / Malha Compartilhada'),
        ('mto', 'MTO'),
    ]

    IS_ACTIVE_CHOICES = [
        (True,"Sim"),
        (False, "Não"),
    ]

    is_active = models.BooleanField(blank=False, null=False, default=True, choices=IS_ACTIVE_CHOICES)
    rule = models.CharField(max_length=500, choices=RULES_CHOICES, null=False)
    value = models.IntegerField(null=True, default=0)
    data_insert = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    objects = models.Manager()
    manager_objects = SNSRuleManager()

