"""
genericissuetracker.views.v1.read.comment
=========================================

Version 1 read-only endpoints for IssueComment.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import IssueComment
from genericissuetracker.serializers.v1.read.comment import (
    IssueCommentReadSerializer,
)
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="comment_read_list",
        tags=["Comment"],
        summary="List comments (read-only)",
    ),
    retrieve=extend_schema(
        operation_id="comment_read_retrieve",
        tags=["Comment"],
        summary="Retrieve comment (read-only)",
    ),
)
class CommentReadViewSet(BaseReadOnlyViewSet):
    queryset = IssueComment.objects.select_related("issue").all()
    read_serializer_class = IssueCommentReadSerializer

    search_fields = ["body", "commenter_email"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    
    lookup_field = "number"
    lookup_url_kwarg = "number"
