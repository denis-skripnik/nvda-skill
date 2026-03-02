# Practical NVDA Add-on Guide

Use this file when the task needs detailed guidance, packaging rules, and
real-world failure handling.

## What To Prioritize

- behavior before architecture
- one working vertical slice before extra features
- stable NVDA settings pages before fancy UI
- correct archive layout before anything else
- local evidence before memory when integrating third-party APIs offline

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

## Popup Rule

For modal dialogs triggered from reminders, timers, or polling services:

- return to the UI thread first
- call `gui.mainFrame.prePopup()` before showing the dialog
- destroy the dialog after close
- call `gui.mainFrame.postPopup()` after close

For first-open focus issues after NVDA startup:

- `Show()` the dialog
- `Raise()` it
- focus a real child control
- if needed, repeat activation with `wx.CallAfter(...)` and `wx.CallLater(...)`

## Monitoring Rule

For reminders, summaries, or recurring checks:

- keep the monitor in a daemon thread
- use short polling intervals such as 30 seconds
- deduplicate notifications by task token or local date
- compare local time for user-facing schedules
- never block the UI thread with sleeps or API calls

## External API Rule

If the user provided local scripts or client code for the same service:

- inspect those files before implementing the Python side
- copy the proven endpoint choices and field names where possible
- treat actual response payloads as authoritative
- guard against multiple date/time shapes in the same API

## Release Rule

Do not call the task done until:

1. the add-on installs
2. NVDA loads it after restart
3. gestures work
4. settings open repeatedly without corruption
5. popup dialogs open from both direct actions and timed flows
6. the built archive excludes `__pycache__`, `.pyc`, and `.pyo`
