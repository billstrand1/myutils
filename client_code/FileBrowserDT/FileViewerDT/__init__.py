from ._anvil_designer import FileViewerDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.server


class FileViewerDT(FileViewerDTTemplate):
  def __init__(self, file_rows, start_index=0, **properties):
    self.init_components(**properties)

    # Store list + index
    self.file_rows = list(file_rows)
    self.index = start_index

    # ---------- BUILD UI ----------

    # Root layout: vertical
    self.root_panel = ColumnPanel(spacing="medium")
    self.add_component(self.root_panel)

    # Header row: title, index, X
    self.header_row = FlowPanel(role=None, spacing="small")
    self.root_panel.add_component(self.header_row)

    self.label_name = Label(text="", bold=True)
    self.header_row.add_component(self.label_name)

    # Flexible spacer
    self.header_row.add_component(Spacer())

    # "N of M" label
    self.label_index = Label(text="", align="right")
    self.header_row.add_component(self.label_index)

    # Small space
    self.header_row.add_component(Spacer(width=10))

    # Top-right Close "X"
    self.link_close = Link(text="✕", align="right", foreground="red")
    self.link_close.set_event_handler("click", self.link_close_click)
    self.header_row.add_component(self.link_close)

    # Content area
    self.content_panel = ColumnPanel(spacing="small")
    self.root_panel.add_component(self.content_panel)

    # Info / comments label
    self.label_info = Label(text="", visible=False)
    self.content_panel.add_component(self.label_info)

    # Image viewer
    self.image_preview = Image(visible=False)
    self.content_panel.add_component(self.image_preview)

    # PDF iframe (via HtmlPanel)
    self.html_pdf = HtmlPanel(visible=False)
    self.content_panel.add_component(self.html_pdf)

    # Video player (via HtmlPanel)
    self.html_video = HtmlPanel(visible=False)
    self.content_panel.add_component(self.html_video)

    # Text viewer
    self.textarea_text = TextArea(visible=False)
    self.textarea_text.auto_expand = True
    self.content_panel.add_component(self.textarea_text)

    # Footer row: Prev / Next / Download / Close
    self.footer_row = FlowPanel(spacing="small")
    self.root_panel.add_component(self.footer_row)

    self.link_previous = Link(text="⟨ Previous", visible=False)
    self.link_previous.set_event_handler("click", self.link_previous_click)
    self.footer_row.add_component(self.link_previous)

    self.link_next = Link(text="Next ⟩", visible=False)
    self.link_next.set_event_handler("click", self.link_next_click)
    self.footer_row.add_component(self.link_next)

    # Spacer between nav and actions
    self.footer_row.add_component(Spacer())

    self.link_download = Link(text="Download")
    self.link_download.set_event_handler("click", self.link_download_click)
    self.footer_row.add_component(self.link_download)

    self.link_close_bottom = Link(text="Close")
    self.link_close_bottom.set_event_handler("click", self.link_close_click)
    self.footer_row.add_component(self.link_close_bottom)

    # ---------- LOAD INITIAL FILE ----------
    self._load_current_file()

  # ------------- CORE LOADER -------------

  def _load_current_file(self):
    # No files
    if not self.file_rows:
      self.label_info.visible = True
      self.label_info.text = "No files to display."
      self.label_index.text = ""
      return

    # Clamp index
    if self.index < 0:
      self.index = 0
    if self.index >= len(self.file_rows):
      self.index = len(self.file_rows) - 1

    file_row = self.file_rows[self.index]

    # Hide everything
    self.image_preview.visible = False
    self.html_pdf.visible = False
    self.html_video.visible = False
    self.textarea_text.visible = False
    self.label_info.visible = False

    # Normalize from DT row
    self.title = file_row['description']
    self.comments = file_row['comments']
    self.media = file_row['file']
    self.mime_type = self.media.content_type

    # Title
    self.label_name.text = self.title

    # N of M
    n = self.index + 1
    m = len(self.file_rows)
    self.label_index.text = f"{n} of {m}"

    print(f"[FileViewerDT] index={self.index}, mime_type={self.mime_type}")

    # Route by mime type
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
      print("[FileViewerDT] unsupported type")
      self.label_info.visible = True
      self.label_info.text = f"Unsupported type: {self.mime_type}"

    # Update navigation
    self._update_nav_buttons()

  # ------------- NAVIGATION -------------

  def _update_nav_buttons(self):
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

  # ------------- DISPLAY HELPERS -------------

  def _show_image(self):
    self.image_preview.source = self.media
    self.image_preview.visible = True
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

  def _show_pdf(self):
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

    url = self.media.get_url(False)
    # Simple iframe filling the width, fixed height
    self.html_pdf.content = f"""
      <iframe src="{url}" style="width:100%; height:500px; border:none;"></iframe>
    """
    self.html_pdf.visible = True

  def _show_video(self):
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

    url = self.media.get_url(False)
    self.html_video.content = f"""
      <video controls style="width:100%; max-height:500px;">
        <source src="{url}">
        Your browser does not support the video tag.
      </video>
    """
    self.html_video.visible = True

  def _show_text(self):
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

    text = anvil.server.call('get_text_from_media', self.media)
    self.textarea_text.text = text
    self.textarea_text.visible = True

  def _looks_like_text(self, title):
    title = title.lower()
    return (
      title.endswith(".txt")
      or title.endswith(".csv")
      or title.endswith(".md")
      or title.endswith(".log")
    )

  # ------------- DOWNLOAD + CLOSE -------------

  def link_download_click(self, **event_args):
    anvil.media.download(self.media)

  def link_close_click(self, **event_args):
    alert.close_alert()
