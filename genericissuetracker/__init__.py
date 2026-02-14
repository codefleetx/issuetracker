"""
genericissuetracker
===================

Reusable, versioned, schema-safe Django Issue Tracker application.

Design Goals
------------
- Fully decoupled from host project domain models.
- API-first architecture.
- URL-based versioning (/v1/).
- Strict serializer separation (read / write).
- DRF + drf-spectacular compatible.
- Soft delete enabled from day one.
- Signals for extensibility (mailer, audit, webhooks).

Important
---------
This package intentionally contains:
    • No environment-specific configuration
    • No direct user model dependencies
    • No mailer or audit coupling
    • No implicit side effects

Host applications are expected to:

    1. Add "genericissuetracker" to INSTALLED_APPS
    2. Include its URL configuration
    3. Optionally override configuration via:
         GENERIC_ISSUETRACKER_<SETTING_NAME>

Compatibility
-------------
Requires:
    - Django >= 4.2
    - Django REST Framework >= 3.14
    - drf-spectacular >= 0.27
"""

__all__ = []
