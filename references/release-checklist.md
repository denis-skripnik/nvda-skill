# Release Checklist

Use this before handing off any non-trivial NVDA add-on.

## Build And Package

- Compile all Python files.
- Build the `.nvda-addon` package.
- Inspect the archive root: `globalPlugins/`, `appModules/`, `doc/`, and manifest files must be at the package root, not under an extra `addon/` directory.
- Confirm `__pycache__/`, `.pyc`, and `.pyo` files are not included.

## Runtime Checks

- Install the add-on in NVDA and restart NVDA.
- Verify the main gesture or menu entry works on the first try after startup.
- Verify the first open of the main window takes focus instead of leaving the previous app active.
- Open the settings panel, save, close, and reopen it to catch duplicate registration or state issues.
- Exercise at least one success path and one failure path, then inspect the NVDA log.

## Background And Time-Based Features

- If the add-on has reminders, timers, or background polling, verify the popup appears through NVDA popup handling and is actionable.
- Verify reminder or summary popups are deduplicated and do not repeat on every poll.
- Verify local date and time parsing with the exact payload format used by the integration.
- For daily or scheduled summaries, verify they trigger once at the configured local time and only once per day.

## External Integrations

- If a third-party API is used, verify against the local prototype, wrapper, or captured payloads before trusting memory or generic docs.
- Re-test one edit or state-changing operation end to end after the read-only views succeed.
