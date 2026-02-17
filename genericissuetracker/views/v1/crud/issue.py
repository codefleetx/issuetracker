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
- Permissions declared explicitly.

Mutation Scope
--------------
- Creation allowed (identity injected in serializer).
- Update allowed (restricted fields only).
- Delete performs soft delete via model.
"""

from rest_framework.permissions import AllowAny

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.issue import IssueReadSerializer
from genericissuetracker.serializers.v1.write.issue import (
    IssueCreateSerializer,
    IssueUpdateSerializer,
)
from genericissuetracker.views.v1.base import BaseCRUDViewSet


class IssueCRUDViewSet(BaseCRUDViewSet):
    """
    Write-capable ViewSet for Issue.

    Responsibilities:
        - Create issues
        - Update issues
        - Soft delete issues

    Read operations routed to IssueReadViewSet.
    """

    queryset = Issue.objects.all()

    read_serializer_class = IssueReadSerializer
    write_serializer_class = IssueCreateSerializer  # default for create

    def get_serializer_class(self):
        """
        Explicit serializer routing for create vs update.

        - create → IssueCreateSerializer
        - update/partial_update → IssueUpdateSerializer
        - destroy → IssueUpdateSerializer (no payload)
        - list/retrieve → IssueReadSerializer
        """
        if self.action == "create":
            return IssueCreateSerializer

        if self.action in ["update", "partial_update"]:
            return IssueUpdateSerializer

        if self.action in ["list", "retrieve"]:
            return self.read_serializer_class

        if self.action == "destroy":
            return IssueUpdateSerializer

        return super().get_serializer_class()

    def perform_destroy(self, instance):
        """
        Soft delete instead of hard delete.

        Delegates deletion behavior to model layer.
        """
        instance.soft_delete()
