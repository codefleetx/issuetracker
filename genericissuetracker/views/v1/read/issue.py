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

Future Extensions
-----------------
- Filtering (Phase 4)
- Search (Phase 4)
- Ordering (Phase 4)
- Pagination (global DRF config)
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.issue import IssueReadSerializer
from genericissuetracker.views.v1.base import BaseReadOnlyViewSet


class IssueReadViewSet(BaseReadOnlyViewSet):
    """
    Read-only ViewSet for Issue.

    Responsibilities:
        - List issues
        - Retrieve issue detail

    No write operations permitted.
    """

    queryset = (
        Issue.objects
        .select_related()  # Placeholder for future relations
        .prefetch_related(
            "labels",
            "comments",
            "attachments",
        )
        .all()
    )

    read_serializer_class = IssueReadSerializer
