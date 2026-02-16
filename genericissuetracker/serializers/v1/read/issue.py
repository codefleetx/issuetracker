"""
genericissuetracker.serializers.v1.read.issue
=============================================

Version 1 read serializer for Issue.

Purpose
-------
Defines the deterministic API representation of an Issue.

Design Rules
------------
- Explicit field declaration (no "__all__").
- No dynamic fields based on request context.
- Nested serializers are read-only.
- Identity fields are exposed in controlled manner.
- Soft-deleted related objects are excluded by default
  via model managers.

This serializer defines the public contract for:
    GET /api/v1/issues/
    GET /api/v1/issues/{id}/
"""

from rest_framework import serializers

from genericissuetracker.models import Issue
from genericissuetracker.serializers.v1.read.attachment import (
    IssueAttachmentReadSerializer,
)
from genericissuetracker.serializers.v1.read.comment import IssueCommentReadSerializer
from genericissuetracker.serializers.v1.read.label import LabelReadSerializer


class IssueReadSerializer(serializers.ModelSerializer):
    """
    Deterministic representation of an Issue.

    Includes:
        - Core issue fields
        - Reporter metadata snapshot
        - Nested comments
        - Nested labels
        - Nested attachments
    """

    comments = IssueCommentReadSerializer(many=True, read_only=True)
    labels = LabelReadSerializer(many=True, read_only=True)
    attachments = IssueAttachmentReadSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            # Primary Identity
            "id",

            # Content
            "title",
            "description",

            # Lifecycle
            "status",
            "priority",
            "is_public",

            # Reporter Snapshot
            "reporter_email",
            "reporter_user_id",

            # Relations
            "labels",
            "comments",
            "attachments",

            # Timestamps
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
