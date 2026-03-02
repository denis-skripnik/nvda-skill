# OpenClaw NVDA Skill

This skill packages a practical workflow for building, debugging, and packaging
NVDA add-ons from concrete feature requests.

## What It Includes

- `SKILL.md`: the primary instructions for `/nvda`
- `references/`: workflow, troubleshooting, and practical guide documents
- `assets/templates/`: reusable add-on project templates
- `scripts/bootstrap_addon.py`: project scaffolding script

## Safety Rule for File Creation

By default, the skill should not create files above the `nvda/` skill
directory.

The bundled bootstrap script enforces this behavior for relative paths:

- relative `output_dir` values are resolved inside `nvda/`
- relative paths that try to escape `nvda/` are rejected
- absolute paths are allowed when an agent or user intentionally targets a
  specific repository structure

## Bootstrap Usage

Generate a project inside the skill directory:

```bash
python nvda/scripts/bootstrap_addon.py generated/myAddon myAddon "My Addon"
```

That command creates:

- `nvda/generated/myAddon/buildVars.py`
- `nvda/generated/myAddon/manifest.ini.tpl`
- `nvda/generated/myAddon/build_addon.py`
- `nvda/generated/myAddon/addon/...`

The generated project's build script writes the package to its own local
`dist/` directory:

```text
nvda/generated/myAddon/dist/
```

If a project must be created elsewhere, pass an explicit absolute path.
