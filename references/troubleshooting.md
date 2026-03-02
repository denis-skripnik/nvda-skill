# Troubleshooting by Symptom

## Gestures do nothing

Check:

- the plugin class loaded at all
- `@scriptHandler.script` is present
- the archive root contains `globalPlugins/...`
- NVDA was restarted after install

## The add-on appears in settings, but the right pane shows another category

Treat this as a settings panel construction failure.

Check:

- exceptions in `makeSettings`
- use of custom widgets or dynamic visibility
- stale entries in `NVDASettingsDialog.categoryClasses`

Fix strategy:

- switch to `gui.guiHelper.BoxSizerHelper`
- replace `Show/Hide` tricks with `Enable/Disable`
- remove fancy controls until the panel is stable

## The settings page works once, then breaks after reopen

Check:

- duplicate panel registration
- stale state stored on the panel instance
- runtime exceptions in event handlers bound during `makeSettings`

## The add-on installs but is not loaded

Check the package layout first.

Inside the archive, you should see:

- `globalPlugins/...`
- `doc/...`
- `manifest.ini`

Not:

- `addon/globalPlugins/...`

## NVDA freezes during API calls

Move the work into a background thread.

Use:

- `threading.Thread(..., daemon=True)`
- `wx.CallAfter(...)` for UI updates

## Reminder or timer dialog never appears

Check:

- whether the due time is actually parsed from the real payload shape
- local time versus UTC assumptions
- the poll interval and deduplication token
- `gui.mainFrame.prePopup()` / `postPopup()` around modal dialogs
- that the actual dialog show call runs on the UI thread

## The first open shows the window but focus stays in the previous app

Check:

- `Raise()` on the dialog
- focus on a real child control instead of the top-level dialog
- a follow-up activation via `wx.CallAfter(...)`
- a delayed retry via `wx.CallLater(...)`

## A once-per-day summary shows multiple times or not at all

Check:

- local-date deduplication
- normalized `HH:MM` parsing
- whether you set the “shown today” flag before or after the dialog
- filtering logic for which tasks qualify

## The package builds but docs do not open

Check:

- `docFileName` in manifest metadata
- `doc/en/readme.html` inside the archive

## The build includes garbage files

Exclude:

- `__pycache__/`
- `.pyc`
- `.pyo`
