from rest_framework import serializers


class ReporteEsperanzaPorcentajeSerializer(serializers.Serializer):
    total_tipo = serializers.IntegerField()
    tipo_oracion = serializers.FloatField()
    tipo_lectura = serializers.FloatField()