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

4. No implicit fallback serializers.
"""

from rest_framework import viewsets


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
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        """
        Deterministic serializer selection based on action.

        This avoids:
            • dynamic schema switching
            • request-based serializer changes
            • OpenAPI ambiguity
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

        # Explicit failure for unknown actions
        raise AssertionError(
            f"Unhandled action '{self.action}' in {self.__class__.__name__}."
        )
