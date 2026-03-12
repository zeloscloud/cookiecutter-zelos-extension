from __future__ import annotations

import re
import sys


def validate(value: str, pattern: str, error_msg: str) -> None:
    """Exit with error if value doesn't match pattern."""
    if not re.match(pattern, value):
        print(f"ERROR: {error_msg}")
        sys.exit(1)


email = "{{cookiecutter.email}}"
validate(email, r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
         f"The email '{email}' is not valid. Please use a valid email format (e.g., 'you@example.com').")

project_name = "{{cookiecutter.project_name}}"
validate(project_name, r"^[a-zA-Z][-a-zA-Z0-9]+$",
         f"The project name '{project_name}' must contain only letters, numbers, or hyphens (start with a letter).")

project_slug = "{{cookiecutter.project_slug}}"
validate(project_slug, r"^[_a-zA-Z][_a-zA-Z0-9]+$",
         f"The project slug '{project_slug}' must be a valid Python identifier (use underscores, not hyphens).")

python_version = "{{cookiecutter.python_version}}"
validate(python_version, r"^3\.\d+$",
         f"The Python version '{python_version}' must be in major.minor format (e.g. '3.11').")

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
