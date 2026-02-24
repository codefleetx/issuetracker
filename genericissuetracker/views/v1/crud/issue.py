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
from rest_framework import status as drf_status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.issue import IssueReadSerializer
from genericissuetracker.serializers.v1.write.issue import (
    IssueCreateSerializer,
    IssueUpdateSerializer,
)
from genericissuetracker.serializers.v1.write.status import (
    IssueStatusUpdateSerializer,
)
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.services.issue_lifecycle import change_issue_status
from genericissuetracker.signals import (
    issue_updated,
    issue_deleted,
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
    lookup_url_kwarg = "pk"

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    # ------------------------------------------------------------------
    # Serializer Routing
    # ------------------------------------------------------------------
    def get_serializer_class(self):
        if self.action == "create":
            return IssueCreateSerializer

        if self.action in ["update", "partial_update"]:
            return IssueUpdateSerializer

        if self.action == "destroy":
            return IssueUpdateSerializer

        if self.action == "change_status":
            return IssueStatusUpdateSerializer

        return super().get_serializer_class()

    # ------------------------------------------------------------------
    # Permission Routing
    # ------------------------------------------------------------------
    def get_permissions(self):
        """
        Permission Rules:

        - Anyone can CREATE
        - Only authenticated users can UPDATE or DELETE
        - Read behavior follows default permission configuration
        """

        if self.action == "create":
            return [AllowAny()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated()]

        return super().get_permissions()

    # ------------------------------------------------------------------
    # Update Handling (Signal Emission Added)
    # ------------------------------------------------------------------
    def perform_update(self, serializer):
        instance = serializer.save()

        identity = get_identity_resolver().resolve(self.request)

        issue_updated.send(
            sender=self.__class__,
            issue=instance,
            identity=identity,
        )

    # ------------------------------------------------------------------
    # Soft Delete Handling (Signal Emission Added)
    # ------------------------------------------------------------------
    def perform_destroy(self, instance):
        identity = get_identity_resolver().resolve(self.request)

        instance.soft_delete()

        issue_deleted.send(
            sender=self.__class__,
            issue=instance,
            identity=identity,
        )

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    # ------------------------------------------------------------------
    # Status Transition (Lifecycle Engine)
    # ------------------------------------------------------------------
    @action(detail=True, methods=["post"], url_path="change-status")
    def change_status(self, request, pk=None):
        """
        Change issue status using lifecycle service.

        Delegates:
            - Transition validation
            - Policy enforcement
            - Atomic DB update
            - Status history creation
            - Signal dispatch
        """

        issue = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        identity = get_identity_resolver().resolve(request)

        change_issue_status(issue, new_status, identity)

        return Response(
            {"detail": "Status updated successfully."},
            status=drf_status.HTTP_200_OK,
        )