"""
genericissuetracker.serializers.v1.write.comment
================================================

Version 1 write serializer for IssueComment.

Responsibilities
----------------
- Allow comment creation.
- Inject identity automatically.
- Prevent spoofing of commenter fields.
- Support atomic comment + attachment creation.
"""

from django.db import transaction
from rest_framework import serializers

from genericissuetracker.models import Issue, IssueAttachment, IssueComment
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting
from genericissuetracker.signals import (
    attachment_added,
    issue_commented,
)


class IssueCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new comments.
    """

    commenter_email = serializers.EmailField(
        required=False,
        help_text="Required for anonymous users."
    )
    
    # File support 0.5.3
    files = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        write_only=True,
        help_text="Optional files to attach to this comment."
    )
    
    issue = serializers.SlugRelatedField(
        slug_field="issue_number",
        queryset=Issue.objects.all(),
        help_text="Issue number (not UUID).",
    )

    class Meta:
        model = IssueComment
        fields = [
            "issue",
            "body",
            "commenter_email",
            "files",
        ]

    def validate(self, attrs):
        identity = get_identity_resolver().resolve(
            self.context.get("request")
        )

        allow_anonymous = get_setting("ALLOW_ANONYMOUS_REPORTING")
        max_length = get_setting("MAX_COMMENT_LENGTH")

        attrs.pop("commenter_user_id", None)
        
        # Comment length policy 0.5.2
        body = attrs.get("body", "")

        if len(body) > max_length:
            raise serializers.ValidationError(
                {"body": f"Comment cannot exceed {max_length} characters."}
            )

        if identity["is_authenticated"]:
            attrs["commenter_user_id"] = identity["id"]
            attrs["commenter_email"] = identity["email"]
        else:
            if not allow_anonymous:
                raise serializers.ValidationError(
                    "Authentication required to comment."
                )

            email = self.initial_data.get("commenter_email")
            if not email:
                raise serializers.ValidationError(
                    {"commenter_email": "This field is required for anonymous commenting."}
                )

            attrs["commenter_user_id"] = None
            attrs["commenter_email"] = email

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        identity = get_identity_resolver().resolve(request)

        files = validated_data.pop("files", [])

        with transaction.atomic():
            # First Create Comment
            comment = IssueComment.objects.create(**validated_data)

            # Emit comment signal
            issue_commented.send(
                sender=comment.__class__,
                issue=comment.issue,
                comment=comment,
                identity=identity,
            )
            
            # Then Attachments (if any)            
            max_count = get_setting("MAX_ATTACHMENTS")
            max_size_mb = get_setting("MAX_ATTACHMENT_SIZE_MB")

            existing_count = comment.issue.attachments.count()

            for file in files:

                if existing_count >= max_count:
                    raise serializers.ValidationError(
                        f"Maximum {max_count} attachments allowed per issue."
                    )

                if file.size > max_size_mb * 1024 * 1024:
                    raise serializers.ValidationError(
                        f"File size must not exceed {max_size_mb} MB."
                    )

                attachment = IssueAttachment.objects.create(
                    issue=comment.issue,
                    comment=comment,
                    file=file,
                    uploaded_by_user_id=identity.get("id"),
                    uploaded_by_email=identity.get("email"),
                )

                attachment_added.send(
                    sender=attachment.__class__,
                    issue=comment.issue,
                    attachment=attachment,
                    identity=identity,
                    comment=comment,
                )

                existing_count += 1

        return comment
