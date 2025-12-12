from ._anvil_designer import FileRowDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..FileViewerDT import FileViewerDT
from anvil import RepeatingPanel
# from .FileViewerDT import FileViewerDT  # adjust import if needed

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
    size_bytes = media.length if media else 0

    youtube_url = get_val("youtube_url", None)
    web_url = get_val("web_url", None)

    is_youtube = bool(youtube_url)
    has_web = bool(web_url)

    # Notes-only detection
    is_notes_only = bool(notes.strip()) and not (media or is_youtube or has_web)

    # Placeholder trip row: no notes, no media, no links
    is_trip_placeholder = (not notes.strip()) and (not media) and (not is_youtube) and (not has_web)

    # ---------- Comments label text ----------
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
      # Placeholder and media rows show comments only
      self.label_comments.text = comments

    # ---------- File size ----------
    def format_size(n):
      if n < 1024:
        return f"{n} bytes"
      elif n < 1024 * 1024:
        return f"{n/1024:.0f} KB"
      elif n < 1024 * 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
      else:
        return f"{n/1024/1024/1024:.2f} GB"

    file_size = format_size(size_bytes) if media else ""

    # ---------- Type & icon ----------
    if is_notes_only:
      icon = "📝"
      display_type = "Notes"
      file_name = ""
      file_size = ""

      # Title line: show (Notes)
      self.label_title.text = f"{title or 'Notes'}  (Notes)".strip()

    elif is_trip_placeholder:
      # ✅ New behavior: show a map icon and NO extra parenthetical text
      icon = "🗺️"
      self.label_title.text = title  # just the trip_id/title, nothing else

    else:
      # Media rows and web/youtube
      if is_youtube:
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
        display_type = "Web Link"
        icon = "🔗"
        file_name = "(web link)"
        file_size = ""
      else:
        # If we ever reach here, treat it like a placeholder too
        display_type = ""
        icon = "🗺️"

      # Build the standard title line
      extra = f"({file_name} — {display_type} — {file_size})".strip()

      # Clean up extra if display_type/file_size are empty-ish
      # (prevents ugly dashes)
      extra = extra.replace(" —  — ", " — ").replace("— )", ")")

      self.label_title.text = f"{title}  {extra}".strip()

    self.label_icon.text = icon



# class FileRowDT(FileRowDTTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)

#     row = self.item  # may be a dict or a Data Table Row

#     # Safe getter for both dict and Row
#     def get_val(name, default=None):
#       try:
#         return row[name]
#       except Exception:
#         if isinstance(row, dict):
#           return row.get(name, default)
#         return default

#     title = get_val("title", "") or ""
#     comments = get_val("comments", "") or ""
#     notes = get_val("notes", "") or ""

#     media = get_val("file", None)
#     mime = media.content_type.lower() if media else ""
#     file_name = media.name if media else ""
#     size_bytes = media.length if media else 0

#     youtube_url = get_val("youtube_url", None)
#     web_url = get_val("web_url", None)

#     is_youtube = bool(youtube_url)
#     has_web = bool(web_url)

#     # Detect a NOTES-ONLY row:
#     is_notes_only = bool(notes.strip()) and not (media or is_youtube or has_web)

#     # ----- Comments label text -----
#     if is_notes_only:
#       # For notes-only item, show comments + notes
#       combined = ""
#       if comments:
#         combined += comments
#       if notes:
#         if combined:
#           combined += "\n"
#         combined += notes
#       self.label_comments.text = combined
#     else:
#       # For media items, show comments only
#       self.label_comments.text = comments

#     # ----- File size formatter -----
#     def format_size(n):
#       if n < 1024:
#         return f"{n} bytes"
#       elif n < 1024 * 1024:
#         return f"{n/1024:.0f} KB"
#       elif n < 1024 * 1024 * 1024:
#         return f"{n/1024/1024:.1f} MB"
#       else:
#         return f"{n/1024/1024/1024:.2f} GB"

#     file_size = format_size(size_bytes) if media else ""

#     # ----- Type & icon -----
#     if is_notes_only:
#       display_type = "Notes"
#       icon = "📝"
#       file_name = ""
#       file_size = ""
#     elif is_youtube:
#       display_type = "YouTube Video"
#       icon = "▶️"
#     elif mime.startswith("image/"):
#       display_type = f"Image ({mime.split('/')[-1].upper()})"
#       icon = "🖼"
#     elif mime == "application/pdf":
#       display_type = "PDF"
#       icon = "📄"
#     elif mime.startswith("video/"):
#       display_type = f"Video ({mime.split('/')[-1].upper()})"
#       icon = "🎥"
#     elif mime.startswith("text/"):
#       display_type = f"Text ({mime.split('/')[-1].upper()})"
#       icon = "📝"
#     elif has_web:
#       display_type = "Web Link"
#       icon = "🔗"
#       file_name = "(web link)"
#       file_size = ""
#     else:
#       display_type = f"Unknown ({mime})" if mime else "Unknown"
#       icon = "❓"

#     # Title text (no emoji here; icon lives in label_icon)
#     if is_notes_only:
#       title_display = title or "Notes"
#       extra = "(Notes)"
#     else:
#       title_display = title
#       extra = f"({file_name} — {display_type})".strip()# — {file_size})".strip()

#     #New Title - Test
#     # self.label_title.text = f"[{display_type}] {title}  ({file_name} — {file_size})"

#     self.label_title.text = f"{title_display}  {extra}".strip()
#     self.label_icon.text = icon

#   # ----------------- open in viewer -----------------

#   def link_open_click(self, **event_args):
#     # from anvil import RepeatingPanel
#     # from .FileViewerDT import FileViewerDT  # adjust if needed

#     # Walk up the parent chain until we find a RepeatingPanel
#     p = self.parent
#     rp = None
#     while p is not None:
#       if isinstance(p, RepeatingPanel):
#         rp = p
#         break
#       p = p.parent

#     if rp is None:
#       print("ERROR: Could not find RepeatingPanel ancestor for FileRowDT")
#       return

#     # Full list of file rows shown in the browser
#     file_rows = list(rp.items)
#     start_index = file_rows.index(self.item)
#     print(f"[FileRowDT] start_index = {start_index}")

#     viewer = FileViewerDT(file_rows=file_rows, start_index=start_index)

#     alert(
#       content=viewer,
#       large=True,
#       buttons=[]  # viewer's own close link handles closing
#     )


# class FileRowDT(FileRowDTTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)

#     row = self.item  # may be a dict or a Data Table Row

#     # Safe getter for both dict and Row
#     def get_val(name, default=None):
#       try:
#         return row[name]
#       except Exception:
#         if isinstance(row, dict):
#           return row.get(name, default)
#         return default

#     title = get_val("title", "") or ""
#     comments = get_val("comments", "") or ""
#     notes = get_val("notes", "") or ""

#     media = get_val("file", None)
#     mime = media.content_type.lower() if media else ""
#     file_name = media.name if media else ""
#     size_bytes = media.length if media else 0

#     youtube_url = get_val("youtube_url", None)
#     web_url = get_val("web_url", None)

#     is_youtube = bool(youtube_url)
#     has_web = bool(web_url)

#     # Detect a NOTES-ONLY row:
#     is_notes_only = bool(notes.strip()) and not (media or is_youtube or has_web)

#     # ----- Comments label text -----
#     if is_notes_only:
#       # For notes-only item, show notes text only
#       self.label_comments.text = notes
#     else:
#       # For media items, show comments only (notes were stripped in expand_file_rows)
#       self.label_comments.text = comments

#     # ----- File size formatter -----
#     def format_size(n):
#       if n < 1024:
#         return f"{n} bytes"
#       elif n < 1024 * 1024:
#         return f"{n/1024:.0f} KB"
#       elif n < 1024 * 1024 * 1024:
#         return f"{n/1024/1024:.1f} MB"
#       else:
#         return f"{n/1024/1024/1024:.2f} GB"

#     file_size = format_size(size_bytes) if media else ""

#     # ----- Type & icon -----
#     if is_notes_only:
#       display_type = "Notes"
#       icon = "📝"
#       file_name = ""
#       file_size = ""
#     elif is_youtube:
#       display_type = "YouTube Video"
#       icon = "▶️"
#     elif mime.startswith("image/"):
#       display_type = f"Image ({mime.split('/')[-1].upper()})"
#       icon = "🖼"
#     elif mime == "application/pdf":
#       display_type = "PDF"
#       icon = "📄"
#     elif mime.startswith("video/"):
#       display_type = f"Video ({mime.split('/')[-1].upper()})"
#       icon = "🎥"
#     elif mime.startswith("text/"):
#       display_type = f"Text ({mime.split('/')[-1].upper()})"
#       icon = "📝"
#     elif has_web:
#       display_type = "Web Link"
#       icon = "🔗"
#       file_name = "(web link)"
#       file_size = ""
#     else:
#       display_type = f"Unknown ({mime})" if mime else "Unknown"
#       icon = "❓"

#     if is_notes_only:
#       title_display = f"📝 {title or 'Notes'}"
#       extra = "(Notes)"
#     else:
#       title_display = title
#       extra = f"({file_name} — {display_type} — {file_size})".strip()

#     self.label_title.text = f"{title_display}  {extra}".strip()
#     self.label_icon.text = icon

#   # ----------------- open in viewer -----------------

#   def link_open_click(self, **event_args):
#     # from anvil import RepeatingPanel
#     # from .FileViewerDT import FileViewerDT  # adjust if needed

#     # Walk up the parent chain until we find a RepeatingPanel
#     p = self.parent
#     rp = None
#     while p is not None:
#       if isinstance(p, RepeatingPanel):
#         rp = p
#         break
#       p = p.parent

#     if rp is None:
#       print("ERROR: Could not find RepeatingPanel ancestor for FileRowDT")
#       return

#     # Full list of file rows shown in the browser
#     file_rows = list(rp.items)
#     start_index = file_rows.index(self.item)
#     print(f"[FileRowDT] start_index = {start_index}")

#     viewer = FileViewerDT(file_rows=file_rows, start_index=start_index)

#     alert(
#       content=viewer,
#       large=True,
#       buttons=[]  # viewer's own close link handles closing
#     )



# class FileRowDT(FileRowDTTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)

#     row = self.item  # may be a dict or a Data Table Row

#     # Safe getter for both dict and Row
#     def get_val(name, default=None):
#       try:
#         return row[name]
#       except Exception:
#         if isinstance(row, dict):
#           return row.get(name, default)
#         return default

#     # Title
#     title = get_val("title", "")

#     # Comments + Notes (for the list row display only)
#     comments = get_val("comments", "") or ""
#     notes = get_val("notes", "") or ""

#     full_comments = comments
#     if notes:
#       # Keep existing behavior: show notes under comments in the list
#       if full_comments:
#         full_comments += "\n"
#       full_comments += notes

#     self.label_comments.text = full_comments

#     # Media info
#     media = get_val("file", None)
#     mime = media.content_type.lower() if media else ""
#     file_name = media.name if media else "(no file)"

#     # File size
#     size_bytes = media.length if media else 0

#     def format_size(n):
#       if n < 1024:
#         return f"{n} bytes"
#       elif n < 1024 * 1024:
#         return f"{n/1024:.0f} KB"
#       elif n < 1024 * 1024 * 1024:
#         return f"{n/1024/1024:.1f} MB"
#       else:
#         return f"{n/1024/1024/1024:.2f} GB"

#     file_size = format_size(size_bytes) if media else ""

#     # URLs
#     youtube_url = get_val("youtube_url", None)
#     web_url = get_val("web_url", None)

#     is_youtube = bool(youtube_url)
#     has_web = bool(web_url)

#     # Type & icon (priority: YouTube → image → PDF → video → text → web → unknown)
#     if is_youtube:
#       display_type = "YouTube Video"
#       icon = "▶️"
#     elif mime.startswith("image/"):
#       display_type = f"Image ({mime.split('/')[-1].upper()})"
#       icon = "🖼"
#     elif mime == "application/pdf":
#       display_type = "PDF"
#       icon = "📄"
#     elif mime.startswith("video/"):
#       display_type = f"Video ({mime.split('/')[-1].upper()})"
#       icon = "🎥"
#     elif mime.startswith("text/"):
#       display_type = f"Text ({mime.split('/')[-1].upper()})"
#       icon = "📝"
#     elif has_web:
#       display_type = "Web Link"
#       icon = "🔗"
#       file_name = "(web link)"
#       file_size = ""
#     else:
#       display_type = f"Unknown ({mime})" if mime else "Unknown"
#       icon = "❓"

#     self.label_title.text = f"{title}  ({file_name} — {display_type} — {file_size})"
#     self.label_icon.text = icon

#   # ----------------- open in viewer -----------------

#   def link_open_click(self, **event_args):

#     # Walk up the parent chain until we find a RepeatingPanel
#     p = self.parent
#     rp = None
#     while p is not None:
#       if isinstance(p, RepeatingPanel):
#         rp = p
#         break
#       p = p.parent

#     if rp is None:
#       print("ERROR: Could not find RepeatingPanel ancestor for FileRowDT")
#       return

#     # Full list of file rows shown in the browser
#     file_rows = list(rp.items)
#     start_index = file_rows.index(self.item)
#     print(f"[FileRowDT] start_index = {start_index}")

#     viewer = FileViewerDT(file_rows=file_rows, start_index=start_index)

#     alert(
#       content=viewer,
#       large=True,
#       buttons=[]  # viewer's own close link handles closing
#     )



# class FileRowDT(FileRowDTTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)

#     row = self.item  # the data table row

#     # Title
#     title = row["title"]

#     # Comments (optional)
#     comments = row.get("comments", "") if isinstance(row, dict) else row['comments']
#     notes = row.get("notes", "") if isinstance(row, dict) else row['notes']
#     if notes:
#       comments = comments + "\n" + notes
#     self.label_comments.text = comments or ""
      
#     # MIME / Type
#     media = row['file']
#     mime = media.content_type.lower() if media else ""
#     file_name = media.name if media else "(no file)"
    
#     # --- File size ---
#     size_bytes = media.length if media else 0
    
#     # --- YouTube URL (may or may not exist) ---
#     youtube_url = row['youtube_url'] #if 'youtube_url' in row else None
#     is_youtube = bool(youtube_url)  

#     web_url = row['web_url'] #if 'web_url' in row else None
#     print(f"web_url: {web_url}")
#     has_web = bool(web_url)
    
#     def format_size(n):
#       if n < 1024:
#         return f"{n} bytes"
#       elif n < 1024 * 1024:
#         return f"{n/1024:.0f} KB"
#       elif n < 1024 * 1024 * 1024:
#         return f"{n/1024/1024:.1f} MB"
#       else:
#         return f"{n/1024/1024/1024:.2f} GB"
  
#     file_size = format_size(size_bytes)

#     # Type & icon
#     if is_youtube:
#       # print('YT found for icon')
#       display_type = "YouTube Video"
#       icon = "▶️"
#     elif mime.startswith("image/"):
#       display_type = f"Image ({mime.split('/')[-1].upper()})"
#       icon = "🖼"
#     elif mime == "application/pdf":
#       display_type = "PDF"
#       icon = "📄"
#     elif mime.startswith("video/"):
#       display_type = f"Video ({mime.split('/')[-1].upper()})"
#       icon = "🎥"
#     elif mime.startswith("text/"):
#       display_type = f"Text ({mime.split('/')[-1].upper()})"
#       icon = "📝"
#     elif has_web:
#       print('weblink found')
#       display_type = "Web Link"
#       icon = "🔗"
#       file_name = "(web link)"
#       file_size = ""
#     else:
#       display_type = f"Unknown ({mime})" if mime else "Unknown"
#       icon = "❓"

#     self.label_title.text = f"{title}  ({file_name} — {display_type} — {file_size})"    # self.label_type.text = display_type
#     self.label_icon.text = icon
    
#   def link_open_click(self, **event_args):
#     from anvil import RepeatingPanel

#     # Walk up the parent chain until we find a RepeatingPanel
#     p = self.parent
#     rp = None
#     while p is not None:
#       if isinstance(p, RepeatingPanel):
#         rp = p
#         break
#       p = p.parent

#     if rp is None:
#       print("ERROR: Could not find RepeatingPanel ancestor for FileRowDT")
#       return

#     # Full list of file rows shown in the browser
#     file_rows = list(rp.items)
#     start_index = file_rows.index(self.item)
#     print(f"[FileRowDT] start_index = {start_index}")

#     viewer = FileViewerDT(file_rows=file_rows, start_index=start_index)

#     alert(
#       content=viewer,
#       large=True,
#       buttons=[]   # viewer's own close link handles closing
#     )
