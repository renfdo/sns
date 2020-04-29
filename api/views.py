from sns.models import LogProcessoBatch, ParametrosSNSRule
from django.views.decorators.http import condition
from concurrent.futures import ThreadPoolExecutor
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse, FileResponse
from .serializers import InsumoLogSerializer
from rest_framework.response import Response
from sns_flow.SnsFlow import SnsFlow
from django.http import HttpResponse
from rest_framework import viewsets
from insumo.models import InsumoLog
from django.db import connection
from datetime import datetime
from .bd import sns_to_sql
import django.db as d
import numpy as np
import platform
import timeit
import csv
import time
import os
from django.shortcuts import redirect


@api_view()
def output(request, date=None):
    if LogProcessoBatch.objects.is_running():
    # if False:
        return Response({"message": "Processo já esta em execução"}, 503)
    else:
        response = StreamingHttpResponse(stream_process_as_is(request, date), content_type='text/html')
        return response


@condition(etag_func=None)
def sleep(request):
    x = StreamingHttpResponse(downloader(request), content_type='text/html')
    return x


def download(request):
    return FileResponse(open('data/saida.csv', 'rb'), filename='output.csv')


def downloader(request):
    # TODO: melhorar esse replace ae
    url_redirect = "{}{}".format(
                                request.build_absolute_uri('').replace(redirect('sleep').url, ""),
                                redirect('download').url)

    print(url_redirect)
    yield "<html><body>\n"
    for x in range(1,5):
        print(f"opa {x}")
        yield f"<div>{x} seconds</div>\n"
        time.sleep(1)
    # yield f'<script>location.replace("{url_redirect}")</script>'
    yield "</body></html>\n"


def stream_process_as_is(request, date):
    '''
    :param request: requisição web
    :param date: data do processamento
    :return: a ideia era de fato retornar o CSV, mas por complicações não pude deixar assim
    :OBS: O pandas processa por bastante tempo e sem retornar nada, maior que o valor
    limite do Azure appservice (não alteravel). então tive que retonar um html com alguma informação para a conexão
    não morrer :-(. Assim q eu termino o processo do pandas (sns_flow) eu salvo o csv e redireciono via JAVACRIPT
    para uma outra URL que vai baixar. O STREAMING que é usado nesse metodo também não deixa eu redirecionar
    via server 302. Tudo uma gambiarra :-(
    '''
    # TODO: melhorar esse replace ae
    # redireciona manualmente via javascript para a página de dowload CSV
    url_redirect = "{}{}".format(
        request.build_absolute_uri('').replace(redirect('output').url, ""),
        redirect('download').url)

    yield "<html><body>\n"
    with ThreadPoolExecutor(max_workers=5) as executor:
        seconds = 1
        futures = executor.submit(run_proc_manual, date)
        while futures.running():
            yield f"<div>{seconds} seconds</div>\n"
            time.sleep(1)
            seconds = seconds + 1

        yield f"{seconds} seconds, thread finished"
        # dt = futures.result()
        # dt = dt.replace(np.nan, '', regex=True)
        # dt.to_csv("temp/saida.csv")
        yield f'<script>location.replace("{url_redirect}")</script>'
        yield "</body></html>\n"


@api_view()
def settings(request):
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
    mem_gib = mem_bytes / (1024. ** 3)  # e.g. 3.74

    info = {
        "Machine": platform.machine(),
        "Version": platform.version(),
        "Platform": platform.platform(),
        "Uname": platform.uname(),
        "System": platform.system(),
        "Processor": platform.processor(),
        "Memory": mem_gib,
    }

    return Response(info)


def run_proc_manual(date=None):
    start = timeit.default_timer()

    a = LogProcessoBatch(status='EXECUCAO', mensagem="Processo Iniciado")
    a.save()
    print("Processo iniciado")

    # chamada do proecesso batch
    print("Chamada do proecesso batch")

    # Preciso fechar todas as conexões, pois se ficar aberto por muito tempo, da erro
    output = exec_flow(date)
    d.connections.close_all()

    print("Atualizando base")
    a = LogProcessoBatch.objects.all().filter(pk=a.pk)[0]
    print(a)
    a.status = 'FINALIZADO'
    a.mensagem = 'Processo finalizado com sucesso'

    a.data_fim = datetime.now()
    a.save()
    print("Fim do processo")

    # Stop time
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    output.to_csv("data/saida.csv")
    # return output


def exec_flow(date=None):
    if date is None:
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    config = {
        'rules': ParametrosSNSRule.manager_objects.to_dict(),
        'connection': {
            'host': connection.settings_dict['HOST'],
            'db': connection.settings_dict['NAME'],
            'user': connection.settings_dict['USER'],
            'password': connection.settings_dict['PASSWORD'],
        }
    }

    flow = SnsFlow()
    flow = flow.run(load_date=date, config=config)

    # armazena a saida do processamento no banco
    sns_to_sql(flow)

    return flow


def dt_to_csv(dt):
    dt = dt.replace(np.nan, '', regex=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ' attachment ; filename = "OutputSNS.csv"'

    writer = csv.writer(response, delimiter=',')
    cols = dt.columns
    writer.writerow(cols)

    for idx, row in dt.iterrows():
        writer.writerow([row[col] for col in cols])

    return response


class InsumoLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = InsumoLog.objects.all()
    serializer_class = InsumoLogSerializer

