from rest_framework import serializers
from insumo.models import InsumoLog


class InsumoLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InsumoLog
        fields = ['file_name', 'type_file','pk']

