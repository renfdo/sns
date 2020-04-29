from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views import View
from django.db.models import Q
from django.forms.models import model_to_dict
from .models import JusfiticativaBo, JusfiticativaCa, LogProcessoBatch
from insumo.models import InsumoLog
from .models import SaidaSns as mSaidaSns, ParametrosSNSRule
from .forms import JustificativaBoForm, JustificativaCaForm, SaidaSnsForm, SNSRules, SNSRule
from .forms import ProcessamentoManualForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView, BSModalReadView
from datetime import datetime
import csv
from api.views import output



# SITE
class Index(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        self.context['batch_log'] = LogProcessoBatch.objects.order_by("-data_inicio")[:10]
        self.context['insumos_log'] = InsumoLog.objects.order_by("-processed_date")[:10]

        return render(request, self.template_name, context=self.context)


# JUSTIFICATIVA BO
class JustificativaBOList(generic.ListView):
    model = JusfiticativaBo
    context_object_name = 'justificativasbo'
    template_name = 'justificativa_bo_list.html'


class JustificativaBOView(BSModalReadView):
    model = JusfiticativaBo


class JustificativaBOCreate(BSModalCreateView):
    template_name = 'justificativa_bo_create.html'
    form_class = JustificativaBoForm
    success_message = 'BO criado com sucesso'
    success_url = reverse_lazy('justificativa_bo_list')


class JustificativaBODelete(BSModalDeleteView):
    model = JusfiticativaBo
    template_name = 'justificativa_bo_delete_confirm.html'
    success_message = 'BO deletado com sucesso.'
    success_url = reverse_lazy('justificativa_bo_list')


class JustificativaBOUpdate(BSModalUpdateView):
    model = JusfiticativaBo
    template_name = 'justificativa_bo_update.html'
    form_class = JustificativaBoForm
    success_message = 'BO Alterado com sucesso'
    success_url = reverse_lazy('justificativa_bo_list')


# JUSTIFICATIVA CA
class JustificativaCAList(generic.ListView):
    model = JusfiticativaCa
    context_object_name = 'justificativasca'
    template_name = 'justificativa_ca_list.html'


class JustificativaCACreate(BSModalCreateView):
    template_name = 'justificativa_ca_create.html'
    form_class = JustificativaCaForm
    success_message = 'CA criado com sucesso'
    success_url = reverse_lazy('justificativa_ca_list')


class JustificativaCADelete(BSModalDeleteView):
    model = JusfiticativaCa
    template_name = 'justificativa_ca_delete_confirm.html'
    success_message = 'CA deletado com sucesso.'
    success_url = reverse_lazy('justificativa_ca_list')


class JustificativaCAUpdate(BSModalUpdateView):
    model = JusfiticativaCa
    template_name = 'justificativa_ca_update.html'
    form_class = JustificativaCaForm
    success_message = 'BO Alterado com sucesso'
    success_url = reverse_lazy('justificativa_ca_list')


# OUTPUT SNS
# TODO: Traduzir para o ingles?
class SaidaSns(generic.FormView):
    form_class = SaidaSnsForm
    initial = {'key': 'value'}
    template_name = 'saidasns.html'
    success_url = '/saidasns'

    def form_valid(self, form):

        if form.cleaned_data['liquido'] == 'TODOS':
            items = mSaidaSns.objects.filter(
                # channel_type=form.cleaned_data['channel_type'],
                # input_type=form.cleaned_data['input_type'],
                dat_original__range=(form.cleaned_data['start_date'], form.cleaned_data['end_date']))
        else:
            items = mSaidaSns.objects.filter(
                # Q(liquido=form.cleaned_data['liquido']) | Q(liquido__contains=''),
                liquido=form.cleaned_data['liquido'],
                # channel_type=form.cleaned_data['channel_type'],
                # input_type=form.cleaned_data['input_type'],
                dat_original__range=(form.cleaned_data['start_date'], form.cleaned_data['end_date']))

        colunas = []
        for field in mSaidaSns._meta.get_fields():
            if field.name in ["id", "id_file"]:
                continue
            colunas.append(field.name)

        response = HttpResponse(content_type='text/csv')
        response = StreamingHttpResponse(gen_saidasns_export(items, colunas), content_type="text/csv")
        response['Content-Disposition'] = ' attachment ; filename = "OutputSNS.csv"'
        return response


# StreamingHttpResponse requires a File-like class that has a 'write' method
class Echo(object):
    def write(self, value):
        return value


def gen_saidasns_export(queryset, columns):
    buffer = Echo()
    delimiter = ";"
    writer = csv.DictWriter(buffer, fieldnames=columns, delimiter=delimiter)
    yield buffer.write(delimiter.join(columns) + "\r\n")

    for item in queryset:
        r = {}
        for c in columns:
            r[c] = getattr(item, c, "")
        yield writer.writerow(r)


# PROCESSAMENTO MANUAL
class ProcessamentoManual(generic.View):
    form_class = ProcessamentoManualForm
    # initial = {'key': 'value'}
    template_name = 'processamento_manual.html'
    success_url = 'processamento_manual'
    context = {}

    def get(self, request):
        self.context['form'] = ProcessamentoManualForm

        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            dt_proc = datetime.strftime(form.cleaned_data["data_proc_manual"], "%Y-%m-%d")

            return redirect('output',dt_proc)

        self.context['form'] = form
        return render(request, self.template_name, self.context)


# RULES
class Rules(generic.View):
    form_class = SNSRules
    template_name = 'rules/rules_create.html'
    success_url = '/parameters'
    context = {}

    def get(self, request):
        self.context['form'] = SNSRules

        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            value_rateio = 0 if form.cleaned_data['value_rateio'] is None else form.cleaned_data['value_rateio']
            value_volta = 0 if form.cleaned_data['value_volta'] is None else form.cleaned_data['value_volta']
            value_alocacao = 0 if form.cleaned_data['value_alocacao'] is None else form.cleaned_data['value_alocacao']
            value_mto = 0 if form.cleaned_data['value_mto'] is None else form.cleaned_data['value_mto']

            rateio = ParametrosSNSRule(rule='RATEIO',
                                       value=value_rateio,
                                       is_active=form.cleaned_data['is_active_rateio']
                                       )
            volta_da_perna = ParametrosSNSRule(rule='VOLTA_DA_PERNA',
                                               value=value_volta,
                                               is_active=form.cleaned_data['is_active_volta'])

            alocacao_normal = ParametrosSNSRule(rule='ALOCACAO_NORMAL',
                                                value=value_alocacao,
                                                is_active=form.cleaned_data['is_active_alocacao'])

            mto = ParametrosSNSRule(rule='MTO',
                                                value=value_mto,
                                                is_active=form.cleaned_data['is_active_mto'])

            rateio.save()
            volta_da_perna.save()
            alocacao_normal.save()
            mto.save()
            return HttpResponseRedirect(reverse('parameters_list'))

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class ParameterRulesList(generic.ListView):
    model = ParametrosSNSRule
    context_object_name = 'parameters'
    template_name = 'rules/parameter_rules_list.html'
    queryset = model.objects.all()

    def get_queryset(self):
        self.model.manager_objects.get_last_rules()

        return self.model.manager_objects.get_last_rules()

