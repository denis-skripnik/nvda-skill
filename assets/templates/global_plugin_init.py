from __future__ import annotations

import addonHandler
import globalPluginHandler
import scriptHandler
import ui


addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("__SUMMARY__")

    @scriptHandler.script(
        description=_("__SCRIPT_DESCRIPTION__"),
        gesture="kb:__GESTURE__",
        category=scriptCategory,
    )
    def script_mainAction(self, gesture):
        ui.message(_("It works"))
