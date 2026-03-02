"""
genericissuetracker.serializers.v1.write.issue
==============================================

Version 1 write serializer for Issue

Responsibilities
----------------

- Define explicit create and update serializers.
- Inherit shared validation from BaseIssueWriteSerializer.
- Keep read/write concerns strictly separated.
- Maintain deterministic schema for OpenAPI generation.
- Support atomic issue creation with attachments (v0.6.0).

Design Rules
------------
- Create and Update serializers are separate.
- Identity fields are NOT client-controlled.
- Attachment creation must be atomic with issue creation.
"""

from django.db import transaction
from rest_framework import serializers

from genericissuetracker.models.issue import Issue
from genericissuetracker.models.attachment import IssueAttachment
from genericissuetracker.serializers.base.issue import BaseIssueWriteSerializer
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting
from genericissuetracker.signals import attachment_added


# ----------------------------------------------------------------------
# ISSUE CREATE SERIALIZER (V1)
# ----------------------------------------------------------------------
class IssueCreateSerializer(BaseIssueWriteSerializer):
    """
    Serializer for creating new issues.
    
    Exposes reporter_email only for anonymous users.
    Authenticated identity is injected automatically.

    v0.6.0
    ------
    Supports atomic issue creation with optional attachments.
    """

    reporter_email = serializers.EmailField(
        required=False,
        help_text="Required for anonymous users."
    )

    # ------------------------------------------------------------------
    # ATTACHMENT SUPPORT (v0.6.0)
    # ------------------------------------------------------------------
    files = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        write_only=True,
        help_text="Optional files to attach during issue creation."
    )

    class Meta(BaseIssueWriteSerializer.Meta):
        model = Issue
        fields = BaseIssueWriteSerializer.Meta.fields + [
            "reporter_email",
            "files",
        ]

    def create(self, validated_data):
        """
        Atomic issue creation with optional attachments.
        """

        request = self.context.get("request")
        resolver = get_identity_resolver()
        identity = resolver.resolve(request)

        allow_anonymous = get_setting("ALLOW_ANONYMOUS_REPORTING")
        max_attachments = get_setting("MAX_ATTACHMENTS")
        max_size_mb = get_setting("MAX_ATTACHMENT_SIZE_MB")

        # Extract files (if any)
        files = validated_data.pop("files", [])

        # Prevent spoofing
        validated_data.pop("reporter_user_id", None)
        validated_data.pop("reporter_email", None)

        if identity["is_authenticated"]:
            validated_data["reporter_user_id"] = identity["id"]
            validated_data["reporter_email"] = identity["email"]

        else:
            if not allow_anonymous:
                raise serializers.ValidationError(
                    "Authentication required to create an issue."
                )

            email = self.initial_data.get("reporter_email")
            if not email:
                raise serializers.ValidationError(
                    {"reporter_email": "This field is required for anonymous reporting."}
                )

            validated_data["reporter_user_id"] = None
            validated_data["reporter_email"] = email

        # ------------------------------------------------------------------
        # ATOMIC TRANSACTION
        # ------------------------------------------------------------------
        with transaction.atomic():

            # Create Issue
            issue = Issue.objects.create(**validated_data)

            # Validate attachment count
            if len(files) > max_attachments:
                raise serializers.ValidationError(
                    f"Maximum {max_attachments} attachments allowed per issue."
                )

            # Create attachments
            for file in files:

                if file.size > max_size_mb * 1024 * 1024:
                    raise serializers.ValidationError(
                        f"File size must not exceed {max_size_mb} MB."
                    )

                attachment = IssueAttachment.objects.create(
                    issue=issue,
                    file=file,
                    uploaded_by_user_id=identity.get("id"),
                    uploaded_by_email=validated_data["reporter_email"],
                )

                # Emit attachment signal
                attachment_added.send(
                    sender=attachment.__class__,
                    issue=issue,
                    attachment=attachment,
                    identity=identity,
                    comment=None,
                )

        return issue


# ----------------------------------------------------------------------
# ISSUE UPDATE SERIALIZER (V1)
# ----------------------------------------------------------------------
class IssueUpdateSerializer(BaseIssueWriteSerializer):
    """
    Serializer for updating existing issue.
    
    Rules:
        - reporter_email cannot be changed.
        - reporter_user_id cannot be changed.
        - Status changes restricted.
    """
    
    reporter_email = serializers.EmailField(read_only=True)
    
    class Meta(BaseIssueWriteSerializer.Meta):
        model = Issue
        fields = BaseIssueWriteSerializer.Meta.fields + [
            "reporter_email",
        ]
    
    def update(self, instance, validated_data):
        """
        Update allowed fields only.
        Identity fields are never mutated.
        """
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
            
        instance.save()
        return instance
