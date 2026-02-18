"""
genericissuetracker.services.filtering
======================================

Filtering resolution utilities for Generic Issue Tracker.

Purpose
-------
Resolve configured DRF filter backends from settings.

Design Principles
-----------------
- Host project controls filtering behavior.
- No hardcoded filter backends inside ViewSets.
- Deterministic resolution.
- Fail-fast if misconfigured.
- DRF-native only (no external dependencies).

Configuration
-------------
GENERIC_ISSUETRACKER_DEFAULT_FILTER_BACKENDS

If empty list:
    Filtering is disabled.
"""

from importlib import import_module
from typing import List, Type

from rest_framework.filters import BaseFilterBackend

from genericissuetracker.settings import get_setting


def _import_from_dotted_path(path: str) -> Type[BaseFilterBackend]:
    """
    Import filter backend class from dotted path.

    Parameters
    ----------
    path : str
        Full dotted path to filter backend class.

    Returns
    -------
    Type[BaseFilterBackend]

    Raises
    ------
    ImportError
        If module cannot be imported.
    AttributeError
        If class not found.
    TypeError
        If class is not a DRF filter backend.
    """
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    klass = getattr(module, class_name)

    if not issubclass(klass, BaseFilterBackend):
        raise TypeError(
            f"{path} is not a valid DRF filter backend."
        )

    return klass


def resolve_filter_backends() -> List[Type[BaseFilterBackend]]:
    """
    Resolve configured filter backends.

    Returns
    -------
    List[Type[BaseFilterBackend]]
        List of DRF filter backend classes.
    """
    backend_paths = get_setting("DEFAULT_FILTER_BACKENDS")

    if not isinstance(backend_paths, list):
        raise TypeError(
            "GENERIC_ISSUETRACKER_DEFAULT_FILTER_BACKENDS must be a list."
        )

    resolved_backends = []

    for path in backend_paths:
        if not isinstance(path, str):
            raise TypeError(
                "Filter backend paths must be strings."
            )

        resolved_backends.append(
            _import_from_dotted_path(path)
        )

    return resolved_backends
