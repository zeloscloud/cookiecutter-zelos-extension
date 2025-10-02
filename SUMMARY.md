# Cookiecutter Zelos Extension - Template Summary

A production-ready cookiecutter template for building Python-based Zelos extensions. This document summarizes the template structure and its documentation strategy.

## Documentation Philosophy

This template generates projects with **three distinct types of documentation**, each serving a different audience:

### 1. Marketplace Documentation (Generated README.md)
**Audience**: End-users browsing the Zelos marketplace

**Purpose**: Convince users to install and use the extension

**Focus**:
- ✅ What the extension does
- ✅ Key features and benefits
- ✅ Configuration options
- ✅ Quick start for users
- ✅ Data formats and outputs
- ❌ No development details
- ❌ No build instructions
- ❌ No tooling information

**Example sections**: Features, Quick Start, Configuration, Actions, Data Format, Requirements

### 2. Developer Documentation (Generated CONTRIBUTING.md)
**Audience**: Contributors and developers working on the extension

**Purpose**: Enable developers to set up, modify, and contribute to the extension

**Focus**:
- ✅ Development environment setup
- ✅ Project structure explanation
- ✅ Testing and debugging
- ✅ Code style guidelines
- ✅ Release process
- ✅ All `just` commands
- ✅ How to add features
- ❌ Not for end-users

**Example sections**: Development Setup, Testing, Project Structure, Code Style, Releasing, Debugging

### 3. Template Documentation (Root README.md)
**Audience**: Extension authors using this template

**Purpose**: Explain how to use the cookiecutter template to generate extensions

**Focus**:
- ✅ How to generate a project
- ✅ Template variables
- ✅ What the template provides
- ✅ Testing the template itself
- ❌ Not about using generated extensions

## Template Structure

```
cookiecutter-zelos-extension/
├── cookiecutter.json            # Template variables and defaults
├── hooks/
│   ├── pre_gen_project.py       # Validates naming and Python version
│   └── post_gen_project.py      # Initializes git repository
├── {{cookiecutter.project_name}}/   # Generated project files
│   ├── extension.toml           # Extension manifest
│   ├── main.py                  # Entry point
│   ├── config.schema.json       # Configuration schema
│   ├── pyproject.toml           # Python dependencies (UV)
│   ├── Justfile                 # Development commands
│   ├── README.md                # 📖 MARKETPLACE-FOCUSED (for users)
│   ├── CONTRIBUTING.md          # 🛠️ DEVELOPER-FOCUSED (for contributors)
│   ├── CHANGELOG.md             # 📝 VERSION HISTORY (for everyone)
│   ├── {{cookiecutter.project_slug}}/
│   │   ├── extension.py         # Extension class
│   │   └── utils/config.py      # Configuration utilities
│   ├── tests/                   # Test suite
│   ├── assets/icon.svg          # Extension icon
│   ├── scripts/package_extension.py
│   ├── .github/workflows/
│   │   ├── ci.yml               # CI on pushes/PRs
│   │   └── release.yml          # Release on tags
│   └── .pre-commit-config.yaml
├── README.md                    # 🔧 TEMPLATE USAGE (this file, for template users)
├── SUMMARY.md                   # 📋 Template summary (you are here)
└── LICENSE                      # MIT License
```

## Key Features

- **Production-ready**: Complete setup with tooling, CI/CD, and packaging
- **Best practices**: Ruff for linting/formatting, pytest for testing, pre-commit hooks
- **Marketplace-optimized**: Correct documentation focus, packaging format
- **Developer-friendly**: Just commands for all common tasks
- **Automated releases**: GitHub Actions with version validation

## Generated Documentation Examples

### ❌ Bad README.md (Too Developer-Focused)
```markdown
## Quick Start
\`\`\`bash
just install
just dev
just test
\`\`\`
```
This is wrong for the marketplace - users don't care about `just` commands!

### ✅ Good README.md (Marketplace-Focused)
```markdown
## Quick Start
1. Install the extension in your Zelos App
2. Configure your settings
3. Start streaming data
```
This is correct - it tells users what to do, not developers.

### ✅ Good CONTRIBUTING.md (Developer-Focused)
```markdown
## Development Workflow
\`\`\`bash
just install
just dev
just test
\`\`\`
```
Perfect! Development commands belong in CONTRIBUTING.md.

## Quality Checklist

When maintaining this template, ensure:

- [ ] Generated README.md is marketplace-focused (no development details)
- [ ] Generated CONTRIBUTING.md is comprehensive for developers
- [ ] Generated CHANGELOG.md follows Keep a Changelog format
- [ ] Root README.md explains template usage clearly
- [ ] All `just` commands work in generated projects
- [ ] CI/CD workflows pass
- [ ] Packaging produces correct tarball format
- [ ] Linting passes (ruff)
- [ ] Tests pass (pytest)

## Testing the Template

```bash
# Generate a test project
uvx cookiecutter . --no-input

# Verify it works
cd my-zelos-extension
just install && just check && just test && just package

# Review the documentation
cat README.md         # Should be marketplace-focused
cat CONTRIBUTING.md   # Should be developer-focused
cat CHANGELOG.md      # Should be version history
```

## Maintenance Notes

When updating this template:

1. **README.md changes**: Focus on end-user value, remove dev details
2. **CONTRIBUTING.md changes**: Add more developer details, keep comprehensive
3. **CHANGELOG.md changes**: Follow Keep a Changelog format strictly
4. **Root README.md changes**: Keep template usage instructions clear
5. **Always test generation**: Run the test commands above before committing
