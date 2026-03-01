"""
genericissuetracker.views.v1.read.attachment
============================================

Version 1 read-only endpoints for IssueAttachment.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import IssueAttachment
from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="attachment_read_list",
        tags=["Attachment"],
        summary="List attachments (read-only)",
    ),
    retrieve=extend_schema(
        operation_id="attachment_read_retrieve",
        tags=["Attachment"],
        summary="Retrieve attachment (read-only)",
    ),
)
class AttachmentReadViewSet(BaseReadOnlyViewSet):
    queryset = IssueAttachment.objects.select_related("issue").all()
    read_serializer_class = IssueAttachmentReadSerializer

    search_fields = ["original_name"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    
    lookup_field = "number"
    lookup_url_kwarg = "number"

