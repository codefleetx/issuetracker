"""
genericissuetracker.views.v1.base
=================================

Base view layer utilities for Version 1 API.

Purpose
-------
Provide shared, deterministic behavior for:

    • Read-only ViewSets
    • CRUD ViewSets

Design Principles
-----------------
- No business logic in views.
- Explicit serializer separation.
- Deterministic serializer selection.
- Configurable permission architecture.
- Configurable pagination architecture.
- No dynamic schema behavior.
- DRY queryset handling.

Rules Enforced
--------------
1. CRUD ViewSets MUST define:
       - read_serializer_class
       - write_serializer_class

2. Read-only ViewSets MUST define:
       - read_serializer_class

3. Serializer selection must never depend on runtime
   request data other than action name.

4. Permission classes default to configured setting
   unless explicitly overridden in ViewSet.

5. Pagination defaults to configured setting
   unless explicitly overridden in ViewSet.
"""

from rest_framework import viewsets

from genericissuetracker.services.filtering import resolve_filter_backends
from genericissuetracker.services.pagination import (
    resolve_page_size,
    resolve_pagination_class,
)
from genericissuetracker.services.permissions import (
    resolve_default_permission_classes,
)


# ----------------------------------------------------------------------
# BASE READ-ONLY VIEWSET
# ----------------------------------------------------------------------
class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Base class for read-only endpoints.

    Requirements:
        - Must define `read_serializer_class`
        - Must define `queryset`
    """

    read_serializer_class = None

    # ------------------------------------------------------------------
    # Serializer Handling
    # ------------------------------------------------------------------
    def get_serializer_class(self):
        if not self.read_serializer_class:
            raise AssertionError(
                "Read-only ViewSet must define `read_serializer_class`."
            )

        return self.read_serializer_class

    # ------------------------------------------------------------------
    # Permission Handling
    # ------------------------------------------------------------------
    def get_permissions(self):
        # Explicit override on subclass
        if "permission_classes" in self.__class__.__dict__:
            return [permission() for permission in self.permission_classes]

        default_permissions = resolve_default_permission_classes()
        return [permission() for permission in default_permissions]
    
    # ------------------------------------------------------------------
    # Pagination Handling
    # ------------------------------------------------------------------
    def get_pagination_class(self):
        if "pagination_class" in self.__class__.__dict__:
            return self.pagination_class

        return resolve_pagination_class()

    def paginate_queryset(self, queryset):
        pagination_class = self.get_pagination_class()

        if pagination_class is None:
            return None

        paginator = pagination_class()
        paginator.page_size = resolve_page_size()

        self._paginator = paginator
        return paginator.paginate_queryset(queryset, self.request, view=self)

    # ------------------------------------------------------------------
    # Filtering Handling
    # ------------------------------------------------------------------
    def get_filter_backends(self):
        if "filter_backends" in self.__class__.__dict__:
            return self.filter_backends

        return resolve_filter_backends()
    
    def filter_queryset(self, queryset):
        """
        Apply configured filter backends deterministically.
        """
        if "filter_backends" in self.__class__.__dict__:
            backends = self.filter_backends
        else:
            backends = resolve_filter_backends()

        for backend in backends:
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset


# ----------------------------------------------------------------------
# BASE CRUD VIEWSET
# ----------------------------------------------------------------------
class BaseCRUDViewSet(viewsets.ModelViewSet):
    """
    Base class for write-capable endpoints.

    Requirements:
        - Must define `read_serializer_class`
        - Must define `write_serializer_class`
        - Must define `queryset`
    """

    read_serializer_class = None
    write_serializer_class = None
    
    # ------------------------------------------------------------------
    # Serializer Handling
    # ------------------------------------------------------------------
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if not self.write_serializer_class:
                raise AssertionError(
                    "CRUD ViewSet must define `write_serializer_class`."
                )
            return self.write_serializer_class

        if not self.read_serializer_class:
            raise AssertionError(
                "CRUD ViewSet must define `read_serializer_class`."
            )

        return self.read_serializer_class

    # ------------------------------------------------------------------
    # Permission Handling
    # ------------------------------------------------------------------
    def get_permissions(self):
        if "permission_classes" in self.__class__.__dict__:
            return [permission() for permission in self.permission_classes]

        default_permissions = resolve_default_permission_classes()
        return [permission() for permission in default_permissions]

    # ------------------------------------------------------------------
    # Pagination Handling
    # ------------------------------------------------------------------
    def get_pagination_class(self):
        if "pagination_class" in self.__class__.__dict__:
            return self.pagination_class

        return resolve_pagination_class()

    def paginate_queryset(self, queryset):
        pagination_class = self.get_pagination_class()

        if pagination_class is None:
            return None

        paginator = pagination_class()
        paginator.page_size = resolve_page_size()

        self._paginator = paginator
        return paginator.paginate_queryset(queryset, self.request, view=self)

    # ------------------------------------------------------------------
    # Filtering Handling
    # ------------------------------------------------------------------
    def get_filter_backends(self):
        if "filter_backends" in self.__class__.__dict__:
            return self.filter_backends

        return resolve_filter_backends()
    
    def filter_queryset(self, queryset):
        """
        Apply configured filter backends deterministically.
        """
        if "filter_backends" in self.__class__.__dict__:
            backends = self.filter_backends
        else:
            backends = resolve_filter_backends()

        for backend in backends:
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset
