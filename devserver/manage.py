#!/usr/bin/env python
"""
Lightweight development server for genericissuetracker.

This project exists ONLY for local testing and development.
It must never be pushed to GitHub or packaged to PyPI.
"""

import os
import sys
from pathlib import Path


def main():
    # Add the parent directory to sys.path so genericissuetracker can be found
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devserver.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
