"""
genericissuetracker.models
==========================

Public model exports for Generic Issue Tracker.

Purpose
-------
- Provide clean import surface for consumers.
- Avoid deep import paths.
- Centralize model exposure.
- Maintain deterministic module structure.

Usage
-----
Host applications may import models like:

    from genericissuetracker.models import Issue
    from genericissuetracker.models import IssueComment
    from genericissuetracker.models import Label
    from genericissuetracker.models import IssueAttachment

Design Rules
------------
- Only concrete models are exported here.
- BaseModel remains internal.
- Enums are exported only if part of public API surface.
"""

from .attachment import IssueAttachment
from .comment import IssueComment
from .issue import Issue, IssuePriority, IssueStatus
from .label import Label
from .status_history import IssueStatusHistory

__all__ = [
    "Issue",
    "IssuePriority",
    "IssueStatus",
    "IssueComment",
    "Label",
    "IssueAttachment",
    "IssueStatusHistory",
]
