"""
genericissuetracker.models.issue
================================

Primary Issue model for the Generic Issue Tracker.

Design Goals
------------
- No dependency on AUTH_USER_MODEL.
- Fully reusable across projects.
- Soft delete compatible (inherits BaseModel).
- Explicit status & priority enums.
- Deterministic schema for API versioning.

Important Architecture Decisions
---------------------------------
1. Reporter is NOT a ForeignKey.
   We store:
       • reporter_email
       • reporter_user_id (optional)

   Why?
   ----
   This library must not assume:
       • Django auth model structure
       • Custom user models
       • External identity systems

   Host applications can correlate reporter_user_id
   to their own user model.

2. No business logic here.
   All validation belongs in serializers.

3. Index critical fields for filtering performance.
"""

from django.db import models

from .base import BaseModel


# ----------------------------------------------------------------------
# ISSUE STATUS ENUM
# ----------------------------------------------------------------------
class IssueStatus(models.TextChoices):
    """
    Enumerates valid lifecycle states for an issue.

    This enum is versioned and must remain backward compatible.
    """

    OPEN = "OPEN", "Open"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


# ----------------------------------------------------------------------
# ISSUE PRIORITY ENUM
# ----------------------------------------------------------------------
class IssuePriority(models.TextChoices):
    """
    Enumerates issue severity levels.

    Must remain stable once released in v1.
    """

    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


# ----------------------------------------------------------------------
# ISSUE MODEL
# ----------------------------------------------------------------------
class Issue(BaseModel):
    """
    Core issue entity.

    Represents:
        • Bug reports
        • Feature requests
        • Tasks
        • Discussions

    This model intentionally contains:
        • No permission logic
        • No notification logic
        • No identity resolution
        • No business rules

    All mutation rules must be implemented in:
        • Serializers
        • Services layer
    """

    # ------------------------------------------------------------------
    # BASIC CONTENT
    # ------------------------------------------------------------------
    title = models.CharField(
        max_length=255,
        help_text="Short descriptive title of the issue.",
    )

    description = models.TextField(
        help_text="Detailed explanation of the issue in markdown or plain text.",
    )

    # ------------------------------------------------------------------
    # LIFECYCLE
    # ------------------------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
        default=IssueStatus.OPEN,
        db_index=True,
        help_text="Current lifecycle state of the issue.",
    )

    priority = models.CharField(
        max_length=20,
        choices=IssuePriority.choices,
        default=IssuePriority.MEDIUM,
        db_index=True,
        help_text="Severity level of the issue.",
    )

    # ------------------------------------------------------------------
    # REPORTER INFORMATION (DECOUPLED)
    # ------------------------------------------------------------------
    reporter_email = models.EmailField(
        help_text="Email address of the issue reporter.",
    )

    reporter_user_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Optional user ID from host application identity system.",
    )

    # ------------------------------------------------------------------
    # VISIBILITY
    # ------------------------------------------------------------------
    is_public = models.BooleanField(
        default=True,
        db_index=True,
        help_text="If False, issue is restricted to internal viewers.",
    )

    # ------------------------------------------------------------------
    # LABEL RELATION
    # ------------------------------------------------------------------
    labels = models.ManyToManyField(
        "Label",
        blank=True,
        related_name="issues",
        help_text="Categorization labels assigned to this issue.",
    )

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["reporter_user_id"]),
        ]

    # ------------------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.title} ({self.status})"
