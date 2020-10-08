from rest_framework import serializers

from .models import UtData, AreaEn

class AreaEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaEn
        fields = ('area_id','area_code', 'area_name')

class UtDataSerializer(serializers.ModelSerializer):
    area = AreaEnSerializer()
    data_value= serializers.DecimalField(max_digits=255, decimal_places=2)
    class Meta:
        model = UtData
        fields = ('data_id', 'area' ,'data_value')