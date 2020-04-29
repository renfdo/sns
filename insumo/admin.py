from django.contrib import admin
from .models import InsumoLog, InsumoPromax, InsumoConsolidado, InsumoRastreabilidade


admin.site.register(InsumoLog)
admin.site.register(InsumoPromax)
admin.site.register(InsumoConsolidado)
admin.site.register(InsumoRastreabilidade)