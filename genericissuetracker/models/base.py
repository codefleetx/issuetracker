"""
genericissuetracker.models.base
===============================

Abstract base model providing:

    • UUID primary key
    • Created / Updated timestamps
    • Soft delete capability
    • Safe queryset managers
    • Deterministic behavior

Design Principles
-----------------
- All concrete models must inherit from BaseModel.
- Soft deletion must NEVER physically delete records.
- Default manager must return only active (non-deleted) records.
- Access to deleted records must be explicit.
- No business logic allowed in base model.

Soft Delete Strategy
--------------------
Instead of deleting database rows:

    is_deleted = True
    deleted_at = <timestamp>

This ensures:
    • Audit compatibility
    • Historical integrity
    • Safer integrations
    • Recoverability
    • Schema stability

Performance
-----------
- is_deleted is indexed for efficient filtering.
- Default manager filters automatically.
- all_objects allows explicit access to full dataset.
"""

import uuid

from django.db import models
from django.utils import timezone


# ----------------------------------------------------------------------
# QUERYSET WITH SOFT DELETE AWARENESS
# ----------------------------------------------------------------------
class SoftDeleteQuerySet(models.QuerySet):
    """
    Custom QuerySet that supports soft delete operations.

    Important:
        - delete() performs soft delete.
        - hard_delete() performs irreversible physical deletion.
        - active() returns non-deleted records.
        - deleted() returns soft-deleted records.
    """

    def delete(self):
        """
        Override bulk delete to perform soft deletion.

        This ensures that calling:
            Model.objects.filter(...).delete()

        Does NOT remove rows from database.
        """
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def hard_delete(self):
        """
        Permanently delete records from database.

        Use with extreme caution.
        Intended for maintenance scripts only.
        """
        return super().delete()

    def active(self):
        """Return only non-deleted records."""
        return self.filter(is_deleted=False)

    def deleted(self):
        """Return only soft-deleted records."""
        return self.filter(is_deleted=True)


# ----------------------------------------------------------------------
# DEFAULT MANAGER (ACTIVE RECORDS ONLY)
# ----------------------------------------------------------------------
class SoftDeleteManager(models.Manager):
    """
    Default manager returning only active records.

    This prevents accidental exposure of soft-deleted rows
    in normal application queries.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


# ----------------------------------------------------------------------
# BASE ABSTRACT MODEL
# ----------------------------------------------------------------------
class BaseModel(models.Model):
    """
    Abstract base model for all Generic Issue Tracker models.

    Provides:
        - UUID primary key
        - Timestamps
        - Soft delete
        - Safe managers

    Usage:
        class Issue(BaseModel):
            ...
    """

    # ------------------------------------------------------------------
    # PRIMARY KEY
    # ------------------------------------------------------------------
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Universally unique identifier for this record.",
    )

    # ------------------------------------------------------------------
    # TIMESTAMPS
    # ------------------------------------------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated.",
    )

    # ------------------------------------------------------------------
    # SOFT DELETE FIELDS
    # ------------------------------------------------------------------
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft delete flag. True means logically deleted.",
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the record was soft deleted.",
    )

    # ------------------------------------------------------------------
    # MANAGERS
    # ------------------------------------------------------------------
    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------
    class Meta:
        abstract = True

    # ------------------------------------------------------------------
    # INSTANCE METHODS
    # ------------------------------------------------------------------
    def soft_delete(self):
        """
        Soft delete this record.

        Safe alternative to instance.delete().
        """
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """
        Restore a previously soft-deleted record.
        """
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self):
        """
        Permanently delete this record from database.

        Use sparingly.
        """
        super().delete()
