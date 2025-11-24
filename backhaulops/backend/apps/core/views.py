from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from .models import Site, Link
from .serializers import SiteSerializer, LinkSerializer

class SiteViewSet(ModelViewSet):
    queryset = Site.objects.all().order_by("name")
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [ "name", "slug"]

class LinkViewSet(ModelViewSet):
    queryset = (Link.objects
                .select_related("site_a", "site_b")
                .all()
                .order_by("-created_at"))
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["vendor", "status", "frequency_ghz"]
    search_fields = ["site_a__name", "site_b__name", "site_a__slug", "site_b__slug"]
    ordering_fields = ["capacity_mbps", "frequency_ghz", "created_at"]
