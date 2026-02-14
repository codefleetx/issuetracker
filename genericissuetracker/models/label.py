"""
genericissuetracker.models.label
================================

Label model for categorizing issues.

Design Goals
------------
- Soft delete enabled (inherits BaseModel).
- Globally reusable across issues.
- Slug-based uniqueness.
- Deterministic ordering.
- No business logic inside model.

Important
---------
Slug must remain stable once created.
Host applications may use slug for:

    • Filtering
    • UI badges
    • API references
    • Automation rules

Color is stored as HEX string (e.g. "#FF5733").
Validation of HEX format belongs in serializers,
not in the model layer.

Soft Delete Behavior
--------------------
Deleted labels:
    • Remain in database
    • Do not appear in default queries
    • Preserve historical issue relations
"""

from django.db import models

from .base import BaseModel


class Label(BaseModel):
    """
    Categorization label attached to issues.

    Example:
        - bug
        - enhancement
        - documentation
        - security
    """

    # ------------------------------------------------------------------
    # BASIC FIELDS
    # ------------------------------------------------------------------
    name = models.CharField(
        max_length=50,
        help_text="Human-readable label name.",
    )

    slug = models.SlugField(
        max_length=60,
        unique=True,
        db_index=True,
        help_text="Unique machine-friendly identifier for this label.",
    )

    color = models.CharField(
        max_length=7,
        default="#6B7280",
        help_text="HEX color code (e.g. #FF5733). Validation handled in serializers.",
    )

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
        ]

    # ------------------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return self.name
