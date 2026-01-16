from ._anvil_designer import AssetEditorTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import _Travel

class AssetEditor(AssetEditorTemplate):
  def __init__(self, trip_row, asset_row=None, **properties):
    self.init_components(**properties)
    self.trip_row = trip_row
    self.asset_row = asset_row
    self._clear_file = False
    
    if asset_row:
      self._load_asset(asset_row)
      
    # Show default file status
    # self._show_existing_file_status()
    
    if asset_row:
      self._load_asset(asset_row)


  def _update_file_status(self):
    if self.file_loader.file:
      self.lbl_file_status.text = f"Selected: {self.file_loader.file.name}"
    elif self.asset_row and self.asset_row['file']:
      self.lbl_file_status.text = f"Current: {self.asset_row['file'].name}"
    else:
      self.lbl_file_status.text = "No file selected"

      
  def _load_asset(self, asset):
    self._clear_file = False
    self.txt_description.text = asset['description']
    self.txt_notes.text = asset['notes']
    # self.chk_thumbnail.checked = asset['is_thumbnail']
    self.txt_web_url.text = asset['web_url']
    self.txt_youtube_url.text = asset['youtube_url']
    self._update_file_status()
    
  def _count_asset_inputs(self):
    return sum([
      bool(self.file_loader.file),
      bool(self.txt_web_url.text),
      bool(self.txt_youtube_url.text),
    ])

  def _count_asset_inputs_effective(self):
    effective_file_present = bool(self.file_loader.file) or (bool(self.asset_row and self.asset_row['file']) and not self._clear_file)
    return sum([
      bool(effective_file_present),
      bool((self.txt_web_url.text or "").strip()),
      bool((self.txt_youtube_url.text or "").strip()),
    ])

      
  @handle("btn_save", "click")
  def btn_save_click(self, **e):
    #From 2B.3:
    count = self._count_asset_inputs_effective()
    if count != 1:
      alert("Provide exactly one: file OR web URL OR YouTube URL (you can remove a file to keep a link).")
      return
    # count = self._count_asset_inputs()

    # if count == 0:
    #   alert("Provide exactly one: file, web URL, or YouTube URL")
    #   return
    
    # if count > 1:
    #   alert("Only ONE asset type is allowed (file OR web URL OR YouTube URL)")
    #   return

    data = {
      "file": self.file_loader.file,  # may be None
      "web_url": (self.txt_web_url.text or "").strip() or None,
      "youtube_url": (self.txt_youtube_url.text or "").strip() or None,
      "description": self.txt_description.text,
      "notes": self.txt_notes.text,
      # "is_thumbnail": self.chk_thumbnail.checked,
      "clear_file": self._clear_file,
    }
    
    # data = {
    #   "file": self.file_loader.file,
    #   "description": self.txt_description.text,
    #   "notes": self.txt_notes.text,
    #   "web_url": self.txt_web_url.text,
    #   "youtube_url": self.txt_youtube_url.text,
    #   "is_thumbnail": self.chk_thumbnail.checked,
    # }

    if self.asset_row:
      anvil.server.call("update_asset", self.asset_row, data)
    else:
      anvil.server.call("add_asset", self.trip_row, data)

    self.raise_event("x-close-alert")

  @handle("btn_cancel", "click")
  def btn_cancel_click(self, **e):
    self.raise_event("x-close-alert")

  @handle("file_loader", "change")
  def file_loader_change(self, file, **event_args):
    self._update_file_status()

  @handle("btn_open_web_url", "click")
  def btn_open_web_url_click(self, **event_args):
    url = (self.txt_web_url.text or "").strip()
    if not url:
      alert("No web URL to open")
      return
  
    _Travel.open_in_file_viewer_dt(
      title=self.txt_description.text or "Asset Web Link",
      web_url=url,
      comments="Web link"
    )

  @handle("btn_open_youtube_url", "click")
  def btn_open_youtube_url_click(self, **event_args):
    url = (self.txt_youtube_url.text or "").strip()
    if not url:
      alert("No YouTube URL to open")
      return
  
    _Travel.open_in_file_viewer_dt(
      title=self.txt_description.text or "Asset YouTube Link",
      youtube_url=url,
      comments="YouTube link"
    )

  @handle("btn_remove_itinerary", "click")
  def btn_remove_itinerary_click(self, **event_args):
    if not (self.asset_row and self.asset_row['file']):
      alert("No file to remove")
      return

    if confirm("Remove the file from this asset?", title="Remove File"):
      self._clear_file = True
      self.lbl_file_status.text = "Will remove file on Save"
    
    
