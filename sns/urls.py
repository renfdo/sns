from django.urls import path
from .views import *

urlpatterns = [
    # SITE
    path('', Index.as_view(), name='index'),
    # JUSTIFICATIVA BO
    path('justificativa_bo_list', JustificativaBOList.as_view(), name='justificativa_bo_list'),
    path('justificativa_bo_create', JustificativaBOCreate.as_view(), name='justificativa_bo_create'),
    path('justificativa_bo_update/<int:pk>/', JustificativaBOUpdate.as_view(), name='justificativa_bo_update'),
    path('justificativa_bo_delete/<int:pk>/', JustificativaBODelete.as_view(), name='justificativa_bo_delete'),
    # JUSTIFICATIVA CA
    path('justificativa_ca_list', JustificativaCAList.as_view(), name='justificativa_ca_list'),
    path('justificativa_ca_create', JustificativaCACreate.as_view(), name='justificativa_ca_create'),
    path('justificativa_ca_update/<int:pk>/', JustificativaCAUpdate.as_view(), name='justificativa_ca_update'),
    path('justificativa_ca_delete/<int:pk>/', JustificativaCADelete.as_view(), name='justificativa_ca_delete'),
    # OUTPUT SNS
    # TODO: Traduzir nomes para o ingles?
    path('saidasns', SaidaSns.as_view(), name='saidasns'),

    path('parameters_create', Rules.as_view(), name='parameters_create'),
    path('parameters', ParameterRulesList.as_view(), name='parameters_list'),
    # PROCESSAMENTO MANUAL
    path('processamento_manual', ProcessamentoManual.as_view(), name='processamento_manual'),
]
