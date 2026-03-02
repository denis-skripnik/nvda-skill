# Practical NVDA Add-on Guide

Use this file when the task needs detailed guidance, packaging rules, and
real-world failure handling.

## What To Prioritize

- behavior before architecture
- one working vertical slice before extra features
- stable NVDA settings pages before fancy UI
- correct archive layout before anything else

## Packaging Rule

Inside the final `.nvda-addon`, ship:

- `globalPlugins/...`
- `appModules/...` if needed
- `doc/...`
- `manifest.ini`

Do not ship an extra `addon/` directory inside the archive.

## Settings Rule

For NVDA settings pages, prefer:

- `gui.guiHelper.BoxSizerHelper`
- `addLabeledControl`
- `Enable/Disable` instead of aggressive `Show/Hide`

## Threading Rule

Slow work belongs in background threads.

Return to UI with `wx.CallAfter(...)`.

## Release Rule

Do not call the task done until:

1. the add-on installs
2. NVDA loads it after restart
3. gestures work
4. settings open repeatedly without corruption
5. the built archive excludes `__pycache__`, `.pyc`, and `.pyo`
