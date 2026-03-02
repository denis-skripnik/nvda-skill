# Practical Workflow

Use this skill as a build-and-debug playbook, not as an API encyclopedia.

## Start Here

1. Read `references/practical-guide.md`.
2. Extract user-visible behavior first:
   - gesture or trigger
   - app scope
   - settings
   - spoken output
   - clipboard or config side effects
   - success criteria
3. Build the smallest vertical slice that proves:
   - NVDA loads the add-on
   - one script runs
   - one `ui.message(...)` works
4. Only then add settings, external APIs, packaging polish, and extra features.

## Rules That Matter In Practice

- Package the archive so `globalPlugins/`, `appModules/`, and `doc/` are at the
  archive root, not under an extra `addon/` directory.
- Use `gui.guiHelper.BoxSizerHelper` with `addLabeledControl` for settings pages.
- Prefer `Enable/Disable` over complex dynamic layout changes in settings.
- Do slow or network work in background threads and return to UI with
  `wx.CallAfter(...)`.
- Exclude `__pycache__`, `.pyc`, and `.pyo` from the final archive.
- Reopen the settings page multiple times and restart NVDA during validation.
