from django.db import models

from genericissuetracker.models.base import BaseModel
from genericissuetracker.models.issue import IssueStatus


class IssueStatusHistory(BaseModel):
    """
    Tracks lifecycle transitions for Issue.
    Industry standard audit trail.
    """

    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        related_name="status_history",
        db_index=True,
    )

    old_status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
    )

    new_status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
    )

    changed_by_user_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    changed_by_email = models.EmailField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["issue"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.issue.issue_number}: {self.old_status} → {self.new_status}"