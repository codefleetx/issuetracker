"""
genericissuetracker.views.v1.read.attachment
============================================

Version 1 read-only endpoints for IssueAttachment.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import IssueAttachment
from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


class AttachmentReadViewSet(BaseReadOnlyViewSet):
    queryset = IssueAttachment.objects.select_related("issue").all()
    read_serializer_class = IssueAttachmentReadSerializer
