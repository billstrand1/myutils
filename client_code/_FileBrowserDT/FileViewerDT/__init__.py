from ._anvil_designer import FileViewerDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js import get_dom_node  
import anvil.js

'''


'''

class FileViewerDT(FileViewerDTTemplate):
  def __init__(self, file_rows, start_index=0, **properties):
    self.init_components(**properties)

    self.file_rows = list(file_rows)
    self.index = start_index

    self._load_current_file()

  # ----------------- core loader / router -----------------

  def _load_current_file(self):
    if not self.file_rows:
      self.label_info.visible = True
      self.label_info.text = ""
      if hasattr(self, "label_index"):
        self.label_index.text = ""
      self.link_download.visible = False
      return

    if self.index < 0:
      self.index = 0
    if self.index >= len(self.file_rows):
      self.index = len(self.file_rows) - 1

    file_row = self.file_rows[self.index]

    def get_val(name, default=None):
      try:
        return file_row[name]
      except Exception:
        if isinstance(file_row, dict):
          return file_row.get(name, default)
        return default

    # Hide all content widgets
    self.you_tube_video.visible = False
    self.image_preview.visible = False
    self.iframe_pdf.visible = False
    self.video_player.visible = False
    self.textarea_text.visible = False
    self.label_info.visible = False
    self.iframe_web.visible = False

    # Header fields
    self.title = get_val("title", "") or ""
    self.comments = get_val("comments", "") or ""
    notes_text = get_val("notes", "") or ""

    # Media/URLs
    self.media = get_val("file", None)
    self.mime_type = self.media.content_type.lower() if self.media else None
    self.youtube_url = get_val("youtube_url", None)
    self.web_url = get_val("web_url", None)

    # Detect notes-only row: notes present, but no media or URLs
    self.is_notes_only = bool(notes_text.strip()) and not (
      self.media or self.youtube_url or self.web_url
    )

    # Title label (with icon for notes-only)
    if self.is_notes_only:
      self.label_name.text = f"📝 {self.title or 'Notes'}"
    else:
      self.label_name.text = self.title

    # Comments in label_info (only if present)
    self.label_info.text = self.comments
    self.label_info.visible = bool(self.comments)

    # Notes panel shows notes_text for any row where notes is set (for notes-only,
    # only this row has notes; media rows had notes cleared in expand_file_rows)
    self.label_notes.text = notes_text or ""
    self.notes_panel.visible = bool(notes_text)
    self.label_notes.visible = bool(notes_text)

    # N of M
    if hasattr(self, "label_index"):
      n = self.index + 1
      m = len(self.file_rows)
      self.label_index.text = f"{n} of {m}"

    # Download/link visibility will be set in _update_nav_buttons
    self.link_download.visible = False

    print(
      f"[FileViewerDT] index={self.index}, mime_type={self.mime_type}, "
      f"youtube_url={self.youtube_url}, web_url={self.web_url}, "
      f"is_notes_only={self.is_notes_only}"
    )

    # ---- NOTES-ONLY ROUTE ----
    if self.is_notes_only:
      # Only notes (and optional comments) are shown; no media.
      # All viewer widgets already hidden above, so just update nav buttons.
      self._update_nav_buttons()
      return

    # ---- PRIORITY 1: YOUTUBE ----
    if self.youtube_url:
      self._show_youtube()
      self._update_nav_buttons()
      return

    # ---- PRIORITY 2: WEB URL ----
    if self.web_url:
      self._show_web()
      self._update_nav_buttons()
      return

    # ---- PRIORITY 3: REGULAR MEDIA ----
    if not self.media:
      # No youtube, no web, no media: just show comments/notes.
      if self.comments:
        self.label_info.text = self.comments
        self.label_info.visible = True
      self._update_nav_buttons()
      return

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

    self._update_nav_buttons()

  # ----------------- navigation buttons -----------------

  def _update_nav_buttons(self):
    self.link_previous.visible = (self.index > 0)
    self.link_next.visible = (self.index < len(self.file_rows) - 1)

    has_file = bool(self.media)
    has_web = bool(self.web_url)
    has_youtube = bool(self.youtube_url)

    # Notes-only: no download/open button
    if self.is_notes_only:
      self.link_download.visible = False
      return

    if has_web or has_youtube:
      self.link_download.icon = "fa:external-link"
      self.link_download.tooltip = "Open in New Tab"
      self.link_download.visible = True
    elif has_file:
      self.link_download.icon = "fa:download"
      self.link_download.tooltip = "Download File"
      self.link_download.visible = True
    else:
      self.link_download.visible = False

  def link_previous_click(self, **event_args):
    if self.index > 0:
      self.index -= 1
      self._load_current_file()

  def link_next_click(self, **event_args):
    if self.index < len(self.file_rows) - 1:
      self.index += 1
      self._load_current_file()

  # ----------------- display helpers (unchanged except for using comments) ----

  def _show_youtube(self):
    print("entering _show_youtube.")

    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

    url = (self.youtube_url or "").strip()

    # Extract video ID
    video_id = None
    if "watch?v=" in url:
      video_id = url.split("watch?v=", 1)[1].split("&", 1)[0]
    elif "youtu.be/" in url:
      video_id = url.split("youtu.be/", 1)[1].split("?", 1)[0]
    else:
      video_id = url

    node = get_dom_node(self.you_tube_video)
    iframe = node.querySelector("iframe") or node
    if iframe:
      iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin")

    self.you_tube_video.youtube_id = video_id
    self.you_tube_video.visible = True

  def _show_image(self):
    self.image_preview.source = self.media
    self.image_preview.visible = True
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

  def _show_pdf(self):
    if self.comments:
      self.label_info.visible = True
      self.label_info.text = self.comments
    docurl = self.media.get_url(False)
    self.iframe_pdf.url = docurl
    self.iframe_pdf.visible = True

  def _show_video(self):
    if self.comments:
      self.label_info.visible = True
      self.label_info.text = self.comments

    self.video_player.height = 500
    self.video_player.width = 1000

    url = self.media.get_url(False)
    self.video_player.source = url
    self.video_player.visible = True

  def _show_text(self):
    if self.comments:
      self.label_info.visible = True
      self.label_info.text = self.comments

    text = anvil.server.call('get_text_from_media', self.media)
    self.textarea_text.text = text
    self.textarea_text.auto_expand = True
    self.textarea_text.visible = True

  def _looks_like_text(self, title):
    title = (title or "").lower()
    return (
      title.endswith(".txt") or
      title.endswith(".csv") or
      title.endswith(".md") or
      title.endswith(".log")
    )

  def _show_web(self):
    if self.comments:
      self.label_info.text = self.comments
      self.label_info.visible = True

    url = (self.web_url or "").strip()
    print(f"[FileViewerDT] web_url={url}")

    self.iframe_web.url = url
    self.iframe_web.visible = True

  # ----------------- download + close -----------------

  def link_download_click(self, **event_args):
    if self.is_notes_only:
      Notification("Nothing to download or open.", style="warning").show()
      return

    if self.media:
      anvil.media.download(self.media)
      return

    if self.web_url:
      url = (self.web_url or "").strip()
      if url:
        anvil.js.window.open(url, "_blank")
      return

    if self.youtube_url:
      url = (self.youtube_url or "").strip()
      if url:
        anvil.js.window.open(url, "_blank")
      return

    Notification("Nothing to download or open.", style="warning").show()

  def link_to_close_click(self, **event_args):
    self.raise_event("x-close-alert", value=None)



# class FileViewerDT(FileViewerDTTemplate):
#   def __init__(self, file_rows, start_index=0, **properties):
#     self.init_components(**properties)

#     # Store the list and current index
#     self.file_rows = list(file_rows)
#     self.index = start_index

#     # Load the initial file right away
#     self._load_current_file()

#   # ----------------- core loader / router -----------------

#   def _load_current_file(self):
#     # No files? show message and bail
#     if not self.file_rows:
#       self.label_info.visible = True
#       self.label_info.text = ""
#       if hasattr(self, "label_index"):
#         self.label_index.text = ""
#       self.link_download.visible = False
#       return

#     # Clamp index just in case
#     if self.index < 0:
#       self.index = 0
#     if self.index >= len(self.file_rows):
#       self.index = len(self.file_rows) - 1

#     file_row = self.file_rows[self.index]

#     # Safe getter for dict or Row
#     def get_val(name, default=None):
#       try:
#         return file_row[name]
#       except Exception:
#         if isinstance(file_row, dict):
#           return file_row.get(name, default)
#         return default

#     # Hide content widgets first
#     self.you_tube_video.visible = False
#     self.image_preview.visible = False
#     self.iframe_pdf.visible = False
#     self.video_player.visible = False
#     self.textarea_text.visible = False
#     self.label_info.visible = False
#     self.iframe_web.visible = False

#     # Header fields
#     self.title = get_val("title", "") or ""
#     self.comments = get_val("comments", "") or ""
#     notes_text = get_val("notes", "") or ""

#     # label_name ← title
#     self.label_name.text = self.title

#     # label_info ← comments (set here for convenience; individual show_* may tweak)
#     self.label_info.text = self.comments
#     self.label_info.visible = bool(self.comments)

#     # label_notes ← notes
#     self.label_notes.text = notes_text or ""
#     self.notes_panel.visible = bool(notes_text)
#     self.label_notes.visible = bool(notes_text)

#     # Media and URLs
#     self.media = get_val("file", None)
#     if self.media:
#       self.mime_type = self.media.content_type.lower()
#       self.link_download.visible = True
#     else:
#       self.mime_type = None
#       # We'll still show download/open button for web/YouTube, via _update_nav_buttons

#     self.youtube_url = get_val("youtube_url", None)
#     self.web_url = get_val("web_url", None)

#     # N of M
#     if hasattr(self, "label_index"):
#       n = self.index + 1
#       m = len(self.file_rows)
#       self.label_index.text = f"{n} of {m}"

#     print(
#       f"[FileViewerDT] index={self.index}, mime_type={self.mime_type}, "
#       f"youtube_url={self.youtube_url}, web_url={self.web_url}"
#     )

#     # ---------- PRIORITY 1: YOUTUBE ----------
#     if self.youtube_url:
#       self._show_youtube()
#       self._update_nav_buttons()
#       return

#     # ---------- PRIORITY 2: WEB URL ----------
#     if self.web_url:
#       self._show_web()
#       self._update_nav_buttons()
#       return

#     # ---------- PRIORITY 3: REGULAR MEDIA ----------
#     if not self.media:
#       # No youtube, no web, no media: just show comments (and notes if present)
#       if self.comments:
#         self.label_info.text = self.comments
#         self.label_info.visible = True
#       self._update_nav_buttons()
#       return

#     # Route based on mime type
#     if self.mime_type.startswith("image/"):
#       print("[FileViewerDT] image found")
#       self._show_image()
#     elif self.mime_type == "application/pdf":
#       print("[FileViewerDT] pdf found")
#       self._show_pdf()
#     elif self.mime_type.startswith("video/"):
#       print("[FileViewerDT] video found")
#       self._show_video()
#     elif self.mime_type.startswith("text/") or self._looks_like_text(self.title):
#       print("[FileViewerDT] text found")
#       self._show_text()
#     else:
#       print("[FileViewerDT] unsupported type found")
#       self.label_info.visible = True
#       self.label_info.text = f"Unsupported type for now: {self.mime_type}"

#     # Update Prev/Next visibility and download/open button
#     self._update_nav_buttons()

#   # ----------------- navigation buttons -----------------

#   def _update_nav_buttons(self):
#     self.link_previous.visible = (self.index > 0)
#     self.link_next.visible = (self.index < len(self.file_rows) - 1)

#     has_file = bool(self.media)
#     has_web = bool(self.web_url)
#     has_youtube = bool(self.youtube_url)

#     # Decide what the download/open button does
#     if has_web or has_youtube:
#       self.link_download.icon = "fa:external-link"
#       self.link_download.tooltip = "Open in New Tab"
#       self.link_download.visible = True
#     elif has_file:
#       self.link_download.icon = "fa:download"
#       self.link_download.tooltip = "Download File"
#       self.link_download.visible = True
#     else:
#       self.link_download.visible = False

#     # IMPORTANT: We no longer hide notes_panel here.
#     # Notes visibility is controlled solely by whether notes exist.

#   def link_previous_click(self, **event_args):
#     if self.index > 0:
#       self.index -= 1
#       self._load_current_file()

#   def link_next_click(self, **event_args):
#     if self.index < len(self.file_rows) - 1:
#       self.index += 1
#       self._load_current_file()

#   # ----------------- display helpers -----------------

#   def _show_youtube(self):
#     print("entering _show_youtube.")

#     # Comments already set in label_info; ensure visible if present
#     if self.comments:
#       self.label_info.text = self.comments
#       self.label_info.visible = True

#     url = (self.youtube_url or "").strip()

#     # Extract video ID from common YouTube URL formats
#     video_id = None
#     if "watch?v=" in url:
#       video_id = url.split("watch?v=", 1)[1].split("&", 1)[0]
#     elif "youtu.be/" in url:
#       video_id = url.split("youtu.be/", 1)[1].split("?", 1)[0]
#     else:
#       video_id = url

#     # Ensure referrer policy for iframe (forum snippet)
#     node = get_dom_node(self.you_tube_video)
#     iframe = node.querySelector("iframe") or node
#     if iframe:
#       iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin")

#     self.you_tube_video.youtube_id = video_id
#     self.you_tube_video.visible = True

#   def _show_image(self):
#     self.image_preview.source = self.media
#     self.image_preview.visible = True
#     if self.comments:
#       self.label_info.text = self.comments
#       self.label_info.visible = True

#   def _show_pdf(self):
#     if self.comments:
#       self.label_info.visible = True
#       self.label_info.text = self.comments
#     docurl = self.media.get_url(False)
#     self.iframe_pdf.url = docurl
#     self.iframe_pdf.visible = True

#   def _show_video(self):
#     if self.comments:
#       self.label_info.visible = True
#       self.label_info.text = self.comments

#     self.video_player.height = 500
#     self.video_player.width = 1000

#     url = self.media.get_url(False)
#     self.video_player.source = url
#     self.video_player.visible = True

#   def _show_text(self):
#     if self.comments:
#       self.label_info.visible = True
#       self.label_info.text = self.comments

#     text = anvil.server.call('get_text_from_media', self.media)
#     self.textarea_text.text = text
#     self.textarea_text.auto_expand = True
#     self.textarea_text.visible = True

#   def _looks_like_text(self, title):
#     title = (title or "").lower()
#     return (
#       title.endswith(".txt") or
#       title.endswith(".csv") or
#       title.endswith(".md") or
#       title.endswith(".log")
#     )

#   def _show_web(self):
#     if self.comments:
#       self.label_info.text = self.comments
#       self.label_info.visible = True

#     url = (self.web_url or "").strip()
#     print(f"[FileViewerDT] web_url={url}")

#     self.iframe_web.url = url
#     self.iframe_web.visible = True

#   # ----------------- download + close -----------------

#   def link_download_click(self, **event_args):
#     # 1) If we have a file, download it
#     if self.media:
#       anvil.media.download(self.media)
#       return

#     # 2) If we have a web link, open it in a new tab
#     if self.web_url:
#       url = (self.web_url or "").strip()
#       if url:
#         anvil.js.window.open(url, "_blank")
#       return

#     # 3) If we have a YouTube URL, open the YouTube page
#     if self.youtube_url:
#       url = (self.youtube_url or "").strip()
#       if url:
#         anvil.js.window.open(url, "_blank")
#       return

#     # 4) Fallback: nothing to download/open
#     Notification("Nothing to download or open.", style="warning").show()

#   def link_to_close_click(self, **event_args):
#     self.raise_event("x-close-alert", value=None)


# class FileViewerDT(FileViewerDTTemplate):
#   def __init__(self, file_rows, start_index=0, **properties):
#     self.init_components(**properties)

#     # Store the list and current index
#     self.file_rows = list(file_rows)
#     self.index = start_index
    
#     # Load the initial file right away
#     self._load_current_file()

#   # ----------------- core loader / router -----------------

#   def _load_current_file(self):
#     # No files? show message and bail
#     if not self.file_rows:
#       self.label_info.visible = True
#       # self.label_info.text = "No files to display."
#       if hasattr(self, "label_index"):
#         self.label_index.text = ""
#       self.link_download.visible = False
#       return

#     # Clamp index just in case
#     if self.index < 0:
#       self.index = 0
#     if self.index >= len(self.file_rows):
#       self.index = len(self.file_rows) - 1

#     file_row = self.file_rows[self.index]

#     # Hide everything first
#     self.you_tube_video.visible = False
#     self.image_preview.visible = False
#     self.iframe_pdf.visible = False
#     self.video_player.visible = False
#     self.textarea_text.visible = False
#     self.label_info.visible = False
#     self.iframe_web.visible = False

#     # Normalize from Data Table row
#     self.title = file_row['title']
#     self.comments = file_row['comments']

#     #New, adding the notes field
#     notes_text = file_row.get('notes') or ''
#     if notes_text:
#       notes_text = '\nNOTES: \n' + notes_text
#     self.notes_panel.visible = bool(notes_text)
#     self.label_notes.text = notes_text
#     self.label_notes.visible = True
    
#     # Media may be None
#     self.media = file_row['file']    
#     if self.media:
#       self.mime_type = self.media.content_type.lower()
#       self.link_download.visible = True
#       # self.label_notes.visible = False
#     else:
#       self.mime_type = None

#     # NEW: YouTube URL (may or may not exist)
#     try:
#       self.youtube_url = file_row['youtube_url']
#       # self.label_notes.visible = False
#     except KeyError:
#       self.youtube_url = None  

#     # Web URL (may or may not exist)
#     try:
#       self.web_url = file_row['web_url']
#     except (KeyError, TypeError):
#       self.web_url = None
    
#     # Set the title (top of the alert)
#     self.label_name.text = self.title

#     # 👉 NEW: set "N of M" label
#     if hasattr(self, "label_index"):
#       n = self.index + 1
#       m = len(self.file_rows)
#       self.label_index.text = f"{n} of {m}"

#     print(f"[FileViewerDT] index={self.index}, mime_type={self.mime_type}, youtube_url={self.youtube_url}, web_url={self.web_url}")


#     # ---------- PRIORITY 1: YOUTUBE ----------
#     if self.youtube_url:
#       print('YouTube url found')
#       # self.label_notes.visible = False
#       self._show_youtube()
#       self._update_nav_buttons()
#       return

#     # ---------- PRIORITY 2: WEB URL ----------
#     if self.web_url:
#       # self.label_notes.visible = False
#       self._show_web()
#       self._update_nav_buttons()
#       return
    
#     # ---------- PRIORITY 3: REGULAR MEDIA ----------
  
#     # If no media and no YouTube, show placeholder
#     if not self.media:
#       self.label_info.visible = True
#       self.label_info.text = self.comments #"No file attached."
#       self._update_nav_buttons()
#       return
    
#     # Route based on mime type
#     if self.mime_type.startswith("image/"):
#       print("[FileViewerDT] image found")
#       self._show_image()
#     elif self.mime_type == "application/pdf":
#       print("[FileViewerDT] pdf found")
#       self._show_pdf()
#     elif self.mime_type.startswith("video/"):
#       print("[FileViewerDT] video found")
#       self._show_video()
#     elif self.mime_type.startswith("text/") or self._looks_like_text(self.title):
#       print("[FileViewerDT] text found")
#       self._show_text()
#     else:
#       print("[FileViewerDT] unsupported type found")
#       self.label_info.visible = True
#       self.label_info.text = f"Unsupported type for now: {self.mime_type}"

#     # Update Prev/Next visibility
#     self._update_nav_buttons()


#   # ----------------- navigation buttons -----------------

#   def _update_nav_buttons(self):
#     # using your link names: link_previous, link_next
#     self.link_previous.visible = (self.index > 0)
#     self.link_next.visible = (self.index < len(self.file_rows) - 1)
#     has_file = bool(self.media)
#     has_web = bool(getattr(self, "web_url", None))
#     has_youtube = bool(getattr(self, "youtube_url", None))
#     if has_web or has_youtube:
#       self.notes_panel.visible = False
#       self.link_download.icon = "fa:external-link"
#       self.link_download.tooltip = "Open in New Tab"
#       self.link_download.visible = True
#     if has_file:
#       self.notes_panel.visible = False
#       self.link_download.icon = "fa:download"
#       self.link_download.tooltip = "Download File"
#       self.link_download.visible = True      
    

#   def link_previous_click(self, **event_args):
#     if self.index > 0:
#       self.index -= 1
#       self._load_current_file()

#   def link_next_click(self, **event_args):
#     if self.index < len(self.file_rows) - 1:
#       self.index += 1
#       self._load_current_file()

  
#   # ----------------- display helpers -----------------
#   def _show_youtube(self):
#     # Optional comments text
#     print('entering show_youtube.')
#     if self.comments:
#       self.label_info.text = self.comments
#       self.label_info.visible = True
  
#     url = (self.youtube_url or "").strip()
  
#     # Extract video ID from common YouTube URL formats
#     video_id = None
#     if "watch?v=" in url:
#       video_id = url.split("watch?v=", 1)[1].split("&", 1)[0]
#     elif "youtu.be/" in url:
#       video_id = url.split("youtu.be/", 1)[1].split("?", 1)[0]
#     else:
#       # If user pasted an ID directly, just use it
#       video_id = url
  
#     #Code from Forum
#     node = get_dom_node(self.you_tube_video)
#     iframe = node.querySelector("iframe") or node
#     if iframe:
#       iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin")    
    
#     # Anvil YouTube component expects the VIDEO ID as .source
#     self.you_tube_video.youtube_id = video_id
#     self.you_tube_video.visible = True

#   def _show_image(self):
#     self.image_preview.source = self.media
#     self.image_preview.visible = True
#     self.label_info.text = self.comments
#     self.label_info.visible = True

#   def _show_pdf(self):
#     self.label_info.visible = True
#     self.label_info.text = self.comments
#     docurl = self.media.get_url(False)
#     self.iframe_pdf.url = docurl
#     self.iframe_pdf.visible = True

#   def _show_video(self):
#     self.label_info.visible = True
#     self.label_info.text = self.comments

#     self.video_player.height = 500
#     self.video_player.width = 1000

#     url = self.media.get_url(False)
#     self.video_player.source = url
#     self.video_player.visible = True

#   def _show_text(self):
#     self.label_info.visible = True
#     self.label_info.text = self.comments

#     text = anvil.server.call('get_text_from_media', self.media)
#     self.textarea_text.text = text
#     self.textarea_text.auto_expand = True
#     self.textarea_text.visible = True

#   def _looks_like_text(self, title):
#     title = title.lower()
#     return (
#       title.endswith(".txt") or
#       title.endswith(".csv") or
#       title.endswith(".md") or
#       title.endswith(".log")
#     )

#   def _show_web(self):
#     # Optional comments text
#     if self.comments:
#       self.label_info.text = self.comments
#       self.label_info.visible = True
  
#     url = (self.web_url or "").strip()
#     print(f"[FileViewerDT] web_url={url}")
  
#     # Just load the URL into the iframe
#     self.iframe_web.url = url
#     self.iframe_web.visible = True

#   # ----------------- download + close -----------------

#   def link_download_click(self, **event_args):
#     #New to handle web/yt/files
#     # 1) If we have a file, download it
#     if self.media:
#       anvil.media.download(self.media)
#       return

#     # 2) If we have a web link, open it in a new tab
#     if getattr(self, "web_url", None):
#       url = (self.web_url or "").strip()
#       if url:
#         anvil.js.window.open(url, "_blank")
#       return
  
#     # 3) If we have a YouTube URL, open the YouTube page
#     if getattr(self, "youtube_url", None):
#       url = (self.youtube_url or "").strip()
#       if url:
#         anvil.js.window.open(url, "_blank")
#       return
  
#     # 4) Fallback: nothing to download/open
#     Notification("Nothing to download or open.", style="warning").show()    


#   def link_to_close_click(self, **event_args):
#     # alert.close_alert()
#     self.raise_event("x-close-alert", value=None)