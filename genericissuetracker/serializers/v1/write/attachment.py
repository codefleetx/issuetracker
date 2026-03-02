"""
genericissuetracker.serializers.v1.write.attachment
===================================================

Version 1 write serializer for IssueAttachment.

Responsibilities
----------------
- Handle file uploads.
- Enforce max attachment count.
- Enforce file size limit.
- Inject uploader identity.
- Validate comment/issue consistency.
"""

from rest_framework import serializers

from genericissuetracker.models import Issue, IssueAttachment
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting


class IssueAttachmentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading attachments.
    """
    issue = serializers.SlugRelatedField(
        slug_field="issue_number",
        queryset=Issue.objects.all(),
        help_text="Issue number (not UUID).",
    )

    class Meta:
        model = IssueAttachment
        fields = [
            "issue",
            "comment",
            "file",
        ]

    def validate(self, attrs):
        issue = attrs["issue"]
        file = attrs["file"]
        comment = attrs["comment"]

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
        
        if comment and comment.issue_id != issue.id:
            raise serializers.ValidationError(
                "Attachment comment must belong to the same issue."
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        identity = get_identity_resolver().resolve(request)

        validated_data["uploaded_by_user_id"] = identity.get("id")

        email = identity.get("email")
        if not email:
            raise serializers.ValidationError(
                {"uploaded_by_email": "Uploader email is required."}
            )

        validated_data["uploaded_by_email"] = email

        return IssueAttachment.objects.create(**validated_data)