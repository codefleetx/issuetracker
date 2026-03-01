"""
genericissuetracker.models.comment
==================================

IssueComment model for the Generic Issue Tracker.

Design Goals
------------
- Soft delete enabled (inherits BaseModel).
- No dependency on AUTH_USER_MODEL.
- Explicit relation to Issue.
- Deterministic ordering.
- No business logic inside model.

Identity Strategy
-----------------
Comments store:
    • commenter_email
    • commenter_user_id (optional)

This avoids coupling to:
    • Django auth
    • Custom user models
    • External identity systems

Host applications are responsible for correlating
commenter_user_id with their own identity model.

Future Considerations
---------------------
This model is intentionally flat (no threading yet).
Threaded comments can be introduced in v2 via:

    parent = models.ForeignKey("self", ...)

Without breaking schema compatibility.
"""

from django.db import models

from .base import BaseModel
from django.db import transaction
from django.db.models import Max


class IssueComment(BaseModel):
    """
    Represents a single comment attached to an Issue.

    This model is intentionally simple and stable.
    """

    # ------------------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------------------
    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
        help_text="The issue this comment belongs to.",
    )
    
    # ------------------------------------------------------------------
    # PUBLIC IDENTIFIER
    # ------------------------------------------------------------------
    number = models.BigIntegerField(
        unique=True,
        db_index=True,
        editable=False,
        help_text="Sequential human-friendly identifier for this comment.",
    )

    # ------------------------------------------------------------------
    # CONTENT
    # ------------------------------------------------------------------    
    body = models.TextField(
        max_length=10000,
        help_text="Comment content in markdown or plain text.",
    )

    # ------------------------------------------------------------------
    # COMMENTER IDENTITY (DECOUPLED)
    # ------------------------------------------------------------------
    commenter_email = models.EmailField(
        help_text="Email address of the commenter.",
    )

    commenter_user_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Optional user ID from host application identity system.",
    )

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------
    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["issue"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["commenter_user_id"]),
        ]

    # ------------------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return f"Comment on {self.issue_id}"
    
    # ------------------------------------------------------------------
    # AUTO ASSIGN NUMBER
    # ------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """
        Automatically assign sequential number on first save.

        Concurrency Safe:
        Uses database transaction + MAX() aggregation.
        """
        if self.number is None:
            with transaction.atomic():
                last_number = (
                    IssueComment.all_objects.aggregate(
                        max_number=Max("number")
                    )["max_number"]
                    or 0
                )
                self.number = last_number + 1

        super().save(*args, **kwargs)
