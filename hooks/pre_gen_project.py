from __future__ import annotations

import re
import sys

# Validate email format
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
email = "{{cookiecutter.email}}"
if not re.match(EMAIL_REGEX, email):
    print(
        f"ERROR: The email '{email}' is not valid. Please use a valid email format (e.g., 'you@example.com')."
    )
    sys.exit(1)

PROJECT_NAME_REGEX = r"^[a-zA-Z][-a-zA-Z0-9]+$"
project_name = "{{cookiecutter.project_name}}"
if not re.match(PROJECT_NAME_REGEX, project_name):
    print(
        f"ERROR: The project name '{project_name}' must contain only letters, numbers, or hyphens (start with a letter)."
    )
    sys.exit(1)

PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
project_slug = "{{cookiecutter.project_slug}}"
if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"ERROR: The project slug '{project_slug}' must be a valid Python identifier (use underscores, not hyphens)."
    )
    sys.exit(1)

# Python version validation - must be 3.10+ for zelos-sdk
PYTHON_VERSION_REGEX = r"^3\.\d+$"
python_version = "{{cookiecutter.python_version}}"
if not re.match(PYTHON_VERSION_REGEX, python_version):
    print(
        f"ERROR: The Python version '{python_version}' must be in major.minor format (e.g. '3.11')."
    )
    sys.exit(1)

# Validate minimum version requirement (zelos-sdk needs Python >= 3.10)
major, minor = map(int, python_version.split("."))
if minor < 10:
    print(
        f"ERROR: Python version must be >= 3.10 (got {python_version}). The zelos-sdk requires Python 3.10 or higher."
    )
    sys.exit(1)
if minor > 14:
    print(
        f"WARNING: Python {python_version} is newer than officially supported (3.10-3.14). It may work but is untested."
    )
