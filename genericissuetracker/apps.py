"""
genericissuetracker.apps
========================

Django AppConfig for the Generic Issue Tracker application.

Purpose
-------
- Registers the application with Django.
- Ensures signal handlers are loaded at startup.
- Keeps initialization deterministic and side-effect free.

Design Principles
-----------------
- No business logic in AppConfig.
- No environment-specific branching.
- No database access during import.
- Only lightweight, safe startup hooks.
- No direct signal imports that trigger linter warnings.

Important
---------
Signal modules are auto-discovered inside `ready()` using
Django's autodiscover mechanism.

This prevents:
    • Circular imports
    • App registry timing issues
    • Unused-import linter warnings
    • Premature model loading

Compatibility
-------------
Fully compatible with:
    • Django migrations
    • Celery workers
    • Management commands
    • Test runners
"""

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class GenericIssueTrackerConfig(AppConfig):
    """
    Official Django application configuration.

    This class is automatically discovered when the app is added to
    INSTALLED_APPS.

    Example:
        INSTALLED_APPS = [
            "genericissuetracker",
        ]
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "genericissuetracker"
    verbose_name = "Generic Issue Tracker"

    def ready(self) -> None:
        """
        Auto-discover and register signal handlers.

        Uses Django's `autodiscover_modules` to load any `signals.py`
        modules within this app.

        Why this approach?
        ------------------
        - Avoids direct imports that trigger linter warnings
        - Prevents circular import risks
        - Ensures models are fully loaded before signal binding
        - Keeps startup deterministic
        """
        autodiscover_modules("signals")
