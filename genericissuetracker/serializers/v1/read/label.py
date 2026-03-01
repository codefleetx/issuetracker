"""
genericissuetracker.serializers.v1.read.label
=============================================

Version 1 read serializer for Label.

Purpose
-------
Defines deterministic representation of a label.
"""

from rest_framework import serializers

from genericissuetracker.models import Label


class LabelReadSerializer(serializers.ModelSerializer):
    """
    Deterministic representation of a Label.
    """

    class Meta:
        model = Label
        fields = [
            "id",
            "number",
            "name",
            "slug",
            "color",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
