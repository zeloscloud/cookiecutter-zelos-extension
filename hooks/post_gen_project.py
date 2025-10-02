#!/usr/bin/env python
"""Post-generation hook."""

from __future__ import annotations

import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def run_command(cmd: list[str], description: str, critical: bool = False) -> bool:
    """Run a command and handle errors gracefully.

    :param cmd: Command and arguments to execute
    :param description: Human-readable description of the command
    :param critical: Whether failure should be treated as critical
    :return: True if command succeeded, False otherwise
    """
    try:
        subprocess.run(
            cmd, cwd=PROJECT_DIRECTORY, check=True, capture_output=True, text=True
        )
        print(f"✓ {description}")
        return True
    except subprocess.CalledProcessError as e:
        if critical:
            print(f"✗ {description} failed: {e.stderr}")
            return False
        else:
            print(f"⚠ {description} skipped (optional)")
            return False
    except FileNotFoundError:
        print(f"⚠ {description} skipped (command not found)")
        return False


def compile_requirements() -> bool:
    """Compile initial requirements.txt from pyproject.toml.

    :return: True if successful, False otherwise
    """
    return run_command(
        ["uv", "pip", "compile", "pyproject.toml", "-o", "requirements.txt"],
        "Created requirements.txt",
        critical=False,
    )


def initialize_git() -> bool:
    """Initialize git repository.

    :return: True if successful, False otherwise
    """
    return run_command(
        ["git", "init", "-b", "main"],
        "Initialized git repository",
        critical=False,
    )


def install_dependencies() -> bool:
    """Install dependencies (including dev extras) if uv is available.

    :return: True if successful, False otherwise
    """
    return run_command(
        ["uv", "sync", "--extra", "dev"],
        "Installed dependencies (dev)",
        critical=False,
    )


if __name__ == "__main__":
    print(f"\n🚀 Setting up {os.path.basename(PROJECT_DIRECTORY)}")
    print("-" * 40)

    # Initialize git repository
    initialize_git()

    # Try to compile requirements.txt
    if not compile_requirements():
        print("  → Run 'just install' to generate requirements.txt")

    # Try to install dependencies
    if not install_dependencies():
        print("  → Run 'just install' to install dependencies")

    print("-" * 40)
    print("\n📦 Next steps:")
    print("  1. cd {}".format(os.path.basename(PROJECT_DIRECTORY)))
    print("  2. just install    # Install dependencies and pre-commit hooks")
    print("  3. just dev        # Run the extension locally")
    print("\n⚠️  Important:")
    print("  - Develop locally BEFORE installing in Zelos")
    print("  - If you get venv errors, run: rm -rf .venv && just install")
    print("\n📚 Documentation:")
    print("  - See CONTRIBUTING.md for development workflow")
    print("  - See README.md for usage instructions")
    print("  - Run 'just' to see all available commands\n")
