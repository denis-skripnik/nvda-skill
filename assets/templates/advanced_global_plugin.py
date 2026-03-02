from __future__ import annotations

import threading

import addonHandler
import globalPluginHandler
import gui
import scriptHandler
import ui
import wx
from gui.settingsDialogs import NVDASettingsDialog

from .settings import AddonSettingsPanel


addonHandler.initTranslation()


class BackgroundService:
    def __init__(self, callback, poll_interval=30):
        self._callback = callback
        self._poll_interval = poll_interval
        self._stopEvent = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return
        self._stopEvent.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stopEvent.set()
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

    def _loop(self):
        while not self._stopEvent.wait(self._poll_interval):
            self._callback()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("__SUMMARY__")

    def __init__(self):
        super().__init__()
        self._mainDialog = None
        self._menuItem = None
        self._register_settings_panel()
        self._create_menu_item()

    def terminate(self):
        self._destroy_main_dialog()
        self._destroy_menu_item()
        self._unregister_settings_panel()
        super().terminate()

    @scriptHandler.script(
        description=_("__SCRIPT_DESCRIPTION__"),
        gesture="kb:__GESTURE__",
        category=scriptCategory,
    )
    def script_mainAction(self, gesture):
        self._open_main_window()

    def _register_settings_panel(self):
        for panelClass in list(NVDASettingsDialog.categoryClasses):
            if panelClass is AddonSettingsPanel:
                continue
            if getattr(panelClass, "title", None) == AddonSettingsPanel.title:
                NVDASettingsDialog.categoryClasses.remove(panelClass)
        if AddonSettingsPanel not in NVDASettingsDialog.categoryClasses:
            NVDASettingsDialog.categoryClasses.append(AddonSettingsPanel)

    def _unregister_settings_panel(self):
        if AddonSettingsPanel in NVDASettingsDialog.categoryClasses:
            NVDASettingsDialog.categoryClasses.remove(AddonSettingsPanel)

    def _create_menu_item(self):
        toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
        self._menuItem = toolsMenu.Append(wx.ID_ANY, _("__SUMMARY__..."))
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self._onMenu, self._menuItem)

    def _destroy_menu_item(self):
        if self._menuItem is None:
            return
        try:
            gui.mainFrame.sysTrayIcon.Unbind(wx.EVT_MENU, handler=self._onMenu, source=self._menuItem)
        except Exception:
            pass
        try:
            gui.mainFrame.sysTrayIcon.toolsMenu.Remove(self._menuItem)
        except Exception:
            pass
        self._menuItem = None

    def _onMenu(self, evt):
        self._open_main_window()

    def _open_main_window(self):
        if self._mainDialog is not None:
            try:
                if self._mainDialog.IsShown():
                    self._mainDialog.Raise()
                    self._focus_main_dialog()
                    return
            except Exception:
                self._mainDialog = None

        # Replace this with a real dialog class.
        dialog = wx.Dialog(gui.mainFrame, title=_("__SUMMARY__"))
        dialog.Bind(wx.EVT_CLOSE, self._on_main_dialog_close)
        self._mainDialog = dialog
        dialog.Show()
        self._focus_main_dialog()

    def _focus_main_dialog(self):
        if self._mainDialog is None:
            return
        try:
            self._mainDialog.Raise()
            self._mainDialog.SetFocus()
        except Exception:
            return
        wx.CallAfter(self._focus_main_dialog_later)
        wx.CallLater(150, self._focus_main_dialog_later)

    def _focus_main_dialog_later(self):
        if self._mainDialog is None:
            return
        try:
            self._mainDialog.Raise()
            self._mainDialog.SetFocus()
        except Exception:
            pass

    def _on_main_dialog_close(self, evt):
        self._mainDialog = None
        evt.Skip()

    def _destroy_main_dialog(self):
        if self._mainDialog is None:
            return
        try:
            self._mainDialog.Destroy()
        except Exception:
            pass
        self._mainDialog = None

    def _show_modal_popup(self, dialog: wx.Dialog):
        gui.mainFrame.prePopup()
        try:
            dialog.Raise()
            dialog.ShowModal()
        finally:
            try:
                dialog.Destroy()
            finally:
                gui.mainFrame.postPopup()
