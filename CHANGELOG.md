# Changelog

All notable changes to this project will be documented here.

This project follows Semantic Versioning.

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