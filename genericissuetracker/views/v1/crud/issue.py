"""
genericissuetracker.views.v1.crud.issue
=======================================

Version 1 CRUD endpoints for Issue.

Purpose
-------
Expose write-capable endpoints:

    • POST   /api/v1/issues/
    • PUT    /api/v1/issues/{id}/
    • PATCH  /api/v1/issues/{id}/
    • DELETE /api/v1/issues/{id}/

Design Principles
-----------------
- No business logic in views.
- Deterministic serializer separation.
- Identity handling occurs in serializers.
- Soft delete handled at model layer.
- Queryset defined explicitly.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.issue import IssueReadSerializer
from genericissuetracker.serializers.v1.write.issue import (
    IssueCreateSerializer,
    IssueUpdateSerializer,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id="issue_crud_list",
        tags=["Issue"],
        summary="List issues (write-capable endpoint)",
    ),
    retrieve=extend_schema(
        operation_id="issue_crud_retrieve",
        tags=["Issue"],
        summary="Retrieve issue (write-capable endpoint)",
    ),
    create=extend_schema(
        operation_id="issue_create",
        tags=["Issue"],
        summary="Create new issue",
    ),
    update=extend_schema(
        operation_id="issue_update",
        tags=["Issue"],
        summary="Update issue",
    ),
    partial_update=extend_schema(
        operation_id="issue_partial_update",
        tags=["Issue"],
        summary="Partially update issue",
    ),
    destroy=extend_schema(
        operation_id="issue_delete",
        tags=["Issue"],
        summary="Soft delete issue",
    ),
)
class IssueCRUDViewSet(BaseCRUDViewSet):
    """
    Write-capable ViewSet for Issue.

    Responsibilities:
        - Create issues
        - Update issues
        - Soft delete issues

    Read operations are also available here,
    but a dedicated read-only ViewSet exists
    for strict architectural separation.
    """

    queryset = Issue.objects.all()

    read_serializer_class = IssueReadSerializer
    write_serializer_class = IssueCreateSerializer
    lookup_field = "issue_number"
    lookup_url_kwarg = "issue_number"


    # ------------------------------------------------------------------
    # Serializer Routing
    # ------------------------------------------------------------------
    def get_serializer_class(self):
        if self.action == "create":
            return IssueCreateSerializer

        if self.action in ["update", "partial_update"]:
            return IssueUpdateSerializer

        if self.action in ["list", "retrieve"]:
            return self.read_serializer_class

        if self.action == "destroy":
            return IssueUpdateSerializer

        return super().get_serializer_class()

    # ------------------------------------------------------------------
    # Soft Delete Handling
    # ------------------------------------------------------------------
    def perform_destroy(self, instance):
        instance.soft_delete()
