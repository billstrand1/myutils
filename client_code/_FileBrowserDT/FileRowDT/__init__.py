from ._anvil_designer import FileRowDTTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..FileViewerDT import FileViewerDT
from anvil import RepeatingPanel

class FileRowDT(FileRowDTTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    row = self.item

    def get_val(name, default=None):
      try:
        return row[name]
      except Exception:
        if isinstance(row, dict):
          return row.get(name, default)
        return default

    title = get_val("title", "") or ""
    comments = get_val("comments", "") or ""
    notes = get_val("notes", "") or ""

    media = get_val("file", None)
    mime = media.content_type.lower() if media else ""
    file_name = media.name if media else ""

    youtube_url = get_val("youtube_url", None)
    web_url = get_val("web_url", None)

    is_youtube = bool(youtube_url)
    has_web = bool(web_url)

    # Notes-only detection
    is_notes_only = bool(notes.strip()) and not (media or is_youtube or has_web)

    # Placeholder trip row: no notes, no media, no links
    is_trip_placeholder = (not notes.strip()) and (not media) and (not is_youtube) and (not has_web)

    # ---------- Comments label ----------
    if is_notes_only:
      combined = ""
      if comments:
        combined += comments
      if notes:
        if combined:
          combined += "\n"
        combined += notes
      self.label_comments.text = combined
    else:
      self.label_comments.text = comments

    # ---------- Icon + title ----------
    if is_notes_only:
      self.label_icon.text = "📝"
      self.label_title.text = f"{title or 'Notes'}  (Notes)"
      
    elif is_trip_placeholder:
    # Placeholder trip row (safe, no HTML, no M3 role usage)
      self.label_icon.text = "✈️"#"🗺️"
      self.label_title.text = title

    else:
      # Media / Web / YouTube rows
      if is_youtube:
        self.label_icon.text = "▶️"
        display_type = "YouTube Video"
        name_part = "YouTube"

      elif mime.startswith("image/"):
        self.label_icon.text = "🖼"
        display_type = "Image"
        name_part = file_name

      elif mime == "application/pdf":
        self.label_icon.text = "📄"
        display_type = "PDF"
        name_part = file_name

      elif mime.startswith("video/"):
        self.label_icon.text = "🎥"
        display_type = "Video"
        name_part = file_name

      elif mime.startswith("text/"):
        self.label_icon.text = "📝"
        display_type = "Text"
        name_part = file_name

      elif has_web:
        self.label_icon.text = "🔗"
        display_type = "Web Link"

        # Base URL only
        url = (web_url or "").strip()
        try:
          base = url.split("//", 1)[1]
        except IndexError:
          base = url
        base = base.split("/", 1)[0]
        name_part = base

      else:
        # Fallback: treat like placeholder
        self.label_icon.text = "🗺️"
        display_type = ""
        name_part = ""

      if display_type:
        # No file size (per request)
        self.label_title.text = f"{title}  ({name_part} — {display_type})"
      else:
        self.label_title.text = title

  # ----------------- open in viewer -----------------

  def link_open_click(self, **event_args):
    # from anvil import RepeatingPanel
    # from .FileViewerDT import FileViewerDT  # adjust import if needed

    # Walk up the parent chain until we find a RepeatingPanel
    p = self.parent
    rp = None
    while p is not None:
      if isinstance(p, RepeatingPanel):
        rp = p
        break
      p = p.parent

    if rp is None:
      print("ERROR: Could not find RepeatingPanel ancestor for FileRowDT")
      return

    # Full list of file rows shown in the browser
    file_rows = list(rp.items)
    start_index = file_rows.index(self.item)
    print(f"[FileRowDT] start_index = {start_index}")

    viewer = FileViewerDT(file_rows=file_rows, start_index=start_index)

    alert(
      content=viewer,
      large=True,
      buttons=[]
    )

