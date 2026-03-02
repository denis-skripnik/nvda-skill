# Practical Workflow

Use this skill as a build-and-debug playbook, not as an API encyclopedia.

## Start Here

1. Read `references/practical-guide.md`.
2. If the user supplied local prototype code or API wrappers, inspect those
   before designing external integrations.
3. Extract user-visible behavior first:
   - gesture or trigger
   - app scope
   - settings
   - spoken output
   - popup dialogs and notifications
   - background timers or polling jobs
   - clipboard or config side effects
   - success criteria
4. Build the smallest vertical slice that proves:
   - NVDA loads the add-on
   - one script runs
   - one `ui.message(...)` works
5. Only then add settings, external APIs, packaging polish, and extra features.

## Rules That Matter In Practice

- Package the archive so `globalPlugins/`, `appModules/`, and `doc/` are at the
  archive root, not under an extra `addon/` directory.
- Use `gui.guiHelper.BoxSizerHelper` with `addLabeledControl` for settings pages.
- Prefer `Enable/Disable` over complex dynamic layout changes in settings.
- Do slow or network work in background threads and return to UI with
  `wx.CallAfter(...)`.
- For dialogs shown from reminders, timers, or background-driven flows, use
  NVDA popup handling such as `prePopup()` / `postPopup()`.
- If the main window must take focus immediately after NVDA starts, explicitly
  `Raise()` it, focus a child control, and repeat activation with
  `wx.CallAfter(...)` or `wx.CallLater(...)` if necessary.
- Reopen the settings page multiple times and restart NVDA during validation.
