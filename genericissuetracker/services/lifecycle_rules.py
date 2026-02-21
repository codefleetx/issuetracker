from rest_framework.exceptions import ValidationError

from genericissuetracker.models import IssueStatus

ALLOWED_TRANSITIONS = {
    IssueStatus.OPEN: [
        IssueStatus.IN_PROGRESS,
        IssueStatus.CLOSED,
    ],
    IssueStatus.IN_PROGRESS: [
        IssueStatus.RESOLVED,
        IssueStatus.CLOSED,
    ],
    IssueStatus.RESOLVED: [
        IssueStatus.CLOSED,
        IssueStatus.OPEN,  # Reopen
    ],
    IssueStatus.CLOSED: [
        IssueStatus.OPEN,  # Reopen
    ],
}


def validate_transition(old_status, new_status):
    if old_status == new_status:
        raise ValidationError(
            "Status is already set to this value."
        )

    allowed = ALLOWED_TRANSITIONS.get(old_status, [])

    if new_status not in allowed:
        raise ValidationError(
            f"Illegal transition from {old_status} to {new_status}."
        )
