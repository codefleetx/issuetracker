"""
genericissuetracker.views.v1.crud.attachment
============================================

Version 1 CRUD endpoints for IssueAttachment.

Exposes:
    • POST   /api/v1/attachments/
    • DELETE /api/v1/attachments/{id}/
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import IssueAttachment
from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)
from genericissuetracker.serializers.v1.write.attachment import (
    IssueAttachmentUploadSerializer,
)
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.signals import (
    attachment_added,
    attachment_deleted,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="attachment_crud_list",
        tags=["Attachment"],
        summary="List attachments (write-capable endpoint)",
    ),
    retrieve=extend_schema(
        operation_id="attachment_crud_retrieve",
        tags=["Attachment"],
        summary="Retrieve attachment (write-capable endpoint)",
    ),
    create=extend_schema(
        operation_id="attachment_create",
        tags=["Attachment"],
        summary="Upload attachment",
    ),
    destroy=extend_schema(
        operation_id="attachment_delete",
        tags=["Attachment"],
        summary="Soft delete attachment",
    ),
)
class AttachmentCRUDViewSet(BaseCRUDViewSet):
    queryset = IssueAttachment.objects.all()

    read_serializer_class = IssueAttachmentReadSerializer
    write_serializer_class = IssueAttachmentUploadSerializer

    http_method_names = ["get", "post", "delete"]
    
    lookup_field = "number"
    lookup_url_kwarg = "number"
        
    def perform_create(self, serializer):
        """
        Handle attachment upload and emit lifecycle signal.

        Emits:
            attachment_added
        """
        instance = serializer.save()

        identity = get_identity_resolver().resolve(self.request)

        attachment_added.send(
            sender=instance.__class__,
            issue=instance.issue,
            attachment=instance,
            identity=identity,
        )

    def perform_destroy(self, instance):
        """
        Soft delete attachment and emit lifecycle signal.

        Emits:
            attachment_deleted
        """
        identity = get_identity_resolver().resolve(self.request)

        instance.soft_delete()

        attachment_deleted.send(
            sender=instance.__class__,
            issue=instance.issue,
            attachment=instance,
            identity=identity,
        )