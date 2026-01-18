from ._anvil_designer import TripAssetsManagerTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..AssetEditor import AssetEditor


class TripAssetsManager(TripAssetsManagerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.trip_row = None
    self.rp_assets.set_event_handler("x-refresh", self.refresh_assets)
    self._read_only = False

  def load_trip(self, trip_row):
    """
    Called by TripEditor after trip is loaded or saved.
    """
    self.trip_row = trip_row

    if not trip_row:
      self._show_locked()
      return

    self._show_assets()
    self.refresh_assets()

  def _show_locked(self):
    self.lbl_hint.visible = True
    self.rp_assets.visible = False
    self.btn_add_asset.visible = False

  def _show_assets(self):
    self.lbl_hint.visible = False
    self.rp_assets.visible = True
    self.btn_add_asset.visible = True

  def refresh_assets(self, **event_args):
    assets = anvil.server.call("get_assets_for_trip", self.trip_row)
    self.rp_assets.items = assets
    self.rp_assets.raise_event("x-set-read-only", read_only=self._read_only)

  @handle("btn_add_asset", "click")
  def btn_add_asset_click(self, **e):
    editor = AssetEditor(self.trip_row)
    
    alert(editor, large=True, buttons=[])
    self.raise_event("x-close-alert")
    self.refresh_assets()

  def set_read_only(self, read_only: bool):
    self.btn_add_asset.visible = not read_only
    self._read_only = read_only

