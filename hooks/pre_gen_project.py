from __future__ import annotations

import re
import sys

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

PYTHON_VERSION_REGEX = r"^\d+\.\d+$"
python_version = "{{cookiecutter.python_version}}"
if not re.match(PYTHON_VERSION_REGEX, python_version):
    print(
        f"ERROR: The Python version '{python_version}' must be in major.minor format (e.g. '3.11')."
    )
    sys.exit(1)
