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
        """
        Create issue instance.
        
        Identity fields are already injected in base validation.
        """
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
    
    class Meta(BaseIssueWriteSerializer.Meta):
        model = Issue
        fields = BaseIssueWriteSerializer.Meta.fields
    
    def update(self, instance, validated_data):
        """
        Update allowed fields only.
        Identity fields are never mutated.
        """
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
            
        instance.save()
        return instance
