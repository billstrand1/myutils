from ._anvil_designer import TripAssetRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...AssetEditor import AssetEditor

class TripAssetRow(TripAssetRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_row()

  def refresh_row(self):
    asset = self.item
    if asset is None:
      return

    self.lbl_desc.text = asset['description'] or "(no description)"
    self.lbl_type.text = asset['asset_type']

    self.lbl_thumbnail.visible = bool(asset['is_thumbnail'])
    if asset['is_thumbnail']:
      self.lbl_thumbnail.text = "Thumbnail"

  @handle("link_edit", "click")
  def link_edit_click(self, **event_args):
    editor = AssetEditor(
      self.item['trip_link'],
      asset_row=self.item
    )
    alert(editor, large=True, buttons=[])
    self.parent.raise_event("x-refresh")
