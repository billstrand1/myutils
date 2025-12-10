from ._anvil_designer import FileRowDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..FileViewerDT import FileViewerDT

class FileRowDT(FileRowDTTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    row = self.item  # the data table row

    # Title
    title = row["title"]

    # Comments (optional)
    comments = row.get("comments", "") if isinstance(row, dict) else row['comments']
    notes = row.get("notes", "") if isinstance(row, dict) else row['notes']
    if notes:
      comments = comments + "\n" + notes
    self.label_comments.text = comments or ""
      
    # MIME / Type
    media = row['file']
    mime = media.content_type.lower() if media else ""
    file_name = media.name if media else "(no file)"
    
    # --- File size ---
    size_bytes = media.length if media else 0
    
    # --- YouTube URL (may or may not exist) ---
    youtube_url = row['youtube_url'] #if 'youtube_url' in row else None
    is_youtube = bool(youtube_url)  

    web_url = row['web_url'] #if 'web_url' in row else None
    print(f"web_url: {web_url}")
    has_web = bool(web_url)
    
    def format_size(n):
      if n < 1024:
        return f"{n} bytes"
      elif n < 1024 * 1024:
        return f"{n/1024:.0f} KB"
      elif n < 1024 * 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
      else:
        return f"{n/1024/1024/1024:.2f} GB"
  
    file_size = format_size(size_bytes)

    # Type & icon
    if is_youtube:
      # print('YT found for icon')
      display_type = "YouTube Video"
      icon = "▶️"
    elif mime.startswith("image/"):
      display_type = f"Image ({mime.split('/')[-1].upper()})"
      icon = "🖼"
    elif mime == "application/pdf":
      display_type = "PDF"
      icon = "📄"
    elif mime.startswith("video/"):
      display_type = f"Video ({mime.split('/')[-1].upper()})"
      icon = "🎥"
    elif mime.startswith("text/"):
      display_type = f"Text ({mime.split('/')[-1].upper()})"
      icon = "📝"
    elif has_web:
      print('weblink found')
      display_type = "Web Link"
      icon = "🔗"
      file_name = "(web link)"
      file_size = ""
    else:
      display_type = f"Unknown ({mime})" if mime else "Unknown"
      icon = "❓"

    self.label_title.text = f"{title}  ({file_name} — {display_type} — {file_size})"    # self.label_type.text = display_type
    self.label_icon.text = icon
    
  def link_open_click(self, **event_args):
    from anvil import RepeatingPanel

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
      buttons=[]   # viewer's own close link handles closing
    )
