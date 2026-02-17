"""
genericissuetracker.views.v1.crud.label
=======================================

Version 1 CRUD endpoints for Label.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import Label
from genericissuetracker.serializers.v1.read.label import LabelReadSerializer
from genericissuetracker.serializers.v1.write.label import LabelCreateSerializer
from genericissuetracker.views.v1.base import BaseCRUDViewSet


class LabelCRUDViewSet(BaseCRUDViewSet):
    queryset = Label.objects.all()

    read_serializer_class = LabelReadSerializer
    write_serializer_class = LabelCreateSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()
