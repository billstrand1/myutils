from ._anvil_designer import TripAssetRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...AssetEditor import AssetEditor
from ......_FileBrowserDT.FileViewerDT import FileViewerDT

class TripAssetRow(TripAssetRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_row()


  
  def refresh_row(self):
    asset = self.item
    if asset is None:
      return
    asset_type = asset['asset_type']
    # self.lnk_asset_type.text = asset_type.capitalize()
    self.lnk_asset_type.tooltip = "Click to view asset"
    icon_map = {
      "image": "🖼️",
      "video": "🎬",
      "pdf": "📄",
      "file": "📎",
      "link": "🔗",
    }

    icon = icon_map.get(asset_type, "")
    self.lnk_asset_type.text = f"{icon} {asset_type.capitalize()}"

    
    self.lbl_desc.text = asset['description'] or "(no description)"
    # self.lbl_type.text = asset['asset_type']

    # self.lbl_thumbnail.visible = bool(asset['is_thumbnail'])
    # if asset['is_thumbnail']:
    #   self.lbl_thumbnail.text = "Thumbnail"

  @handle("link_edit", "click")
  def link_edit_click(self, **event_args):
    editor = AssetEditor(
      self.item['trip_link'],
      asset_row=self.item
    )
    alert(editor, large=True, buttons=[])
    self.parent.raise_event("x-refresh")

  @handle("link_delete", "click")
  def link_delete_click(self, **event_args):
    asset = self.item
    if not asset:
      return

    desc = asset['description'] or "this asset"

    confirmed = confirm(
      f"Are you sure you want to delete {desc}?",
      title="Delete Asset",
      buttons=[
        ("Delete", True),
        ("Cancel", False),
      ],
      large=False
    )

    if not confirmed:
      return

    anvil.server.call("delete_asset", asset)

    # Tell TripAssetsManager to refresh
    self.parent.raise_event("x-refresh")


  def _open_asset_viewer(self):
    asset = self.item
    if not asset:
      return
  
    # try:
    #   from _FileBrowserDT import FileViewerDT
    # except ImportError:
    #   from FileViewerDT import FileViewerDT
  
    file_row = {
      "description": asset['description'] or "Asset",
      "comments": asset['notes'],
      "file": asset['file'],
      "web_url": asset['web_url'],
      "youtube_url": asset['youtube_url'],
    }
  
    viewer = FileViewerDT(file_rows=[file_row], start_index=0)
    alert(content=viewer, large=True, buttons=[])

  @handle("lnk_asset_type", "click")
  def lnk_asset_type_click(self, **event_args):
    self._open_asset_viewer()
