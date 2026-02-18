"""
genericissuetracker.views.v1.read.issue
=======================================

Version 1 read-only endpoints for Issue.

Purpose
-------
Expose read-only access to issues:

    • GET /api/v1/issues/
    • GET /api/v1/issues/{id}/

Design Principles
-----------------
- No mutation allowed.
- No business logic in views.
- Deterministic serializer usage.
- Queryset defined explicitly.
- Soft-deleted records excluded via model manager.
- Prefetch related objects for performance.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.issue import IssueReadSerializer
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="issue_read_list",
        tags=["Issue"],
        summary="List issues (read-only)",
    ),
    retrieve=extend_schema(
        operation_id="issue_read_retrieve",
        tags=["Issue"],
        summary="Retrieve issue (read-only)",
    ),
)
class IssueReadViewSet(BaseReadOnlyViewSet):
    """
    Read-only ViewSet for Issue.

    Responsibilities:
        - List issues
        - Retrieve issue detail
    """

    search_fields = ["title", "description", "reporter_email"]
    ordering_fields = ["created_at", "updated_at", "priority"]
    ordering = ["-created_at"]

    queryset = (
        Issue.objects
        .prefetch_related(
            "labels",
            "comments",
            "attachments",
        )
        .all()
    )

    read_serializer_class = IssueReadSerializer
