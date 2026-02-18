# Generic Issue Tracker

![PyPI](https://img.shields.io/pypi/v/genericissuetracker)
![Python](https://img.shields.io/pypi/pyversions/genericissuetracker)
![License](https://img.shields.io/pypi/l/genericissuetracker)
![Django](https://img.shields.io/badge/django-4.2-green)

A production-grade, reusable, installable Django Issue Tracking library.

---

## 🚀 Overview

GenericIssueTracker is a versioned, schema-safe, soft-delete-compatible issue tracking engine designed to integrate into any Django application.

It provides:

- Issue management
- Comments
- Labels
- Attachments
- Human-friendly issue numbers
- Versioned REST API
- Configurable permissions
- Configurable pagination
- Configurable filtering
- OpenAPI schema support (drf-spectacular compatible)

Designed for:

- SaaS platforms
- Internal tools
- Public open-source issue hubs
- Enterprise-grade Django systems

---

## 🏗 Architecture

### Layered Design

```
Models (Domain)
    ↓
Services (Identity / Permissions / Pagination / Filtering)
    ↓
Serializers (Validation & Representation)
    ↓
Versioned Views
    ↓
Versioned URLs
    ↓
OpenAPI Schema
```

### Design Principles

- No dependency on AUTH_USER_MODEL
- Soft delete first-class
- UUID internal identity
- Sequential issue_number public identity
- Strict versioning (`/api/v1/`)
- Deterministic schema
- Zero business logic in views
- Fat serializers, thin views
- No runtime schema mutation

---

## 📦 Installation

```bash
pip install genericissuetracker
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "genericissuetracker",
]
```

Include URLs:

```python
path("api/", include("genericissuetracker.urls.root")),
```

---

## 🛠 Required Dependencies

- Django >= 4.2
- djangorestframework >= 3.14
- drf-spectacular >= 0.27

---

## ⚙ Configuration

All settings are namespaced:

```python
GENERIC_ISSUETRACKER_<SETTING>
```

### Available Settings

| Setting | Description |
|----------|-------------|
| IDENTITY_RESOLVER | Custom identity resolver path |
| ALLOW_ANONYMOUS_REPORTING | Allow anonymous issue creation |
| MAX_ATTACHMENTS | Max attachments per issue |
| MAX_ATTACHMENT_SIZE_MB | Max file size |
| DEFAULT_PERMISSION_CLASSES | Default DRF permissions |
| DEFAULT_PAGINATION_CLASS | Pagination class |
| PAGE_SIZE | Pagination size |
| DEFAULT_FILTER_BACKENDS | Filtering backends |

Example:

```python
GENERIC_ISSUETRACKER_DEFAULT_PERMISSION_CLASSES = [
    "rest_framework.permissions.IsAuthenticated"
]
```

---

## 🔐 Identity Model

Reporter is stored as:

- reporter_email
- reporter_user_id (optional)

No direct ForeignKey to user model.

---

## 🧾 Issue Identifiers

- `id` → UUID (internal)
- `issue_number` → Sequential public identifier

Example:

```
/api/v1/issues/12/
```

---

## 📚 API Endpoints

### Issues

| Method | Endpoint |
|--------|----------|
| GET | /api/v1/issues/ |
| GET | /api/v1/issues/{issue_number}/ |
| POST | /api/v1/issues/ |
| PUT | /api/v1/issues/{issue_number}/ |
| PATCH | /api/v1/issues/{issue_number}/ |
| DELETE | /api/v1/issues/{issue_number}/ |

### Comments

```
/api/v1/comments/
```

### Labels

```
/api/v1/labels/
```

### Attachments

```
/api/v1/attachments/
```

---

## 🔎 Filtering

Supports:

- SearchFilter
- OrderingFilter

Example:

```
/api/v1/issues/?search=bug
/api/v1/issues/?ordering=-created_at
```

---

## 📄 Pagination

Configurable via:

```
GENERIC_ISSUETRACKER_PAGE_SIZE
```

---

## 📖 OpenAPI Schema

Fully compatible with drf-spectacular.

```
/schema/
/docs/
```

---

## 🧪 Development

Install dev tools:

```bash
pip install -e ".[dev]"
ruff check .
```

---

## 🧩 Integration Guide

1. Install package
2. Add to INSTALLED_APPS
3. Include URLs
4. Configure permissions
5. Run migrations
6. Start creating issues

---

## 🧱 Versioning Policy

- Minor releases: new features (backward compatible)
- Patch releases: internal improvements
- Major releases: breaking changes

---

## 📜 License

MIT License.

---

## 👤 Maintainer

BinaryFleet

---

## 🌟 Contributing

Pull requests welcome.
Follow:

- DRY principles
- Schema determinism
- Versioned serializers
- No business logic in views
