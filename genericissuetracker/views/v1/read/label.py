"""
genericissuetracker.views.v1.read.label
=======================================

Version 1 read-only endpoints for Label.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import Label
from genericissuetracker.serializers.v1.read.label import LabelReadSerializer
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="label_read_list",
        tags=["Label"],
        summary="List labels (read-only)",
    ),
    retrieve=extend_schema(
        operation_id="label_read_retrieve",
        tags=["Label"],
        summary="Retrieve label (read-only)",
    ),
)
class LabelReadViewSet(BaseReadOnlyViewSet):
    queryset = Label.objects.all()
    read_serializer_class = LabelReadSerializer

    search_fields = ["name", "slug"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
