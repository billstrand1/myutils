from ._anvil_designer import AssetEditorTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AssetEditor(AssetEditorTemplate):
  def __init__(self, trip_row, asset_row=None, **properties):
    self.init_components(**properties)
    self.trip_row = trip_row
    self.asset_row = asset_row
    
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
    self.txt_description.text = asset['description']
    self.txt_notes.text = asset['notes']
    self.chk_thumbnail.checked = asset['is_thumbnail']
    self.txt_web_url.text = asset['web_url']
    self.txt_youtube_url.text = asset['youtube_url']
    self._update_file_status()
    

  # def _show_existing_file_status(self):
  #   """
  #   Updates the status label to reflect whether we have an existing file (edit mode)
  #   or whether a new file has been selected.
  #   """
  #   # If user has selected a new file in this session, show that first
  #   new_file = self.file_loader.file
  #   if new_file is not None:
  #     name = getattr(new_file, "name", None) or "(selected file)"
  #     self.lbl_file_status.text = f"Selected: {name}"
  #     return
  
  #   # Otherwise show existing file (edit mode)
  #   if self.asset_row is not None and self.asset_row['file'] is not None:
  #     existing = self.asset_row['file']
  #     name = getattr(existing, "name", None) or "(existing file)"
  #     self.lbl_file_status.text = f"Current: {name}"
  #   else:
  #     self.lbl_file_status.text = "No file selected"
      
  @handle("btn_save", "click")
  def btn_save_click(self, **e):
    if not (self.file_loader.file or self.txt_web_url.text or self.txt_youtube_url.text):
      alert("Provide a file or a URL")
      return

    data = {
      "file": self.file_loader.file,
      "description": self.txt_description.text,
      "notes": self.txt_notes.text,
      "web_url": self.txt_web_url.text,
      "youtube_url": self.txt_youtube_url.text,
      "is_thumbnail": self.chk_thumbnail.checked,
    }

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
    
    
