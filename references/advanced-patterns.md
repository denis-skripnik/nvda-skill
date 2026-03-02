# Advanced Patterns for NVDA Add-ons

Use this file when the request goes beyond a single script and needs reminders,
dialogs, settings, external APIs, or recurring background work.

## Popup Dialogs

When a dialog is shown from a timer, reminder, monitor, or other background-
driven flow:

1. marshal back to UI with `wx.CallAfter(...)`
2. call `gui.mainFrame.prePopup()`
3. create and show the dialog
4. destroy it
5. call `gui.mainFrame.postPopup()`

Treat bare `ShowModal()` as unsafe for background-driven flows unless you are
already inside a known NVDA popup helper.

## First-Open Focus

If the main window appears but focus stays in the previous app, explicitly:

- `dialog.Show()`
- `dialog.Raise()`
- focus a real child control such as a combo box or list
- repeat activation once with `wx.CallAfter(...)`
- if needed, repeat again with `wx.CallLater(100-200, ...)`

This matters most on the first open after NVDA starts.

## Polling and Timers

For reminders or daily summaries:

- keep polling in a daemon thread
- store the last shown token or date
- compare local time, not just UTC, when behavior is user-facing
- keep poll intervals short but not aggressive, for example 30 seconds
- never block the UI thread with network or sleeps

## External APIs While Offline

If the user gave you a local prototype or API wrapper:

- inspect that file first
- copy working endpoint choices and field names from it when possible
- log or guard against unexpected response shapes
- prefer local evidence over memory

When the API exposes multiple shapes for date/time fields, code for the real
shapes you see, not only the idealized documented one.

## Complex Task Dialogs

For CRUD-style task managers:

- prefer one editor dialog reused for add/edit flows
- pass in a client factory, not a live client instance stored globally
- rebuild checkbox groups when remote data changes
- keep destructive actions behind confirmation dialogs
- separate “main manager” dialogs from “summary” or “reminder” dialogs

## Daily Summary Features

If the user wants a once-per-day summary:

- store the configured time as normalized `HH:MM`
- show the summary once per local date after the threshold time
- filter active items locally using the user's intended rule
- make the summary dialog intentionally smaller and simpler than the full
  manager window
