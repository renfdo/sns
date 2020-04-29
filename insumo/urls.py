from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    # SITE
    url(regex='^r/(?P<type_file>\D+)*/*(?P<date>[\d-]+)*', view=InsumoLogView.as_view(),
        name='insumo_list'),

    # Detalhes e Exportação unico para todos tipos de insumo
    path('DETAILS/<str:table>/<int:pk>', InsumoDetails.as_view(), name='insumo_details'),
    path('EXPORT/<str:table>/<int:pk>', insumo_export, name='insumo_export'),

    # API para cada tipo de insumo
    path('api/protomax/<int:pk>/', InsumoPromaxViewSet.as_view()),

    # Consolidado agora é Malha
    # path('api/consolidado/<int:pk>/', InsumoConsolidadoViewSet.as_view()),
    path('api/malha/<int:pk>/', InsumoConsolidadoViewSet.as_view()),

    # Rastreabilidade agora é foto
    # path('api/rastreabilidade/<int:pk>/', InsumoRastreabilidadeViewSet.as_view()),
    path('api/foto/<int:pk>/', InsumoRastreabilidadeViewSet.as_view()),

    path('api/adhoc/<int:pk>/', InsumoADHOCCUBOViewSet.as_view()),
    path('api/cube/<int:pk>/', InsumoADHOCCUBOViewSet.as_view()),
    path('api/adhoccube/<int:pk>/', InsumoADHOCCUBOViewSet.as_view()),


]
