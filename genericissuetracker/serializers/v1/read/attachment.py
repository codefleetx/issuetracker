"""
genericissuetracker.serializers.v1.read.attachment
==================================================

Version 1 read serializer for IssueAttachment.

Purpose
-------
Defines deterministic representation of an attachment.
"""

from rest_framework import serializers

from genericissuetracker.models import IssueAttachment


class IssueAttachmentReadSerializer(serializers.ModelSerializer):
    """
    Deterministic representation of an Issue attachment.
    """

    class Meta:
        model = IssueAttachment
        fields = [
            "id",
            "number",
            "issue",
            "comment",
            "file",
            "original_name",
            "size",
            "uploaded_by_user_id",
            "uploaded_by_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
