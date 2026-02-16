"""
genericissuetracker.serializers.v1.write.label
==============================================

Version 1 write serializer for Label.

Responsibilities
----------------
- Create new labels.
- Enforce slug uniqueness.
"""

from rest_framework import serializers

from genericissuetracker.models import Label


class LabelCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating labels.
    """

    class Meta:
        model = Label
        fields = [
            "name",
            "slug",
            "color",
        ]

    def create(self, validated_data):
        return Label.objects.create(**validated_data)
