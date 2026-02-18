"""
genericissuetracker.services.pagination
=======================================

Pagination resolution utilities for Generic Issue Tracker.

Purpose
-------
Resolve configured pagination class and page size from settings.

Design Principles
-----------------
- Host project controls pagination behavior.
- No hardcoded pagination inside ViewSets.
- Deterministic behavior.
- Fail-fast if misconfigured.
- No import-time side effects.
- DRF-native only (no external dependencies).

Configuration
-------------
GENERIC_ISSUETRACKER_DEFAULT_PAGINATION_CLASS
GENERIC_ISSUETRACKER_PAGE_SIZE

If DEFAULT_PAGINATION_CLASS is None:
    Pagination is disabled.
"""

from importlib import import_module
from typing import Optional, Type

from rest_framework.pagination import BasePagination

from genericissuetracker.settings import get_setting


def _import_from_dotted_path(path: str) -> Type[BasePagination]:
    """
    Import pagination class from dotted path.

    Parameters
    ----------
    path : str
        Full dotted path to pagination class.

    Returns
    -------
    Type[BasePagination]

    Raises
    ------
    ImportError
        If module cannot be imported.
    AttributeError
        If class is not found.
    TypeError
        If class is not a DRF pagination class.
    """
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    klass = getattr(module, class_name)

    if not issubclass(klass, BasePagination):
        raise TypeError(
            f"{path} is not a valid DRF pagination class."
        )

    return klass


def resolve_pagination_class() -> Optional[Type[BasePagination]]:
    """
    Resolve configured pagination class.

    Returns
    -------
    Type[BasePagination] or None
        Pagination class if configured,
        None if pagination disabled.
    """
    pagination_path = get_setting("DEFAULT_PAGINATION_CLASS")

    if pagination_path is None:
        return None

    if not isinstance(pagination_path, str):
        raise TypeError(
            "GENERIC_ISSUETRACKER_DEFAULT_PAGINATION_CLASS must be a string or None."
        )

    return _import_from_dotted_path(pagination_path)


def resolve_page_size() -> int:
    """
    Resolve configured page size.

    Returns
    -------
    int
        Configured page size.

    Raises
    ------
    TypeError
        If page size is not an integer.
    ValueError
        If page size is <= 0.
    """
    page_size = get_setting("PAGE_SIZE")

    if not isinstance(page_size, int):
        raise TypeError(
            "GENERIC_ISSUETRACKER_PAGE_SIZE must be an integer."
        )

    if page_size <= 0:
        raise ValueError(
            "GENERIC_ISSUETRACKER_PAGE_SIZE must be greater than zero."
        )

    return page_size
