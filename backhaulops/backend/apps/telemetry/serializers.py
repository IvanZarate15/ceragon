# backend/apps/telemetry/serializers.py
from rest_framework import serializers

class TelemetryEventSerializer(serializers.Serializer):
    """
    Esquema base de un evento de telemetría (NoSQL).
    No es ModelSerializer porque no usamos ORM.
    """
    device_id = serializers.CharField(max_length=64)
    site_slug = serializers.CharField(max_length=128)
    type = serializers.ChoiceField(choices=[
        ("CURRENT", "CURRENT"),
        ("TEMPERATURE", "TEMPERATURE"),
        ("PRESSURE", "PRESSURE"),
        ("HUMIDITY", "HUMIDITY"),
        ("ALTITUDE", "ALTITUDE"),
        ("BATTERY", "BATTERY"),
        ("ALARM", "ALARM"),
        ("HEALTH", "HEALTH"),
    ])
    value = serializers.FloatField()
    unit = serializers.CharField(max_length=16, required=False, allow_blank=True)  
    ts = serializers.DateTimeField() 
    metadata = serializers.DictField(required=False)  

class TelemetryQuerySerializer(serializers.Serializer):
    """
    Valida parámetros de consulta vía querystring.
    """
    device_id = serializers.CharField(max_length=64, required=False)
    site_slug = serializers.CharField(max_length=128, required=False)
    type = serializers.CharField(max_length=32, required=False)
    since = serializers.DateTimeField(required=False)  
    until = serializers.DateTimeField(required=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=1000, default=200)
    sort = serializers.ChoiceField(choices=[("asc","asc"),("desc","desc")], required=False, default="desc")
