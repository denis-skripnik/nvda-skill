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
3. If the user provided local prototype code, scripts, or API clients, inspect
   those files before designing the integration. Treat them as the primary
   source for third-party API semantics when working offline.
4. Write down the user-visible behavior first:
   - gesture or trigger
   - addon type: global plugin or app module
   - settings required
   - spoken output
   - popup dialogs or notifications
   - background timers, polling, or daily jobs
   - clipboard or configuration side effects
   - success criteria
5. Build the smallest vertical slice that proves:
   - NVDA loads the add-on
   - one script runs
   - one `ui.message(...)` works
6. Only then add:
   - settings panels
   - external APIs
   - multiple gestures
   - bundled libraries
   - packaging polish
7. For manager-style or API-heavy requests, prefer the advanced bootstrap path
   or the advanced templates instead of stretching the minimal template.
8. Build and validate repeatedly:
   - syntax check Python
   - build `.nvda-addon`
   - install in NVDA
   - restart NVDA
   - test gestures
   - test first-open focus behavior after NVDA start
   - test popup dialogs from timers, reminders, and background threads
   - reopen settings multiple times
   - inspect NVDA log on failure
9. Before handoff, run `references/release-checklist.md` for a short NVDA-specific
   release pass.

## Non-Negotiable Rules

- Package the archive so `globalPlugins/`, `appModules/`, and `doc/` sit at the
  archive root. Do not ship an extra `addon/` directory inside the archive.
- Use `gui.guiHelper.BoxSizerHelper` and `addLabeledControl` for settings pages.
- Prefer `Enable/Disable` over complex dynamic show/hide behavior in settings.
- Run slow or network work in background threads and return to UI with
  `wx.CallAfter(...)`.
- For modal dialogs shown from timers, reminders, or background-driven UI,
  wrap display with `gui.mainFrame.prePopup()` / `postPopup()` or use NVDA's
  popup helpers. Do not rely on bare `ShowModal()` from background-driven
  flows.
- For the first show of a complex dialog after NVDA startup, explicitly
  activate it with `Raise()`, focus a real child control, and if needed repeat
  activation with `wx.CallAfter(...)` / `wx.CallLater(...)`.
- For reminder or monitoring features, deduplicate by task/date token so the
  same alert is not shown repeatedly during polling.
- When a third-party API is involved, inspect actual response shapes and field
  names before coding against them. Do not assume the docs, SDK, and payloads
  all use the same names.
- Exclude `__pycache__`, `.pyc`, and `.pyo` from the final archive.
- Deduplicate settings panel registration if the add-on can be reloaded or
  updated in place.
- By default, create generated files inside the `nvda/` skill directory. Only
  write outside it if the user explicitly provides a concrete path or the repo
  structure requires it.

## References

- `references/workflow.md`: short, practical checklist
- `references/practical-guide.md`: compact practical guide
- `references/advanced-patterns.md`: popup, polling, focus, and integration patterns for complex add-ons
- `references/release-checklist.md`: compact pre-release checks for packaging and NVDA-specific runtime behavior
- `references/troubleshooting.md`: failure-driven debugging guide

## Bundled Resources

- `assets/templates/`: minimal reusable files for project bootstrapping
- `assets/templates/advanced_global_plugin.py`: optional starting point for
  menu items, settings registration, popup helpers, and background services
- `assets/templates/list_manager_dialog.py`: reusable list-manager dialog for
  CRUD-style add-ons
- `scripts/bootstrap_addon.py`: create a small working NVDA add-on project from
  the included templates
