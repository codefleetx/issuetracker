"""
genericissuetracker.urls.v1
===========================

Version 1 API routing configuration.

Purpose
-------
Register all v1 endpoints under:

    /api/v1/

Design Principles
-----------------
- URL-based versioning.
- Explicit router registration.
- No nested routers in v1.
- Deterministic endpoint structure.
"""

from rest_framework.routers import DefaultRouter

from genericissuetracker.views.v1.crud.attachment import AttachmentCRUDViewSet
from genericissuetracker.views.v1.crud.comment import CommentCRUDViewSet
from genericissuetracker.views.v1.crud.issue import IssueCRUDViewSet
from genericissuetracker.views.v1.crud.label import LabelCRUDViewSet
from genericissuetracker.views.v1.read.attachment import AttachmentReadViewSet
from genericissuetracker.views.v1.read.comment import CommentReadViewSet
from genericissuetracker.views.v1.read.issue import IssueReadViewSet
from genericissuetracker.views.v1.read.label import LabelReadViewSet

router = DefaultRouter()

# ----------------------------------------------------------------------
# ISSUE ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"issues", IssueCRUDViewSet, basename="issue")
router.register(r"issues-read", IssueReadViewSet, basename="issue-read")

# ----------------------------------------------------------------------
# COMMENT ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"comments", CommentCRUDViewSet, basename="comment")
router.register(r"comments-read", CommentReadViewSet, basename="comment-read")

# ----------------------------------------------------------------------
# LABEL ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"labels", LabelCRUDViewSet, basename="label")
router.register(r"labels-read", LabelReadViewSet, basename="label-read")

# ----------------------------------------------------------------------
# ATTACHMENT ENDPOINTS
# ----------------------------------------------------------------------
router.register(r"attachments", AttachmentCRUDViewSet, basename="attachment")
router.register(r"attachments-read", AttachmentReadViewSet, basename="attachment-read")


urlpatterns = router.urls
