from django.db import models
from datetime import timedelta, datetime
from django.db.models.functions import Cast
from django.db.models.fields import DateField


class ListDirectory(object):

    def __init__(self,
                 name,
                 isdir,
                 total_files='',
                 data_puxada='',
                 processed_date='',
                 id=''
                 ):
        self.name = name
        self.total_files = total_files
        self.isdir = isdir
        self.data_puxada = data_puxada
        self.processed_date = processed_date
        self.id = id

    def __str__(self):
        return str(self.name)


class InsumoLogManager(models.Manager):

    def get_type_files(self):
        query_set = super().get_queryset().exclude(type_file__in=["MALHA_PROD", "MALHA_REAL"]).values('type_file').annotate(models.Count('file_name'))
        output = []
        for type_file in query_set:
            output.append(ListDirectory(name=type_file['type_file'],
                                        total_files=type_file['file_name__count'],
                                        isdir=True))
        return output

    def get_dates(self, type_file):
        query_set = super().get_queryset()\
            .filter(type_file=type_file)\
            .annotate(processed_date_only=Cast('processed_date', DateField()))\
            .values('processed_date_only')\
            .annotate(models.Count('file_name'))

        output = []

        for result in query_set:
            output.append(ListDirectory(name=result['processed_date_only'].strftime("%Y-%m-%d"),
                                        total_files=result['file_name__count'],
                                        isdir=True))
        return output

    def get_files(self, type_file, data_puxada):
        query_set = super().get_queryset().filter(
            type_file=type_file,
            processed_date__range=[data_puxada, data_puxada+timedelta(seconds=86399)]
        )
        print(type_file)
        print(len(query_set))
        print(data_puxada+timedelta(seconds=86399))

        output = []
        for result in query_set:
            output.append(ListDirectory(name=result.file_name,
                                        isdir=False,
                                        data_puxada=result.data_puxada,
                                        processed_date=result.processed_date,
                                        id=result.pk
                                        ))

        return output


# Log de Insumos
class InsumoLog(models.Model):
    file_name = models.CharField(max_length=100)
    processed_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    data_puxada = models.DateTimeField(blank=True, null=True)
    type_file = models.CharField(max_length=100)

    # TODO: Manter esta nomenclatura?
    data_min = models.DateTimeField(blank=True, null=True)
    data_max = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    manager_objects = InsumoLogManager()

    def data_to_group_by(self):
        return datetime(self.processed_date.year, self.processed_date.month, self.processed_date.day)

    def data_diff(self):
        # Calculo da quantidade de dias
        quantidade_dias = abs((self.data_max - self.processed_date).days)
        return quantidade_dias

    def status(self):
        if self.data_diff() <= 1:
            return True
        return False

    def __str__(self):
        return self.file_name


class InsumoPromax(models.Model):
    id_file = models.ForeignKey('InsumoLog', on_delete=models.CASCADE)
    cod_unidade = models.FloatField(null=True)
    # cod_unidade = models.CharField(max_length=200, null=True)
    nom_unidade = models.CharField(max_length=200, null=True)
    nom_geo = models.CharField(max_length=200, null=True)
    dat_pedido = models.CharField(max_length=200, null=True)
    cod_produto = models.CharField(max_length=200, null=True)
    nom_produto = models.CharField(max_length=200, null=True)
    dsc_motivo = models.CharField(max_length=200, null=True)
    qtd_sku = models.CharField(max_length=200, null=True)
    dsc_canal = models.CharField(max_length=200, null=True)

    @property
    def fields(self):
        return [f.name for f in self._meta.fields + self._meta.many_to_many]

    def __str__(self):
        return self.nom_geo


class InsumoConsolidado(models.Model):
    id_file = models.ForeignKey('InsumoLog', on_delete=models.CASCADE)
    coddir = models.BigIntegerField(null=True)
    nomedir = models.CharField(max_length=200, null=True)
    codcom = models.BigIntegerField(null=True)
    nomecom = models.CharField(max_length=200, null=True)
    codfab = models.BigIntegerField(null=True)
    nomefab = models.CharField(max_length=200, null=True)
    cod_cliente = models.CharField(max_length=200, null=True)
    nomecliente = models.CharField(max_length=200, null=True)
    codpro = models.BigIntegerField(null=True)
    nomepro = models.CharField(max_length=200, null=True)
    marca = models.CharField(max_length=200, null=True)
    linemb = models.CharField(max_length=200, null=True)
    tipomarcaprod = models.CharField(max_length=200, null=True)
    semana = models.CharField(max_length=200, null=True)
    tipo_malha = models.CharField(max_length=200, null=True)
    malha = models.CharField(max_length=200, null=True)
    malhaajustada = models.CharField(max_length=200, null=True)
    real = models.CharField(max_length=200, null=True)
    comprometido = models.CharField(max_length=200, null=True)
    devolucoes = models.CharField(max_length=200, null=True)
    tendnumerica = models.CharField(max_length=200, null=True)
    tendlinear = models.CharField(max_length=200, null=True)
    dispersao = models.CharField(max_length=200, null=True)
    fatorhl = models.CharField(max_length=200, null=True)
    processed_date = models.CharField(max_length=200, null=True)
    data_puxada = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nomedir


class InsumoRastreabilidade(models.Model):
    id_file = models.ForeignKey('InsumoLog', on_delete=models.CASCADE)
    cod_tipo = models.CharField(max_length=200, null=True)
    cod_cliente = models.FloatField(null=True)
    dat_exportacao = models.CharField(max_length=200, null=True)
    dat_importacao = models.CharField(max_length=200, null=True)
    dat_aprovacao = models.CharField(max_length=200, null=True)
    dat_tratamento_pedido = models.CharField(max_length=200, null=True)
    dat_inclusao_pendencia = models.CharField(max_length=200, null=True)
    dat_puxada = models.CharField(max_length=200, null=True)
    dat_cancelamento_nf = models.CharField(max_length=200, null=True)
    etapa_g2 = models.CharField(max_length=200, null=True)
    hra_puxada = models.CharField(max_length=200, null=True)
    hra_aprovacao_pendencia = models.CharField(max_length=200, null=True)
    hra_inclusao_pendencia = models.CharField(max_length=200, null=True)
    hra_exportacao_pedido = models.CharField(max_length=200, null=True)
    hra_inclusao_pedido = models.CharField(max_length=200, null=True)
    hra_tratamento_pedido = models.CharField(max_length=200, null=True)
    cod_justificativa_bo = models.CharField(max_length=200, null=True)
    cod_justificativa_ca = models.CharField(max_length=200, null=True)
    cod_nota_fiscal = models.CharField(max_length=200, null=True)
    val_item_nota_fiscal = models.CharField(max_length=200, null=True)
    cod_produto_nf = models.CharField(max_length=200, null=True)
    val_qtd_sku_prod_nf = models.CharField(max_length=200, null=True)
    val_qtd_HL_prod_nf = models.CharField(max_length=200, null=True)
    cod_bo = models.CharField(max_length=200, null=True)
    num_carro = models.CharField(max_length=200, null=True)
    num_item = models.CharField(max_length=200, null=True)
    num_pedido = models.CharField(max_length=200, null=True)
    bln_pedido_faturado = models.CharField(max_length=200, null=True)
    cod_pendencia_pedido = models.CharField(max_length=200, null=True)
    cod_produto = models.FloatField(null=True)
    val_qtd_prod_hl = models.FloatField(null=True)
    val_qtd_prod_sku = models.FloatField(null=True)
    sgl_status_carro = models.CharField(max_length=200, null=True)
    sgl_status_item = models.CharField(max_length=200, null=True)
    dsc_tipo_cliente = models.CharField(max_length=200, null=True)
    sgl_tipo_nota_fiscal = models.CharField(max_length=200, null=True)
    cod_unb_comercial = models.CharField(max_length=200, null=True)
    cod_unb_destino = models.CharField(max_length=200, null=True)
    bln_unb_fora_malha = models.CharField(max_length=200, null=True)
    cod_unb_origem = models.CharField(max_length=200, null=True)
    cod_geo = models.CharField(max_length=200, null=True)
    sgl_tipo_canal = models.CharField(max_length=200, null=True)
    dsc_status_bo = models.CharField(max_length=200, null=True)
    dat_carregamento = models.CharField(max_length=200, null=True)
    dat_emissao_nf = models.CharField(max_length=200, null=True)
    cod_tipo_categ_bo = models.CharField(max_length=200, null=True)
    cod_tipo_subcateg_bo = models.CharField(max_length=200, null=True)
    dat_puxada_original = models.CharField(max_length=200, null=True)
    num_carro_original = models.CharField(max_length=200, null=True)
    Processed_date = models.CharField(max_length=200, null=True)
    data_puxada = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.pk)


class InsumoADHOCCUBO(models.Model):
    id_file = models.ForeignKey('InsumoLog', on_delete=models.CASCADE)
    cod_unidade = models.IntegerField(null=True, blank=True)
    nomeunidade = models.CharField(max_length=50, null=True, blank=True)
    cod_unidade_original = models.IntegerField(null=True, blank=True)
    regional = models.CharField(max_length=50, null=True, blank=True)
    cod_cliente = models.IntegerField(null=True, blank=True)
    nome_cliente = models.CharField(max_length=50, null=True, blank=True)
    geografia = models.CharField(max_length=50, null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    embalagem_fechada = models.CharField(max_length=50, null=True, blank=True)
    embalagem_aberta = models.CharField(max_length=50, null=True, blank=True)
    cod_prod = models.IntegerField(null=True, blank=True)
    nome_prod = models.CharField(max_length=50, null=True, blank=True)
    data_puxada = models.CharField(max_length=50, null=True, blank=True)
    marcacao = models.CharField(max_length=50, null=True, blank=True)
    entrega = models.CharField(max_length=50, null=True, blank=True)
    ns_gross = models.CharField(max_length=50, null=True, blank=True)
    ns_net = models.CharField(max_length=50, null=True, blank=True)
    status_Item = models.CharField(max_length=50, null=True, blank=True)
    motivo = models.CharField(max_length=50, null=True, blank=True)
    num_carro = models.IntegerField(null=True, blank=True)
    cod_justificativa = models.IntegerField(null=True, blank=True)
    justificativa = models.IntegerField(null=True, blank=True)
    cod_justificativa_bo = models.IntegerField(null=True, blank=True)
    justificativa_bo = models.CharField(max_length=100, null=True, blank=True)
    canal_de_marcacao = models.CharField(max_length=50, null=True, blank=True)
    micro_regiao = models.CharField(max_length=50, null=True, blank=True)
    abci = models.CharField(max_length=50, null=True, blank=True)
    tipo_venda = models.CharField(max_length=50, null=True, blank=True)
    entrada = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.pk)





MODELS_BY_NAME = {
    "promax": InsumoPromax,
    #"consolidado": InsumoConsolidado,
    "malha": InsumoConsolidado,
    #"rastreabilidade": InsumoRastreabilidade,
    "foto": InsumoRastreabilidade,
    "adhoc": InsumoADHOCCUBO,
    "cubo": InsumoADHOCCUBO,
    "adhoccubo": InsumoADHOCCUBO
}
