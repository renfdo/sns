from django import forms

from .models import JusfiticativaBo, JusfiticativaCa, SaidaSns, ParametrosSNSRule

from bootstrap_modal_forms.forms import BSModalForm


# JUSTIFICATIVA BO
class JustificativaBoForm(BSModalForm):
    class Meta:
        model = JusfiticativaBo
        # TODO: Incluir os demais campos do Model no Form (Django)
        labels = {
            "val_flag_indisp": "Indisponibilidade",
            "cod_justificativa": "Código da Justificativa",
            "dsc_justificativa": "Justificativa",
        }
        exclude = [
            "data_inclusao",
            "data_alteracao",
        ]


# JUSTIFICATIVA CA
class JustificativaCaForm(BSModalForm):
    class Meta:
        model = JusfiticativaCa
        labels = {
            "cod_justificativa": "Código da Justificativa",
            "cod_tipo_justificativa": "Código Tipo Justificativa",
            "dsc_justificativa": "Justificativa",
            "ind_automatica": "Indisponibilidade Automática",
            "ind_cancelamento": "Indisponibilidade Cancelamento",
            "val_flag_indisp ": "Indisponibilidade",
            "cod_motivo ": "Motivo",
        }
        exclude = [
            "data_inclusao",
            "data_alteracao",
        ]


# OUTPUT SNS
class DateInput(forms.DateInput):
    input_type = 'date'


class SaidaSnsForm(forms.ModelForm):

    # TODO: Traduzir nomes para o ingles?
    start_date = forms.DateField(widget=DateInput(format='%d/%m/%Y'), label='Data Inicial')
    end_date = forms.DateField(widget=DateInput(format='%d/%m/%Y'), label='Data Final')

    class Meta:
        model = SaidaSns
        fields = [
            # "liquid_type",
            # "input_type",
            # "channel_type",
            "liquido",
        ]
        labels = {
            "liquido": "Tipo de Líquido",
            # "input_type": "Tipo de Insumo",
            # "channel_type": "Tipo de Canal",
            "start_date": "Data Inicial",
            "end_date": "Data Final",
        }


# PROCESSAMENTO MANUAL
class ProcessamentoManualForm(forms.Form):
    data_proc_manual = forms.DateField(widget=DateInput(format='%d/%m/%Y'), label='Data Processamento')


class SNSRule(forms.ModelForm):

    class Meta:
        model = ParametrosSNSRule
        exclude = [
            "data_insert",
        ]


class SNSRules(forms.Form):

    rateio = forms.CharField(label="Rateio", required=False)
    value_rateio = forms.IntegerField(label="Parâmetro", min_value=0, required=True, initial=0)
    is_active_rateio = forms.BooleanField(label="Ativo",  initial=True, required=False)

    volta = forms.CharField(label="Volta da Perna", required=False)
    value_volta = forms.IntegerField(label="Parâmetro", min_value=0, required=True, initial=0)
    is_active_volta = forms.BooleanField(label="Ativo", initial=True, required=False)

    alocacao = forms.CharField(label="Alocação Normal", required=False)
    value_alocacao = forms.IntegerField(label="Parâmetro", min_value=0, required=True, initial=0)
    is_active_alocacao = forms.BooleanField(label="Ativo", initial=True, required=False)

    mto = forms.CharField(label="MTO", required=False)
    value_mto = forms.IntegerField(label="Parâmetro", min_value=0, required=True, initial=0)
    is_active_mto = forms.BooleanField(label="Ativo", initial=True, required=False)


