"""
genericissuetracker.urls.root
=============================

Root URL configuration for Generic Issue Tracker.

Purpose
-------
Expose versioned API structure:

    /api/v1/

Host project integration example:

    path("api/", include("genericissuetracker.urls.root"))
"""

from django.urls import include, path

urlpatterns = [
    path("v1/", include("genericissuetracker.urls.v1")),
]
