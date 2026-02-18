"""
genericissuetracker.views.v1.crud.label
=======================================

Version 1 CRUD endpoints for Label.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import Label
from genericissuetracker.serializers.v1.read.label import LabelReadSerializer
from genericissuetracker.serializers.v1.write.label import LabelCreateSerializer
from genericissuetracker.views.v1.base import BaseCRUDViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="label_crud_list",
        tags=["Label"],
        summary="List labels (write-capable endpoint)",
    ),
    retrieve=extend_schema(
        operation_id="label_crud_retrieve",
        tags=["Label"],
        summary="Retrieve label (write-capable endpoint)",
    ),
    create=extend_schema(
        operation_id="label_create",
        tags=["Label"],
        summary="Create label",
    ),
    destroy=extend_schema(
        operation_id="label_delete",
        tags=["Label"],
        summary="Soft delete label",
    ),
)
class LabelCRUDViewSet(BaseCRUDViewSet):
    queryset = Label.objects.all()

    read_serializer_class = LabelReadSerializer
    write_serializer_class = LabelCreateSerializer
    
    http_method_names = ["get", "post", "delete"]

    def perform_destroy(self, instance):
        instance.soft_delete()
