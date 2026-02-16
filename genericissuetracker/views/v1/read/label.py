"""
genericissuetracker.views.v1.read.label
=======================================

Version 1 read-only endpoints for Label.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import Label
from genericissuetracker.serializers.v1.read.label import LabelReadSerializer
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


class LabelReadViewSet(BaseReadOnlyViewSet):
    queryset = Label.objects.all()
    read_serializer_class = LabelReadSerializer
    permission_classes = [AllowAny]
