from django.db import models

from genericissuetracker.models.base import BaseModel
from genericissuetracker.models.issue import IssueStatus


class IssueStatusHistory(BaseModel):
    """
    Tracks lifecycle transitions for Issue.

    This model acts as a timeline-ready event store for issue lifecycle events.
    It records status transitions and allows attaching structured metadata
    for integrations, automation, and analytics.

    Design Principles
    -----------------
    • Library-safe (no auth dependency)
    • Timeline friendly
    • Extensible via metadata JSON
    • Explicit event classification
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
    
    # Event Classification
    event_type = models.CharField(
        max_length=32,
        default="status_changed",
        db_index=True,
        help_text="Machine readable event classification.",
    )

    # Extensible Metadata
    metadata = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="Optional structured metadata for integrations and automation.",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["issue"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["issue", "created_at"]),
        ]

    def __str__(self):
        return f"{self.issue.issue_number}: {self.old_status} → {self.new_status}"