"""
genericissuetracker.serializers.base.issue
==========================================

Base serializer logic for Issue write operations.

Purpose
-------
This module centralizes shared validation and mutation logic
for Issue creation and updates.

Why This Exists
---------------
To avoid duplication across:

    • IssueCreateSerializer
    • IssueUpdateSerializer

Responsibilities
----------------
- Enforce anonymous reporting rules
- Inject identity (reporter_user_id / reporter_email)
- Prevent client-controlled identity injection
- Validate status transitions (basic guard)
- Maintain deterministic schema

Important
---------
This serializer:
    • Must not contain view logic
    • Must not emit signals (handled later in service layer)
    • Must not dynamically change fields
"""

from typing import Any, Dict

from rest_framework import serializers

from genericissuetracker.models import Issue, IssueStatus
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting


class BaseIssueWriteSerializer(serializers.ModelSerializer):
    """
    Abstract base write serializer for Issue.

    Provides shared validation logic for create/update operations.
    """

    class Meta:
        model = Issue
        fields = [
            "issue_number",
            "title",
            "description",
            "status",
            "priority",
            "is_public",
        ]
        read_only_fields = ["status"]  # Status changes controlled separately

    # ------------------------------------------------------------------
    # VALIDATION: STATUS TRANSITION GUARD
    # ------------------------------------------------------------------
    def validate_status(self, value: str) -> str:
        """
        Prevent invalid direct status manipulation during creation.

        Rules:
            - On create: status must be OPEN.
            - On update: transition rules enforced later (TODO).

        This prevents clients from creating issues directly as CLOSED.
        """
        if self.instance is None and value != IssueStatus.OPEN:
            raise serializers.ValidationError(
                "New issues must be created with status OPEN."
            )

        return value

    # ------------------------------------------------------------------
    # VALIDATION: IDENTITY ENFORCEMENT
    # ------------------------------------------------------------------
    def _resolve_identity(self) -> Dict[str, Any]:
        """
        Resolve request identity using configured resolver.
        """
        request = self.context.get("request")
        resolver = get_identity_resolver()
        return resolver.resolve(request)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Global validation hook.

        Enforces:
            - Anonymous reporting rules
            - Reporter identity injection
        """
        identity = self._resolve_identity()

        allow_anonymous = get_setting("ALLOW_ANONYMOUS_REPORTING")

        # Prevent client from injecting reporter fields
        attrs.pop("reporter_user_id", None)
        attrs.pop("reporter_email", None)

        if identity["is_authenticated"]:
            # Authenticated user: inject identity
            attrs["reporter_user_id"] = identity["id"]
            attrs["reporter_email"] = identity["email"]

        else:
            # Anonymous user
            if not allow_anonymous:
                raise serializers.ValidationError(
                    "Authentication required to create an issue."
                )

            # Anonymous must provide email in request data
            email = self.initial_data.get("reporter_email")
            if not email:
                raise serializers.ValidationError(
                    {"reporter_email": "This field is required for anonymous reporting."}
                )

            attrs["reporter_email"] = email
            attrs["reporter_user_id"] = None

        return attrs
