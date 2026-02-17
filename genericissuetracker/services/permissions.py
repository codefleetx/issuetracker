"""
genericissuetracker.services.permissions
========================================

Permission resolution utilities for Generic Issue Tracker.

Purpose
-------
Resolve dotted permission class paths defined in settings into
actual DRF permission classes.

Design Principles
-----------------
- No hardcoded permission classes in views.
- Host project controls default permissions.
- Deterministic resolution.
- Fail-fast if misconfigured.
- No import-time side effects.

Example Setting
---------------
GENERIC_ISSUETRACKER_DEFAULT_PERMISSION_CLASSES = [
    "rest_framework.permissions.IsAuthenticated",
]

If not overridden, defaults to:
    ["rest_framework.permissions.AllowAny"]
"""

from importlib import import_module
from typing import List, Type

from rest_framework.permissions import BasePermission

from genericissuetracker.settings import get_setting


def _import_from_dotted_path(path: str) -> Type[BasePermission]:
    """
    Import a class from a dotted path string.

    Parameters
    ----------
    path : str
        Full dotted path to permission class.

    Returns
    -------
    Type[BasePermission]
        Imported permission class.

    Raises
    ------
    ImportError
        If module cannot be imported.
    AttributeError
        If class is not found in module.
    TypeError
        If imported object is not a DRF permission class.
    """
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    klass = getattr(module, class_name)

    if not issubclass(klass, BasePermission):
        raise TypeError(
            f"{path} is not a valid DRF permission class."
        )

    return klass


def resolve_default_permission_classes() -> List[Type[BasePermission]]:
    """
    Resolve configured default permission classes.

    Returns
    -------
    List[Type[BasePermission]]
        List of DRF permission classes.
    """
    permission_paths = get_setting("DEFAULT_PERMISSION_CLASSES")

    if not isinstance(permission_paths, list):
        raise TypeError(
            "GENERIC_ISSUETRACKER_DEFAULT_PERMISSION_CLASSES must be a list."
        )

    resolved_permissions = []

    for path in permission_paths:
        if not isinstance(path, str):
            raise TypeError(
                "Permission class paths must be strings."
            )

        resolved_permissions.append(
            _import_from_dotted_path(path)
        )

    return resolved_permissions
