"""
genericissuetracker.serializers.v1.write.attachment
===================================================

Version 1 write serializer for IssueAttachment.

Responsibilities
----------------
- Handle file uploads.
- Enforce max attachment count.
- Enforce file size limit.
"""

from rest_framework import serializers

from genericissuetracker.models import IssueAttachment
from genericissuetracker.settings import get_setting


class IssueAttachmentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading attachments.
    """

    class Meta:
        model = IssueAttachment
        fields = [
            "issue",
            "file",
        ]

    def validate(self, attrs):
        issue = attrs["issue"]
        file = attrs["file"]

        max_count = get_setting("MAX_ATTACHMENTS")
        max_size_mb = get_setting("MAX_ATTACHMENT_SIZE_MB")

        if issue.attachments.count() >= max_count:
            raise serializers.ValidationError(
                f"Maximum {max_count} attachments allowed per issue."
            )

        if file.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(
                f"File size must not exceed {max_size_mb} MB."
            )

        return attrs

    def create(self, validated_data):
        return IssueAttachment.objects.create(**validated_data)
