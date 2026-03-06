from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from genericissuetracker.models import IssueStatusHistory
from genericissuetracker.signals import issue_status_changed

from .lifecycle_policy import get_transition_policy
from .lifecycle_rules import validate_transition


def change_issue_status(issue, new_status, identity, metadata=None, event_type="status_changed"):
    """
    Change issue status and record lifecycle history.

    Parameters
    ----------
    issue : Issue
        Issue instance being modified

    new_status : str
        Target status

    identity : dict
        Identity payload resolved from request

    metadata : dict, optional
        Optional contextual metadata for the event

    event_type : str
        Machine readable event classification
    """

    old_status = issue.status

    validate_transition(old_status, new_status)

    policy = get_transition_policy()

    if not policy.can_transition(issue, old_status, new_status, identity):
        raise PermissionDenied("Transition not allowed.")

    with transaction.atomic():
        issue.status = new_status
        issue.save(update_fields=["status"])

        IssueStatusHistory.objects.create(
            issue=issue,
            old_status=old_status,
            new_status=new_status,
            changed_by_user_id=identity.get("id"),
            changed_by_email=identity.get("email"),
            event_type=event_type,
            metadata=metadata or {},
        )

        issue_status_changed.send(
            sender=issue.__class__,
            issue=issue,
            old_status=old_status,
            new_status=new_status,
            identity=identity,
        )