from __future__ import annotations

import threading
from typing import Any, Callable

import addonHandler
import ui
import wx


addonHandler.initTranslation()


class ListManagerDialog(wx.Dialog):
    def __init__(
        self,
        parent,
        title: str,
        load_items: Callable[[], list[Any]],
        describe_item: Callable[[Any], str],
    ):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetMinSize((700, 420))
        self._load_items = load_items
        self._describe_item = describe_item
        self._items: list[Any] = []
        self._build_ui()
        self._load_items_async()

    def _build_ui(self):
        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        self.itemsList = wx.ListBox(panel, style=wx.LB_SINGLE)
        panelSizer.Add(self.itemsList, proportion=1, flag=wx.EXPAND | wx.ALL, border=12)

        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.refreshButton = wx.Button(panel, label=_("Refresh"))
        self.primaryButton = wx.Button(panel, label=_("Primary action"))
        self.secondaryButton = wx.Button(panel, label=_("Secondary action"))
        self.closeButton = wx.Button(panel, label=_("Close"))
        for button in (self.refreshButton, self.primaryButton, self.secondaryButton, self.closeButton):
            buttonsSizer.Add(button, flag=wx.RIGHT, border=8)
        panelSizer.Add(buttonsSizer, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=12)

        self.statusLabel = wx.StaticText(panel, label="")
        panelSizer.Add(self.statusLabel, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=12)

        panel.SetSizer(panelSizer)
        mainSizer.Add(panel, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainSizer)

        self.itemsList.Bind(wx.EVT_LISTBOX, self._onSelectionChanged)
        self.refreshButton.Bind(wx.EVT_BUTTON, lambda evt: self._load_items_async())
        self.primaryButton.Bind(wx.EVT_BUTTON, self.onPrimaryAction)
        self.secondaryButton.Bind(wx.EVT_BUTTON, self.onSecondaryAction)
        self.closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        self._update_action_state()

    def _set_status(self, text: str):
        self.statusLabel.SetLabel(text)

    def _current_item(self):
        index = self.itemsList.GetSelection()
        if index == wx.NOT_FOUND or index >= len(self._items):
            return None
        return self._items[index]

    def _onSelectionChanged(self, evt):
        self._update_action_state()

    def _update_action_state(self):
        has_item = self._current_item() is not None
        self.primaryButton.Enable(has_item)
        self.secondaryButton.Enable(has_item)

    def _load_items_async(self):
        self._set_status(_("Loading"))

        def worker():
            try:
                items = self._load_items()
            except Exception as error:
                wx.CallAfter(self._handle_error, error)
                return
            wx.CallAfter(self._finish_load, items)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_load(self, items: list[Any]):
        self._items = list(items)
        self.itemsList.Clear()
        for item in self._items:
            self.itemsList.Append(self._describe_item(item))
        self._set_status(_("Items: {count}").format(count=len(self._items)))
        self._update_action_state()

    def _handle_error(self, error: Exception):
        message = str(error)
        self._set_status(message)
        ui.message(message)

    def run_action_async(
        self,
        action: Callable[[], Any],
        success_message: str,
        after_success: Callable[[Any], None] | None = None,
    ):
        self._set_status(_("Working"))

        def worker():
            try:
                result = action()
            except Exception as error:
                wx.CallAfter(self._handle_error, error)
                return
            wx.CallAfter(self._finish_action, success_message, result, after_success)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_action(
        self,
        success_message: str,
        result: Any,
        after_success: Callable[[Any], None] | None,
    ):
        self._set_status(success_message)
        ui.message(success_message)
        if after_success is not None:
            after_success(result)
        else:
            self._load_items_async()

    def onPrimaryAction(self, evt):
        ui.message(_("Replace onPrimaryAction with a real implementation."))

    def onSecondaryAction(self, evt):
        ui.message(_("Replace onSecondaryAction with a real implementation."))
