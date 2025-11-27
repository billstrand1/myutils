from ._anvil_designer import FileViewerDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FileViewerDT(FileViewerDTTemplate):
  def __init__(self, file_rows, start_index=0, **properties):
    self.init_components(**properties)

    # Store the list and current index
    self.file_rows = list(file_rows)
    self.index = start_index

    # Load the initial file right away
    self._load_current_file()

  # ----------------- core loader / router -----------------

  def _load_current_file(self):
    # No files? show message and bail
    if not self.file_rows:
      self.label_info.visible = True
      self.label_info.text = "No files to display."
      if hasattr(self, "label_index"):
        self.label_index.text = ""
      return

    # Clamp index just in case
    if self.index < 0:
      self.index = 0
    if self.index >= len(self.file_rows):
      self.index = len(self.file_rows) - 1

    file_row = self.file_rows[self.index]

    # Hide everything first
    self.image_preview.visible = False
    self.iframe_pdf.visible = False
    self.video_player.visible = False
    self.textarea_text.visible = False
    self.label_info.visible = False

    # Normalize from Data Table row
    self.title = file_row['description']
    self.comments = file_row['comments']
    
    # self.media = file_row['file']
    # self.mime_type = self.media.content_type
    self.media = file_row['file']
    
    if self.media:
      self.mime_type = self.media.content_type.lower()
    else:
      self.mime_type = None

    if not self.media:
      self.label_info.visible = True
      self.label_info.text = "No file attached."
      # Hide all viewer components
      self.image_preview.visible = False
      self.iframe_pdf.visible = False
      self.video_player.visible = False
      self.textarea_text.visible = False
      return

    
    # Set the title (top of the alert)
    self.label_name.text = self.title

    # 👉 NEW: set "N of M" label
    if hasattr(self, "label_index"):
      n = self.index + 1
      m = len(self.file_rows)
      self.label_index.text = f"{n} of {m}"

    print(f"[FileViewerDT] index={self.index}, mime_type={self.mime_type}")

    # Route based on mime type
    if self.mime_type.startswith("image/"):
      print("[FileViewerDT] image found")
      self._show_image()
    elif self.mime_type == "application/pdf":
      print("[FileViewerDT] pdf found")
      self._show_pdf()
    elif self.mime_type.startswith("video/"):
      print("[FileViewerDT] video found")
      self._show_video()
    elif self.mime_type.startswith("text/") or self._looks_like_text(self.title):
      print("[FileViewerDT] text found")
      self._show_text()
    else:
      print("[FileViewerDT] unsupported type found")
      self.label_info.visible = True
      self.label_info.text = f"Unsupported type for now: {self.mime_type}"

    # Update Prev/Next visibility
    self._update_nav_buttons()


  # ----------------- navigation buttons -----------------

  def _update_nav_buttons(self):
    # using your link names: link_previous, link_next
    self.link_previous.visible = (self.index > 0)
    self.link_next.visible = (self.index < len(self.file_rows) - 1)

  def link_previous_click(self, **event_args):
    if self.index > 0:
      self.index -= 1
      self._load_current_file()

  def link_next_click(self, **event_args):
    if self.index < len(self.file_rows) - 1:
      self.index += 1
      self._load_current_file()

  # ----------------- display helpers -----------------

  def _show_image(self):
    self.image_preview.source = self.media
    self.image_preview.visible = True
    self.label_info.text = self.comments
    self.label_info.visible = True

  def _show_pdf(self):
    self.label_info.visible = True
    self.label_info.text = self.comments

    docurl = self.media.get_url(False)
    self.iframe_pdf.url = docurl
    self.iframe_pdf.visible = True

  def _show_video(self):
    self.label_info.visible = True
    self.label_info.text = self.comments

    self.video_player.height = 500
    self.video_player.width = 1000

    url = self.media.get_url(False)
    self.video_player.source = url
    self.video_player.visible = True

  def _show_text(self):
    self.label_info.visible = True
    self.label_info.text = self.comments

    text = anvil.server.call('get_text_from_media', self.media)
    self.textarea_text.text = text
    self.textarea_text.auto_expand = True
    self.textarea_text.visible = True

  def _looks_like_text(self, title):
    title = title.lower()
    return (
      title.endswith(".txt") or
      title.endswith(".csv") or
      title.endswith(".md") or
      title.endswith(".log")
    )

  # ----------------- download + close -----------------

  def link_download_click(self, **event_args):
    anvil.media.download(self.media)

  # def link_to_close_click(self, **event_args):
  #   # top-right X or bottom "Close" can both call this
  #   alert.close_alert()

  def link_to_close_click(self, **event_args):
    # alert.close_alert()
    self.raise_event("x-close-alert", value=None)