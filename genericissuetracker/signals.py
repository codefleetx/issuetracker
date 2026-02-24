"""
genericissuetracker.signals
===========================

Signal definitions for the Generic Issue Tracker.

Purpose
-------
Provide extension points for host applications without creating
direct dependencies on:

    • Mail systems
    • Audit logging
    • Notification engines
    • Webhook dispatchers
    • External integrations

Design Philosophy
-----------------
- The core library emits signals.
- Host applications listen and react.
- No business logic lives here.
- No side effects are triggered automatically.

This ensures:
    • Reusability
    • Decoupling
    • Clean architecture
    • Long-term maintainability

Usage Example (Host App)
------------------------

from django.dispatch import receiver
from genericissuetracker.signals import issue_created

@receiver(issue_created)
def handle_issue_created(sender, issue, identity, **kwargs):
    # Send email, audit log, etc.
    pass

Signal Payload Contract
-----------------------
All signals MUST provide explicit, documented keyword arguments.
No implicit or dynamic payloads are allowed.
"""

from django.dispatch import Signal

# ----------------------------------------------------------------------
# ISSUE LIFECYCLE SIGNALS
# ----------------------------------------------------------------------

issue_created = Signal()
"""
Dispatched after a new issue is successfully created.

Kwargs:
    issue: Issue instance
    identity: dict containing identity resolution result
        {
            "id": Optional[int],
            "email": Optional[str],
            "is_authenticated": bool,
        }
"""


issue_commented = Signal()
"""
Dispatched after a new comment is added to an issue.

Kwargs:
    issue: Issue instance
    comment: IssueComment instance
    identity: dict containing identity resolution result
"""


issue_status_changed = Signal()
"""
Dispatched when an issue status transitions (e.g., OPEN → CLOSED).

Kwargs:
    issue: Issue instance
    old_status: str
    new_status: str
    identity: dict containing identity resolution result
"""


issue_updated = Signal()
"""
Dispatched after an issue is successfully updated.

Kwargs:
    issue: Issue instance
    identity: dict containing identity resolution result
"""


issue_deleted = Signal()
"""
Dispatched after an issue is soft deleted.

Kwargs:
    issue: Issue instance
    identity: dict containing identity resolution result
"""