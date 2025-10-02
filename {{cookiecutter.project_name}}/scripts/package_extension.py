#!/usr/bin/env python3
"""Package the Zelos extension into a tar.gz archive."""

import subprocess
import sys
import tarfile
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore


def filter_archive_files(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
    """Filter out unwanted files from archive per Zelos security requirements.

    :param tarinfo: Tar member info
    :return: None if should be excluded, tarinfo otherwise
    """
    # Skip Python cache files
    if "__pycache__" in tarinfo.name or tarinfo.name.endswith((".pyc", ".pyo")):
        return None

    # Skip hidden files/directories (security requirement)
    parts = Path(tarinfo.name).parts
    if any(part.startswith(".") for part in parts):
        return None

    # Ensure no symlinks or special files (security requirement)
    if tarinfo.issym() or tarinfo.islnk():
        print(f"WARNING: Skipping symlink: {tarinfo.name}")
        return None
    if not (tarinfo.isfile() or tarinfo.isdir()):
        print(f"WARNING: Skipping special file: {tarinfo.name}")
        return None

    return tarinfo


def main() -> None:
    """Package the extension."""
    # Load manifest
    try:
        with Path("extension.toml").open("rb") as f:
            manifest = tomllib.load(f)
    except FileNotFoundError:
        print("ERROR: extension.toml not found")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to parse extension.toml: {e}")
        sys.exit(1)

    version = manifest.get("version")
    if not version:
        print("ERROR: No version in extension.toml")
        sys.exit(1)

    # Ensure requirements.txt exists
    if not Path("requirements.txt").exists():
        print("Compiling requirements.txt...")
        result = subprocess.run(
            ["uv", "pip", "compile", "pyproject.toml", "-o", "requirements.txt"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("ERROR: Failed to compile requirements.txt")
            print(result.stderr)
            sys.exit(1)

    # Collect files to package
    files = ["extension.toml"]  # Always required

    # Add runtime files from manifest
    runtime = manifest.get("runtime", {})
    if "entry" in runtime:
        files.append(runtime["entry"])
    if "requirements" in runtime:
        files.append(runtime["requirements"])

    # Add optional files referenced in manifest
    for key in ["icon", "readme", "changelog"]:
        if key in manifest:
            files.append(manifest[key])

    # Add config schema if present
    config = manifest.get("config", {})
    if "schema" in config:
        files.append(config["schema"])

    # Add Python packages from src/ directory
    src_dir = Path("src")
    if src_dir.exists():
        for path in src_dir.iterdir():
            if (
                path.is_dir()
                and (path / "__init__.py").exists()
                and path.name not in ["tests", "test", "__pycache__"]
            ):
                files.append(f"src/{path.name}")

    # Also check root for any packages (backwards compatibility)
    for path in Path().iterdir():
        if (
            path.is_dir()
            and path.name not in ["src", "tests", "test", "__pycache__", ".vscode", ".github"]
            and (path / "__init__.py").exists()
        ):
            files.append(path.name)

    # Create archive
    project_name = Path.cwd().name
    archive_name = f"{project_name}-v{version}.tar.gz"

    print(f"Creating {archive_name}...")
    print("Packaging files for Zelos marketplace...")

    with tarfile.open(archive_name, "w:gz") as tar:
        for file_path in sorted(set(files)):
            path = Path(file_path)
            if not path.exists():
                print(f"ERROR: Required file missing: {file_path}")
                sys.exit(1)

            tar.add(file_path, arcname=file_path, filter=filter_archive_files)
            print(f"  + {file_path}")

    # Verify archive size constraints
    archive_path = Path(archive_name)
    size_bytes = archive_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    # Check against Zelos marketplace limits
    MAX_SIZE_MB = 500
    if size_mb > MAX_SIZE_MB:
        print(f"\n❌ ERROR: Archive too large ({size_mb:.1f} MB > {MAX_SIZE_MB} MB limit)")
        sys.exit(1)

    print(f"\n✓ Package created: {archive_name}")
    print(f"  Size: {size_kb:.1f} KB ({size_mb:.2f} MB)")
    print("  Ready for marketplace submission!")


if __name__ == "__main__":
    main()
