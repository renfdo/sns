from django.views import generic
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from sns_project.ultils import CSVExportView
from datetime import datetime
from rest_framework import viewsets, generics
from .serializers import InsumoConsolidadoSerializer, InsumoPromaxSerializer, InsumoRastreabilidadeSerializer, InsumoADHOCCUBOSerializer
from .models import InsumoLog, InsumoPromax, InsumoConsolidado, InsumoRastreabilidade, InsumoADHOCCUBO, MODELS_BY_NAME
from .tables import TABLES
import json, csv, copy


class InsumoLogView(generic.TemplateView):
    template_name = 'insumo/insumo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        insumo_manager = InsumoLog
        context['insumos'] = None

        url = {
            'type_file': '',
            'date': '',
        }

        if self.kwargs['type_file']:
            type_file = self.kwargs['type_file'].replace('/', '')
        else:
            context['insumos'] = None
            context['insumos'] = insumo_manager.manager_objects.get_type_files()
            context['url'] = url
            return context

        if self.kwargs['date']:
            context['insumos'] = None
            date_p = str(self.kwargs['date'].replace('/', ''))

            url['type_file'] = type_file
            url['date'] = date_p
            context['url'] = url

            data_puxada = date_p.split('-')
            data = datetime(int(data_puxada[0]), int(data_puxada[1]), int(data_puxada[2]))

            context['insumos'] = insumo_manager.manager_objects.get_files(type_file, data)
            print(context['insumos'])
            return context

        url['type_file'] = type_file
        context['url'] = url
        context['insumos'] = insumo_manager.manager_objects.get_dates(type_file)

        return context


class InsumoPromaxViewSet(generics.ListAPIView):
    serializer_class = InsumoPromaxSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return InsumoPromax.objects.filter(id_file=pk)


class InsumoConsolidadoViewSet(generics.ListAPIView):
    serializer_class = InsumoConsolidadoSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return InsumoConsolidado.objects.filter(id_file=pk)


class InsumoRastreabilidadeViewSet(generics.ListAPIView):
    serializer_class = InsumoRastreabilidadeSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return InsumoRastreabilidade.objects.filter(id_file=pk)


class InsumoADHOCCUBOViewSet(generics.ListAPIView):
    serializer_class = InsumoADHOCCUBOSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return InsumoADHOCCUBO.objects.filter(id_file=pk)


class InsumoDetails(generic.TemplateView):
    template_name = 'insumo/insumo_promax_details.html'

    def get_context_data(self, **kwargs):
        insumo = get_object_or_404(InsumoLog, pk=self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        tablename = self.kwargs.get("table", "").lower()
        tabledata = TABLES[tablename]
        tabledatajson = json.dumps(tabledata)
        tabledatajson = tabledatajson.replace('{id}', str(insumo.pk))
        context['tabledatajson'] = tabledatajson
        context['type_file'] = insumo.type_file
        context['processed_date'] = insumo.processed_date.strftime("%Y-%m-%d")
        context['file_name'] = insumo.file_name
        return context

    def get_queryset(self):
        return self.queryset.filter(id_file=self.kwargs.get('pk'))


# StreamingHttpResponse requires a File-like class that has a 'write' method
class Echo(object):
    def write(self, value):
        return value

def gen_insumo_export(queryset, columns):
    buffer = Echo()
    delimiter = ";"
    writer = csv.DictWriter(buffer, fieldnames=columns, delimiter=delimiter)
    yield buffer.write(delimiter.join(columns) + "\r\n")

    for item in queryset:
        r = {}
        for c in columns:
            r[c] = getattr(item, c, "")
        yield writer.writerow(r)


def insumo_export(request, table, pk):
    insumo = get_object_or_404(InsumoLog, pk=pk)
    tablename = table.lower()
    tabledata = TABLES[tablename]
    tablecolumns = list(map(lambda x: x["data"], tabledata["columns"]))
    queryset = MODELS_BY_NAME[tablename].objects.filter(id_file=pk)
    response = StreamingHttpResponse(gen_insumo_export(queryset, tablecolumns), content_type="text/csv")
    filename = insumo.file_name
    if filename.split(".")[-1] != "csv":
        filename = filename + ".csv"
    response['Content-Disposition'] = 'attachment;filename=' + filename
    return response



