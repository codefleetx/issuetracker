"""
genericissuetracker.views.v1.read.comment
=========================================

Version 1 read-only endpoints for IssueComment.

Exposes:
    • GET /api/v1/comments/
    • GET /api/v1/comments/{id}/

Design:
- No mutation.
- Deterministic serializer usage.
- Soft delete respected.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import IssueComment
from genericissuetracker.serializers.v1.read.comment import (
    IssueCommentReadSerializer,
)
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


class CommentReadViewSet(BaseReadOnlyViewSet):
    queryset = IssueComment.objects.select_related("issue").all()
    read_serializer_class = IssueCommentReadSerializer
    permission_classes = [AllowAny]
