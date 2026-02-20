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

Design Rules
------------
- Create and Update serializers are separate.
- Identity fields are NOT client-controlled.
- Status transitions will be handled later (TODO).
"""


from rest_framework import serializers

from genericissuetracker.models.issue import Issue
from genericissuetracker.serializers.base.issue import BaseIssueWriteSerializer
from genericissuetracker.services.identity import get_identity_resolver
from genericissuetracker.settings import get_setting


# ----------------------------------------------------------------------
# ISSUE CREATE SERIALIZER (V1)
# ----------------------------------------------------------------------
class IssueCreateSerializer(BaseIssueWriteSerializer):
    """
    Serializer for creating new issues.
    
    Exposes reporter_email only for anonymous users.
    Authenticated identity is inhjected automatically.
    """
    
    reporter_email = serializers.EmailField(
        required=False,
        help_text="Required for anonymous users."
    )
    
    class Meta(BaseIssueWriteSerializer.Meta):
        model = Issue
        fields = BaseIssueWriteSerializer.Meta.fields +[
            "reporter_email",
        ]
        
    def create(self, validated_data):
        request = self.context.get("request")
        resolver = get_identity_resolver()
        identity = resolver.resolve(request)

        allow_anonymous = get_setting("ALLOW_ANONYMOUS_REPORTING")

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

        return Issue.objects.create(**validated_data)


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
    # reporter_user_id = serializers.IntegerField(read_only=True)
    
    class Meta(BaseIssueWriteSerializer.Meta):
        model = Issue
        fields = BaseIssueWriteSerializer.Meta.fields  + [
            "reporter_email",
            # "reporter_user_id",
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
