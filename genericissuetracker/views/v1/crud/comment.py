"""
genericissuetracker.views.v1.crud.comment
=========================================

Version 1 CRUD endpoints for IssueComment.

Exposes:
    • POST   /api/v1/comments/
    • DELETE /api/v1/comments/{id}/
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import IssueComment
from genericissuetracker.serializers.v1.read.comment import (
    IssueCommentReadSerializer,
)
from genericissuetracker.serializers.v1.write.comment import (
    IssueCommentCreateSerializer,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="comment_crud_list",
        tags=["Comment"],
        summary="List comments (write-capable endpoint)",
    ),
    retrieve=extend_schema(
        operation_id="comment_crud_retrieve",
        tags=["Comment"],
        summary="Retrieve comment (write-capable endpoint)",
    ),
    create=extend_schema(
        operation_id="comment_create",
        tags=["Comment"],
        summary="Create comment",
    ),
    destroy=extend_schema(
        operation_id="comment_delete",
        tags=["Comment"],
        summary="Soft delete comment",
    ),
)
class CommentCRUDViewSet(BaseCRUDViewSet):
    queryset = IssueComment.objects.all()

    read_serializer_class = IssueCommentReadSerializer
    write_serializer_class = IssueCommentCreateSerializer
    
    http_method_names = ["get", "post", "delete"]

    def perform_destroy(self, instance):
        instance.soft_delete()
