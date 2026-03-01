"""
genericissuetracker.models.attachment
=====================================

IssueAttachment model for file uploads linked to an Issue.

Design Goals
------------
- Soft delete enabled (inherits BaseModel).
- Storage backend agnostic.
- No direct dependency on any specific file storage system.
- Validation of size and count handled in serializer layer.
- Secure upload path structure.

Security Considerations
-----------------------
- Files are stored under:
      issues/<issue_id>/<filename>

- No user-supplied path manipulation allowed.
- original_name stored explicitly for display purposes.

Important
---------
This model does NOT:
    • Enforce file size limits (serializer responsibility)
    • Enforce max attachment count (serializer responsibility)
    • Send notifications
    • Trigger business logic

Future Compatibility
--------------------
Designed to support:
    • Local file storage
    • S3 / cloud storage backends
    • Signed URL generation
    • Virus scanning middleware
"""

import os

from django.db import models

from .base import BaseModel
from django.db import transaction
from django.db.models import Max


def issue_attachment_upload_path(instance, filename: str) -> str:
    """
    Construct deterministic upload path.

    Format:
        issues/<issue_uuid>/<filename>

    This ensures:
        • Logical grouping per issue
        • Easy storage cleanup
        • Clear directory structure
    """
    base_name = os.path.basename(filename)
    return f"issues/{instance.issue_id}/{base_name}"


class IssueAttachment(BaseModel):
    """
    Represents a file attached to an Issue.

    Attachments are independent soft-deletable records.
    """

    # ------------------------------------------------------------------
    # RELATIONSHIP
    # ------------------------------------------------------------------
    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        related_name="attachments",
        db_index=True,
        help_text="Issue this attachment belongs to.",
    )
    
    # ------------------------------------------------------------------
    # PUBLIC IDENTIFIER
    # ------------------------------------------------------------------
    number = models.BigIntegerField(
        unique=True,
        db_index=True,
        editable=False,
        help_text="Sequential human-friendly identifier for this attachment.",
    )

    # ------------------------------------------------------------------
    # FILE STORAGE
    # ------------------------------------------------------------------
    file = models.FileField(
        upload_to=issue_attachment_upload_path,
        help_text="Uploaded file.",
    )

    original_name = models.CharField(
        max_length=255,
        help_text="Original filename at upload time.",
    )

    size = models.PositiveBigIntegerField(
        help_text="File size in bytes.",
    )

    # ------------------------------------------------------------------
    # META
    # ------------------------------------------------------------------
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["issue"]),
            models.Index(fields=["created_at"]),
        ]

    # ------------------------------------------------------------------
    # SAVE OVERRIDE (SAFE METADATA POPULATION)
    # ------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """
        Automatically populate number, original_name and size
        when file is first saved.

        This keeps metadata consistent without adding
        business logic to serializers.
        """
        if self.number is None:
            with transaction.atomic():
                last_number = (
                    IssueAttachment.all_objects.aggregate(
                        max_number=Max("number")
                    )["max_number"]
                    or 0
                )
                self.number = last_number + 1

        if self.file:
            if not self.original_name:
                self.original_name = os.path.basename(self.file.name)

            if not self.size:
                try:
                    self.size = self.file.size
                except Exception:
                    self.size = 0

        super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # STRING REPRESENTATION
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return self.original_name
