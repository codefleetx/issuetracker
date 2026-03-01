# Changelog

All notable changes to this project will be documented here.

This project follows Semantic Versioning.

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