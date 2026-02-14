"""
genericissuetracker.settings
============================

Central configuration access layer for the Generic Issue Tracker.

Design Principles
-----------------
- This library MUST NOT contain environment-specific logic.
- The host Django project owns dev / staging / prod separation.
- This module provides:
    • Default configuration values
    • A safe accessor helper
    • A single namespace for overrides

Override Strategy
-----------------
Host applications can override any setting via:

    GENERIC_ISSUETRACKER_<SETTING_NAME>

Example:

    GENERIC_ISSUETRACKER_ALLOW_ANONYMOUS_REPORTING = False
    GENERIC_ISSUETRACKER_MAX_ATTACHMENTS = 3

This ensures:
- Deterministic behavior
- No hidden runtime branching
- Predictable OpenAPI schema generation
"""

from django.conf import settings as django_settings

# ----------------------------------------------------------------------
# DEFAULT CONFIGURATION VALUES
# ----------------------------------------------------------------------
DEFAULTS = {
    # --------------------------------------------------------------
    # Identity Resolution
    # --------------------------------------------------------------
    # Fully qualified path to identity resolver class.
    # Must implement:
    #     resolve(self, request) -> dict
    #
    # Required return structure:
    # {
    #     "id": Optional[int],
    #     "email": Optional[str],
    #     "is_authenticated": bool,
    # }
    # --------------------------------------------------------------
    "IDENTITY_RESOLVER": "genericissuetracker.services.identity.DefaultIdentityResolver",

    # --------------------------------------------------------------
    # Reporting Behavior
    # --------------------------------------------------------------
    # If False:
    #     Anonymous users cannot create issues.
    # If True:
    #     reporter_email becomes mandatory for anonymous requests.
    # --------------------------------------------------------------
    "ALLOW_ANONYMOUS_REPORTING": True,

    # --------------------------------------------------------------
    # Attachment Controls
    # --------------------------------------------------------------
    # Maximum number of attachments per issue.
    # Enforced at serializer validation layer.
    # --------------------------------------------------------------
    "MAX_ATTACHMENTS": 5,

    # Maximum attachment size in MB.
    # Used for validation only. Storage backend enforces physical limits.
    # --------------------------------------------------------------
    "MAX_ATTACHMENT_SIZE_MB": 10,
}


# ----------------------------------------------------------------------
# SAFE SETTING ACCESSOR
# ----------------------------------------------------------------------
def get_setting(name: str):
    """
    Fetch a namespaced configuration value.

    Lookup Order:
        1. Django project setting:
           GENERIC_ISSUETRACKER_<NAME>
        2. DEFAULTS defined in this module

    This helper ensures:
        - No direct dependency on Django settings internals
        - Centralized config access
        - Future extensibility (e.g. validation layer)

    Parameters
    ----------
    name : str
        Setting key without prefix.

    Returns
    -------
    Any
        Configuration value.
    """
    return getattr(
        django_settings,
        f"GENERIC_ISSUETRACKER_{name}",
        DEFAULTS.get(name),
    )
