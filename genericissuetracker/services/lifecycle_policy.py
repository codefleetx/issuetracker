from genericissuetracker.settings import get_setting
from importlib import import_module


class DefaultTransitionPolicy:
    """
    Default: allow all legal transitions.
    Host app may override.
    """

    def can_transition(self, issue, old_status, new_status, identity):
        return True


def get_transition_policy():
    path = get_setting("TRANSITION_POLICY")

    if not path:
        return DefaultTransitionPolicy()

    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    policy_class = getattr(module, class_name)

    return policy_class()