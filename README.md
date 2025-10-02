# Cookiecutter Zelos Extension Template

A production-ready [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for building Python-based [Zelos](https://zeloscloud.io) extensions. This template generates a complete extension project with best practices, tooling, and marketplace-ready packaging.

> **Note**: This is the template repository. The generated projects will have their own structure and documentation focused on end-users.

## ✨ What You Get

This template generates a complete Zelos extension project with:

### Extension Essentials
- ✅ **Valid `extension.toml`** - Complete manifest with all required fields and documentation
- ✅ **Working example** - Functional `main.py` that streams data via `zelos-sdk`
- ✅ **Configuration UI** - JSON Schema for user settings in the Zelos App
- ✅ **Interactive actions** - Example actions for runtime control

### Developer Experience
- ⚡ **[UV](https://github.com/astral-sh/uv)** - Lightning-fast dependency management
- 🎨 **Code quality tools** - Ruff (linting + formatting), ty (type checking), pytest
- 🔄 **Pre-commit hooks** - Automatic code quality checks on every commit
- 📋 **Just commands** - Simple, memorable commands (`just dev`, `just test`, etc.)

### Production Ready
- 🚀 **GitHub Actions CI/CD** - Automated testing and releases
- 📦 **Marketplace packaging** - Correct tarball format for Zelos marketplace
- 📝 **Professional docs** - Marketplace-focused README, developer-focused CONTRIBUTING
- 🔖 **Version management** - Automated version bumping and git tagging

## 📋 Prerequisites

To use this template and develop extensions:

- **Python 3.10+**
- **[Cookiecutter](https://github.com/cookiecutter/cookiecutter)** (or use `uvx` to run without installing)
- **[UV](https://github.com/astral-sh/uv)** - For dependency management in generated projects
- **[Just](https://github.com/casey/just)** - For running development commands (e.g., `brew install just` on macOS)

## 🚀 Quick Start

### 1. Generate Your Extension Project

```bash
uvx cookiecutter https://github.com/zeloscloud/cookiecutter-zelos-extension.git
```

You will be prompted for:

- `author` – your display name (e.g., "Jane Doe")
- `email` – contact email (e.g., "jane@example.com")
- `author_github_handle` – GitHub username (e.g., "janedoe")
- `project_name` – extension name in kebab-case (e.g., "sensor-monitor")
- `project_description` – short summary (auto-generated from project name if skipped)

The template automatically derives:

- `publisher_id` – sanitized GitHub handle (`janedoe` → `janedoe`)
- `extension_id` – `publisher.project-name` (e.g., `janedoe.sensor-monitor`)
- `project_slug` – Python package import name (e.g., `sensor_monitor`)
- `python_version` – defaults to `3.11`

### 2. Start Developing

```bash
cd my-zelos-extension

just install          # Install dependencies and pre-commit hooks
just dev              # Run extension locally
just check            # Run linting and type checking
just test             # Run tests
```

The template automatically initializes a git repository for you.

### 3. Create a Release

```bash
just release 1.0.0    # Update version, run checks, create tag
git push origin main v1.0.0
```

The GitHub Actions workflow automatically:
- Validates the version
- Runs all checks and tests
- Packages the extension as a tarball
- Creates a GitHub release with assets

### 4. Publish to Marketplace

Submit your repository at <https://marketplace.zeloscloud.io>. After approval, users can install your extension directly in the Zelos App.

## 📁 Generated Project Structure

```
my-zelos-extension/
├── extension.toml              # Zelos manifest
├── main.py                     # Entry point
├── config.schema.json          # Configuration UI schema
├── pyproject.toml              # Dependencies and metadata
├── my_zelos_extension/
│   ├── __init__.py
│   ├── extension.py            # Extension class with actions
│   └── utils/
│       └── config.py           # Configuration loader
├── tests/
│   └── test_config.py
├── assets/
│   └── icon.svg                # Extension icon
├── scripts/
│   └── package_extension.py    # Packaging script
├── Justfile                    # Commands: install/dev/check/test/release/package
├── CONTRIBUTING.md             # Developer documentation
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI on main
│       └── release.yml         # Release on tags
└── .pre-commit-config.yaml
```

## 🛠️ Available Commands

The generated project includes these `just` commands for development:

- **`just install`** - Install dependencies and pre-commit hooks
- **`just dev`** - Run the extension locally for testing
- **`just check`** - Run ruff and ty
- **`just test`** - Run pytest
- **`just format`** - Format code with ruff
- **`just release VERSION`** - Update version, run checks, and create git tag
- **`just package`** - Create tarball for marketplace

All dependencies are managed by UV and locked in `uv.lock`.

### Documentation in Generated Projects

Each generated project includes:
- **README.md** - Marketplace-focused documentation for end-users
- **CONTRIBUTING.md** - Comprehensive developer guide for contributors
- **CHANGELOG.md** - Version history following Keep a Changelog format

## 🧪 Testing the Template

Before releasing changes to this template, verify it generates working projects:

```bash
git clone https://github.com/zeloscloud/cookiecutter-zelos-extension.git
cd cookiecutter-zelos-extension

# Test generation
uvx cookiecutter . --no-input

# Verify the generated project
cd my-zelos-extension
just install && just check && just test && just package
```

## 🤝 Contributing to This Template

Contributions are welcome! To contribute:

1. Fork this repository
2. Make your changes to the template files
3. Test the generation (see "Testing the Template" above)
4. Submit a Pull Request with a clear description

Please ensure:
- Generated projects work out of the box
- All `just` commands function correctly
- Documentation is clear and accurate
- CI workflows pass

## 📄 License

MIT License - see [LICENSE](LICENSE)

Generated projects inherit this license by default, but can be changed by the user.

## 📚 Resources

- **[Zelos Documentation](https://docs.zeloscloud.io)** - Full extension development guide
- **[Zelos SDK on PyPI](https://pypi.org/project/zelos-sdk/)** - Python SDK for data streaming
- **[UV Documentation](https://docs.astral.sh/uv/)** - Fast Python package manager
- **[Just Documentation](https://just.systems/)** - Command runner
- **[Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)** - Project templating

## 💡 Template Variables

When you run `cookiecutter`, you'll be prompted for these values:

| Variable | Description | Example |
|----------|-------------|---------|
| `author` | Your display name | John Doe |
| `email` | Contact email | john@example.com |
| `author_github_handle` | GitHub username | johndoe |
| `project_name` | Extension name (kebab-case) | sensor-monitor |
| `project_description` | Short description | Real-time sensor data monitoring |
| `python_version` | Python version to use | 3.11 |

**Derived automatically:**
- `publisher_id` - Sanitized GitHub handle (used in extension ID)
- `extension_id` - Full extension ID (`publisher.project-name`)
- `project_slug` - Python package name (`sensor_monitor`)
