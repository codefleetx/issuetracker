"""
genericissuetracker.views.v1.crud.comment
=========================================

Version 1 CRUD endpoints for IssueComment.

Exposes:
    • POST   /api/v1/comments/
    • DELETE /api/v1/comments/{id}/

Updates are intentionally not supported in v1.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import IssueComment
from genericissuetracker.serializers.v1.read.comment import (
    IssueCommentReadSerializer,
)
from genericissuetracker.serializers.v1.write.comment import (
    IssueCommentCreateSerializer,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


class CommentCRUDViewSet(BaseCRUDViewSet):
    queryset = IssueComment.objects.all()

    read_serializer_class = IssueCommentReadSerializer
    write_serializer_class = IssueCommentCreateSerializer

    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        instance.soft_delete()
