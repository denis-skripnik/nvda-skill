from __future__ import annotations

import addonHandler
import gui
import wx
from gui.settingsDialogs import SettingsPanel


addonHandler.initTranslation()


class AddonSettingsPanel(SettingsPanel):
    title = _("__SUMMARY__")

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        self.enabledCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=_("Enable add-on"))
        )
        self.apiKeyEdit = sHelper.addLabeledControl(
            _("API key:"),
            wx.TextCtrl,
            value="",
            style=wx.TE_PASSWORD,
        )
        self.timeoutEdit = sHelper.addLabeledControl(
            _("Timeout in seconds:"),
            wx.SpinCtrl,
            min=5,
            max=300,
            initial=45,
        )

    def onSave(self):
        pass
