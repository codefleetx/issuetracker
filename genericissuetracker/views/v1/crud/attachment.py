"""
genericissuetracker.views.v1.crud.attachment
============================================

Version 1 CRUD endpoints for IssueAttachment.

Exposes:
    • POST   /api/v1/attachments/
    • DELETE /api/v1/attachments/{id}/
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import IssueAttachment
from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)
from genericissuetracker.serializers.v1.write.attachment import (
    IssueAttachmentUploadSerializer,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


class AttachmentCRUDViewSet(BaseCRUDViewSet):
    queryset = IssueAttachment.objects.all()

    read_serializer_class = IssueAttachmentReadSerializer
    write_serializer_class = IssueAttachmentUploadSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()
