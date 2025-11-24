from rest_framework import serializers
from .models import Site, Link
from math import radians, sin, cos, sqrt, atan2

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["id", "name", "slug", "latitude", "longitude"]

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    dlat = radians(float(lat2) - float(lat1))
    dlon = radians(float(lon2) - float(lon1))
    a = sin(dlat/2)**2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlon/2)**2
    return round(2 * R *atan2(sqrt(a), sqrt(1 - a)), 3)

class LinkSerializer(serializers.ModelSerializer):
    site_a = serializers.SlugRelatedField(slug_field = "slug", queryset=Site.objects.all())
    site_b = serializers.SlugRelatedField(slug_field = "slug", queryset=Site.objects.all())
    km_length = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            "id", "site_a", "site_b", "frequency_ghz", "capacity_mbps", "vendor",
            "status", "km_length", "created_at"
        ]
    def get_km_length(self, obj):
        return haversine_km(
            obj.site_a.latitude, obj.site_a.longitude,
            obj.site_b.latitude, obj.site_b.longitude
        )
    def validate(self, attrs):
        a, b = attrs["site_a"], attrs["site_b"]
        if a == b: 
            raise serializers.ValidationError("site_a y site_b deben ser distintos.")
        exists = (
            Link.objects.filter(site_a=a, site_b=b).exists() or
            Link.objects.filter(site_a=b, site_b=a).exists()
        )
        if exists and (self.instance is None):
            raise serializers.ValidationError("Ya existe un enlace entre esos sitios (sin importar el orden).")
        return attrs 
