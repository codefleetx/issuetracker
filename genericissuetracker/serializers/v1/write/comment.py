"""
genericissuetracker.serializers.v1.write.comment
================================================

Version 1 write serializer for IssueComment.

Responsibilities
----------------
- Allow comment creation.
- Inject identity automatically.
- Prevent spoofing of commenter fields.
"""

from rest_framework import serializers

from genericissuetracker.models import IssueComment
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting


class IssueCommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new comments.
    """

    commenter_email = serializers.EmailField(
        required=False,
        help_text="Required for anonymous users."
    )

    class Meta:
        model = IssueComment
        fields = [
            "issue",
            "body",
            "commenter_email",
        ]

    def validate(self, attrs):
        identity = get_identity_resolver().resolve(
            self.context.get("request")
        )

        allow_anonymous = get_setting("ALLOW_ANONYMOUS_REPORTING")
        max_length = get_setting("MAX_COMMENT_LENGTH")

        attrs.pop("commenter_user_id", None)

        # ----------------------------------------------------------
        # COMMENT LENGTH ENFORCEMENT (v0.5.2)
        # ----------------------------------------------------------
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
        return IssueComment.objects.create(**validated_data)
