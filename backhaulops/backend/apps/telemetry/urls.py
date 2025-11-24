# backend/apps/telemetry/urls.py
from django.urls import path
from .views import TelemetryIngestView, TelemetryQueryView, \
                   # ya tenías ping si lo quieres mantener:
                   # ping

urlpatterns = [
    # path("ping/", ping, name="telemetry-ping"),
    path("events/", TelemetryIngestView.as_view(), name="telemetry-ingest"),
    path("events/bulk/", TelemetryIngestView.as_view(), name="telemetry-ingest-bulk"),
    path("events/query/", TelemetryQueryView.as_view(), name="telemetry-query"),
]
