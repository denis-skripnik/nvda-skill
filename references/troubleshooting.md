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

## The package builds but docs do not open

Check:

- `docFileName` in manifest metadata
- `doc/en/readme.html` inside the archive

## The build includes garbage files

Exclude:

- `__pycache__/`
- `.pyc`
- `.pyo`
