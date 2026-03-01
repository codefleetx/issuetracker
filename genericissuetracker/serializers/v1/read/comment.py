"""
genericissuetracker.serializers.v1.read.comment
===============================================

Version 1 read serializer for IssueComment.

Purpose
-------
Defines deterministic representation of a comment.

Design Rules
------------
- Explicit field declaration.
- Identity snapshot only.
- No nested issue object.
"""

from rest_framework import serializers

from genericissuetracker.models import IssueComment


class IssueCommentReadSerializer(serializers.ModelSerializer):
    """
    Deterministic representation of an Issue comment.
    """

    class Meta:
        model = IssueComment
        fields = [
            "id",
            "number",
            "issue",
            "body",
            "commenter_email",
            "commenter_user_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
