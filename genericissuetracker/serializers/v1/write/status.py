from rest_framework import serializers
from genericissuetracker.models import IssueStatus


class IssueStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=IssueStatus.choices)