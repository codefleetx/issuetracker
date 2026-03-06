# Changelog

All notable changes to this project will be documented here.

This project follows Semantic Versioning.

---

## [0.6.1] - 2026-03-06

### Timeline Ready Issue Status History

### Added
- `event_type` field in `IssueStatusHistory` for machine-readable lifecycle event classification
- `metadata` JSON field allowing structured contextual data for lifecycle transitions
- Composite index `(issue, created_at)` optimized for timeline queries

### Changed
- `change_issue_status()` lifecycle service now accepts optional parameters:
  - `event_type`
  - `metadata`
- Status history events now support extensible event semantics while preserving existing lifecycle behavior

### Improvements
- `IssueStatusHistory` now acts as a timeline-ready lifecycle event store
- Enables integrations, automation triggers, and analytics pipelines without requiring future schema migrations
- Optimized database performance for issue timeline queries

### Compatibility
- Fully backward compatible
- Existing events automatically behave as:
  - `event_type = "status_changed"`
  - `metadata = {}`

### Migration Notes
- Migration adds two fields to `IssueStatusHistory`:
  - `event_type`
  - `metadata`
- Adds composite index `(issue, created_at)`
- No data migration required

---

## [0.6.0] - 2026-03-02

### ✨ Added
- Atomic issue creation with attachments (API v1).
- `files` field added to IssueCreateSerializer (optional).
- Attachments can now be uploaded during issue creation using multipart/form-data.
- Attachments validated using existing MAX_ATTACHMENTS and MAX_ATTACHMENT_SIZE_MB settings.
- attachment_added signal emitted per uploaded file.

### 🔒 Improved
- Issue + attachments creation wrapped in transaction.atomic().
- Strict anti-spoofing identity enforcement preserved.

### 🧪 Behavior
- Fully backward compatible.
- No database migrations required.
- No breaking API changes.
- Deterministic OpenAPI schema maintained.

---

## [0.5.3] - 2026-03-02

### Added

* Comment-linked attachments (optional `comment` FK on `IssueAttachment`)
* Uploader identity tracking (`uploaded_by_user_id`, `uploaded_by_email`)
* Atomic comment + attachment creation via multipart/form-data
* Serializer-level issue/comment consistency validation
* Comment-aware `attachment_added` signal payload
* Support for referencing `Issue` via `issue_number` instead of UUID in write endpoints

### Changed

* Comment create endpoint now accepts optional `files[]`
* Attachment upload automatically injects uploader identity
* Write serializers now resolve `Issue` using `issue_number` (numeric) instead of UUID
* OpenAPI schema updated for multipart support

### Migration Notes

* Staged migration for new attachment fields:

  1. Add nullable fields
  2. Backfill historical rows
  3. Enforce NOT NULL on `uploaded_by_email`

### Backward Compatibility

* No endpoint removed
* UUID primary keys unchanged
* Numeric public identifiers unchanged
* Existing integrations remain functional

---

## [0.5.2] - 2026-03-01

### Added
- Sequential public `number` field for:
  - IssueComment
  - IssueAttachment
  - Label
- Attachment lifecycle signals:
  - attachment_added
  - attachment_deleted
- MAX_COMMENT_LENGTH setting (default: 10,000)

### Changed
- API routing now resolves by `number` instead of UUID for:
  - comments
  - attachments
  - labels
- Comment body now enforces database-level max_length=10000

### Migration Notes
- Two-step migration for numeric identifiers
- UUID primary keys remain unchanged
- UUID-based URLs are no longer supported

---

## [0.5.0] - 2026-02-21

### Added
- Lifecycle state machine with transition matrix
- Reopen support (`RESOLVED → OPEN`, `CLOSED → OPEN`)
- `IssueStatusHistory` model for lifecycle audit trail
- Atomic transaction wrapper for status transitions
- Dedicated service layer for lifecycle operations
- Pluggable transition policy hook (`GENERIC_ISSUETRACKER_TRANSITION_POLICY`)
- Strict validation preventing same-to-same transitions
- Custom `/change-status/` endpoint (v1 API)

### Changed
- Status transitions now enforced through deterministic state machine
- Status change logic moved from ViewSet into service layer
- Status updates no longer allowed via generic update endpoints
- Transition validation now returns 400 for illegal or redundant transitions

### Security
- Prevented no-op transitions from polluting audit history
- Ensured lifecycle updates are atomic and rollback-safe

---

## [0.4.3] - 2026-02-20

### Fixed
- Corrected PUT update behavior (PUT disabled, PATCH enforced).
- Fixed serializer behavior for update without reporter_email.
- Clarified identity injection for authenticated comment creation.
- Ensured permission-based form visibility in Browsable API.

---

## [0.4.2] - 2026-02-18

### 🚀 First Public Enterprise Release
GenericIssueTracker is now publicly available on PyPI.
Highlights:

- Versioned API architecture (v1)
- Schema-safe DRF implementation
- Soft delete foundation
- Sequential human-friendly issue_number
- Configurable permission architecture
- Pagination + filtering
- OpenAPI integration (drf-spectacular)
- CI workflow enabled
- PyPI distribution ready

---

## [0.4.1] - 2026-02-18

### Added
- Sequential `issue_number` field
- Human-friendly issue lookup
- Pagination architecture
- Filtering architecture
- Permission abstraction layer
- OpenAPI schema hardening
- CI workflow
- Production-ready README

### Changed
- Lookup field switched from UUID to issue_number
- Improved PyPI metadata

---

## [0.4.0]

- Pagination support
- Filtering support
- Schema grouping
- Operation IDs standardized

---

## [0.3.0]

- Configurable permission architecture

---

## [0.2.0]

- Versioned serializers
- CRUD + read view separation

---

## [0.1.0]

- Initial domain foundation
- Soft delete
- Signals
- Identity abstraction