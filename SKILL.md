---
name: nvda
description: Practical workflow for creating, updating, debugging, and packaging NVDA add-ons from concrete feature requests. Use when working on global plugins, app modules, gestures, settings panels, manifests, build scripts, `.nvda-addon` packaging, or NVDA runtime failures during add-on development. Use this skill for `/nvda` requests about add-on development.
---

# OpenClaw NVDA Add-on

Use this skill to turn a feature request into a working NVDA add-on, not into a
theoretical design document.

## Workflow

1. Read `references/workflow.md`.
2. Read `references/practical-guide.md` before writing code.
3. Write down the user-visible behavior first:
   - gesture or trigger
   - addon type: global plugin or app module
   - settings required
   - spoken output
   - clipboard or configuration side effects
   - success criteria
4. Build the smallest vertical slice that proves:
   - NVDA loads the add-on
   - one script runs
   - one `ui.message(...)` works
5. Only then add:
   - settings panels
   - external APIs
   - multiple gestures
   - bundled libraries
   - packaging polish
6. Build and validate repeatedly:
   - syntax check Python
   - build `.nvda-addon`
   - install in NVDA
   - restart NVDA
   - test gestures
   - reopen settings multiple times
   - inspect NVDA log on failure

## Non-Negotiable Rules

- Package the archive so `globalPlugins/`, `appModules/`, and `doc/` sit at the
  archive root. Do not ship an extra `addon/` directory inside the archive.
- Use `gui.guiHelper.BoxSizerHelper` and `addLabeledControl` for settings pages.
- Prefer `Enable/Disable` over complex dynamic show/hide behavior in settings.
- Run slow or network work in background threads and return to UI with
  `wx.CallAfter(...)`.
- Exclude `__pycache__`, `.pyc`, and `.pyo` from the final archive.
- Deduplicate settings panel registration if the add-on can be reloaded or
  updated in place.
- By default, create generated files inside the `nvda/` skill directory. Only
  write outside it if the user explicitly provides a concrete path or the repo
  structure requires it.

## References

- `references/workflow.md`: short, practical checklist
- `references/practical-guide.md`: compact practical guide
- `references/troubleshooting.md`: failure-driven debugging guide

## Bundled Resources

- `assets/templates/`: minimal reusable files for project bootstrapping
- `scripts/bootstrap_addon.py`: create a small working NVDA add-on project from
  the included templates
