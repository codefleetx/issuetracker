"""
genericissuetracker.services.identity
=====================================

Identity resolution service for Generic Issue Tracker.

Purpose
-------
Provide a pluggable abstraction layer for resolving user identity
from an incoming request.

Why This Exists
---------------
This library must NOT depend on:
    • Django's default User model
    • Custom AUTH_USER_MODEL
    • External authentication systems
    • Third-party identity providers

Instead, it exposes a configurable resolver that host
applications can override.

Default Behavior
----------------
The default resolver:
    • Uses request.user if authenticated
    • Returns a structured identity dictionary
    • Supports anonymous fallback

Override Strategy
-----------------
Host projects may override via Django settings:

    GENERIC_ISSUETRACKER_IDENTITY_RESOLVER = \
        "path.to.CustomIdentityResolver"

Custom resolver must implement:

    resolve(self, request) -> dict

Required return format:

    {
        "id": Optional[int],
        "email": Optional[str],
        "is_authenticated": bool,
    }

No dynamic fields allowed.
Schema must remain deterministic.
"""

from importlib import import_module
from typing import Any, Dict, Optional

from genericissuetracker.settings import get_setting


# ----------------------------------------------------------------------
# DEFAULT RESOLVER
# ----------------------------------------------------------------------
class DefaultIdentityResolver:
    """
    Default identity resolver implementation.

    Behavior:
        • If request.user is authenticated → extract id + email
        • Otherwise → return anonymous identity
    """

    def resolve(self, request: Any) -> Dict[str, Optional[Any]]:
        """
        Resolve identity from request.

        Parameters
        ----------
        request : HttpRequest
            Incoming request object.

        Returns
        -------
        dict
            Identity payload.
        """
        user = getattr(request, "user", None)

        if user and getattr(user, "is_authenticated", False):
            return {
                "id": getattr(user, "id", None),
                "email": getattr(user, "email", None),
                "is_authenticated": True,
            }

        return {
            "id": None,
            "email": None,
            "is_authenticated": False,
        }


# ----------------------------------------------------------------------
# RESOLVER FACTORY
# ----------------------------------------------------------------------
def get_identity_resolver():
    """
    Load configured identity resolver.

    Lookup Order:
        1. GENERIC_ISSUETRACKER_IDENTITY_RESOLVER (Django settings)
        2. DefaultIdentityResolver

    Returns
    -------
    Instance of configured resolver class.
    """
    resolver_path = get_setting("IDENTITY_RESOLVER")

    if not resolver_path:
        return DefaultIdentityResolver()

    module_path, class_name = resolver_path.rsplit(".", 1)
    module = import_module(module_path)
    resolver_class = getattr(module, class_name)

    return resolver_class()
