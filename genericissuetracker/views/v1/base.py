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
"""

from rest_framework import viewsets

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
    permission_classes = []

    def get_serializer_class(self):
        """
        Always return the read serializer.

        Enforces deterministic schema.
        """
        if not self.read_serializer_class:
            raise AssertionError(
                "Read-only ViewSet must define `read_serializer_class`."
            )

        return self.read_serializer_class

    def get_permissions(self):
        """
        Resolve permission classes.

        Priority:
            1. Explicit `permission_classes` defined on ViewSet
            2. Configured DEFAULT_PERMISSION_CLASSES
        """
        print(">>> USING CUSTOM PERMISSION RESOLVER <<<")
        
        if "permission_classes" in self.__class__.__dict__:
            return [permission() for permission in self.permission_classes]

        default_permissions = resolve_default_permission_classes()
        return [permission() for permission in default_permissions]


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

    Serializer Selection Rules:
        - list/retrieve → read_serializer_class
        - create/update/partial_update/destroy → write_serializer_class

    Permission Rules:
        - Uses configured default permissions
          unless explicitly overridden.
    """

    read_serializer_class = None
    write_serializer_class = None
    permission_classes = []

    def get_serializer_class(self):
        """
        Deterministic serializer selection based on action.
        """
        if self.action in ["list", "retrieve"]:
            if not self.read_serializer_class:
                raise AssertionError(
                    "CRUD ViewSet must define `read_serializer_class`."
                )
            return self.read_serializer_class

        if self.action in ["create", "update", "partial_update", "destroy"]:
            if not self.write_serializer_class:
                raise AssertionError(
                    "CRUD ViewSet must define `write_serializer_class`."
                )
            return self.write_serializer_class

        raise AssertionError(
            f"Unhandled action '{self.action}' in {self.__class__.__name__}."
        )

    def get_permissions(self):
        """
        Resolve permission classes.

        Priority:
            1. Explicit `permission_classes` defined on ViewSet
            2. Configured DEFAULT_PERMISSION_CLASSES
        """
        if getattr(self, "permission_classes", None):
            return [permission() for permission in self.permission_classes]

        default_permissions = resolve_default_permission_classes()
        return [permission() for permission in default_permissions]
