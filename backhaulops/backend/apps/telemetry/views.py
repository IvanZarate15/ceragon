# backend/apps/telemetry/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from bson import ObjectId
from django.utils.timezone import make_naive
from .mongo import telemetry_col, ensure_indexes
from .serializers import TelemetryEventSerializer, TelemetryQuerySerializer

def to_serializable(doc: dict) -> dict:
    """
    Transforma documentos de Mongo a JSON amigable:
    - _id de ObjectId -> str
    - ts (datetime) -> ISO 8601 (naive UTC o tu preferencia)
    """
    out = dict(doc)
    if "_id" in out and isinstance(out["_id"], ObjectId):
        out["_id"] = str(out["_id"])
    if "ts" in out:
        # DRF puede serializar aware; si prefieres naive ISO:
        try:
            out["ts"] = make_naive(out["ts"]).isoformat()
        except Exception:
            try:
                out["ts"] = out["ts"].isoformat()
            except Exception:
                pass
    return out

class TelemetryIngestView(APIView):
    """
    POST /api/telemetry/events/         -> 1 evento
    POST /api/telemetry/events/bulk/    -> lista de eventos
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ensure_indexes()  # inofensivo si ya existen
        col = telemetry_col()

        data = request.data
        # ¿bulk?
        if isinstance(data, list):
            ser = TelemetryEventSerializer(data=data, many=True)
        else:
            ser = TelemetryEventSerializer(data=data)

        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        payload = ser.validated_data
        if isinstance(payload, list):
            # Inserción en bloque
            # Aseguramos que ts sea datetime (DRF ya lo parseó)
            docs = [dict(ev) for ev in payload]
            res = col.insert_many(docs)
            return Response({"inserted_count": len(res.inserted_ids)}, status=status.HTTP_201_CREATED)
        else:
            res = col.insert_one(dict(payload))
            return Response({"inserted_id": str(res.inserted_id)}, status=status.HTTP_201_CREATED)

class TelemetryQueryView(APIView):
    """
    GET /api/telemetry/events/?device_id=...&type=...&since=...&until=...&limit=200&sort=desc
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        col = telemetry_col()
        qser = TelemetryQuerySerializer(data=request.query_params)
        qser.is_valid(raise_exception=True)
        q = qser.validated_data

        # Filtro dinámico
        filt = {}
        if "device_id" in q:
            filt["device_id"] = q["device_id"]
        if "site_slug" in q:
            filt["site_slug"] = q["site_slug"]
        if "type" in q:
            filt["type"] = q["type"]

        # Rango temporal
        if "since" in q or "until" in q:
            time_range = {}
            if "since" in q:
                time_range["$gte"] = q["since"]
            if "until" in q:
                time_range["$lte"] = q["until"]
            filt["ts"] = time_range

        # Orden/limit
        sort_dir = -1 if q.get("sort", "desc") == "desc" else 1
        limit = q.get("limit", 200)

        cursor = col.find(filt).sort("ts", sort_dir).limit(limit)
        docs = [to_serializable(d) for d in cursor]
        return Response({"count": len(docs), "results": docs}, status=status.HTTP_200_OK)
