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
    notes = asset['notes']
    
    if notes:
      self.lbl_notes.text = notes
      self.lbl_notes.visible = True
    else:
      self.lbl_notes.text = ""
      self.lbl_notes.visible = False
    
    self.img_preview.visible = False
    self.lbl_preview_hint.visible = False
    self.img_preview.source = None
    
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
    
    # self.img_preview.tooltip = "Click to view"
    # self.lbl_preview_hint.tooltip = "Click to view"


    # Inline preview logic
    if asset['file'] and self._is_image_media(asset['file']):
      # Image file preview
      self.img_preview.source = asset['file']
      self.img_preview.visible = True
    
    elif asset['youtube_url']:
      # YouTube thumbnail preview
      thumb_url = self._youtube_thumbnail_url(asset['youtube_url'])
      if thumb_url:
        self.img_preview.source = thumb_url
        self.img_preview.visible = True
      else:
        self.lbl_preview_hint.text = "YouTube preview"
        self.lbl_preview_hint.visible = True
    
    elif asset['web_url']:
      # Web link (no inline image)
      self.lbl_preview_hint.text = "Web preview"
      self.lbl_preview_hint.visible = True
    
    elif asset['file']:
      # Non-image file (PDF, etc.)
      self.lbl_preview_hint.text = "File preview"
      self.lbl_preview_hint.visible = True


  
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
  
    file_row = {
      "title": asset['description'] or "Asset", #self.lbl_desc.text, 
      # "description": asset['description'] or "Asset", 
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


  def _is_image_media(self, media_obj):
    if not media_obj:
      return False
    name = (getattr(media_obj, "name", "") or "").lower()
    return name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
  
  def _youtube_thumbnail_url(self, youtube_url):
    """
      Extracts the video ID and returns a thumbnail URL.
      Works for standard youtu.be and youtube.com URLs.
      """
    if not youtube_url:
      return None
  
    import re
    patterns = [
      r"youtu\.be/([^?&]+)",
      r"v=([^?&]+)",
    ]
  
    for p in patterns:
      m = re.search(p, youtube_url)
      if m:
        return f"https://img.youtube.com/vi/{m.group(1)}/hqdefault.jpg"
  
    return None


  def apply_read_only(self, read_only: bool):
    self.link_edit.visible = not read_only
    self.link_delete.visible = not read_only
