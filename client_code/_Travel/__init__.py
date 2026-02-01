import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .._FileBrowserDT.FileViewerDT import FileViewerDT

from anvil import *

def open_in_file_viewer_dt(*, title, file=None, web_url=None, youtube_url=None, comments=None):
  """
  Opens FileViewerDT inside an alert using the provided file/url data.
  Adjust the import path below to match your dependency module name.
  """
  # try:
  #   # Common patterns you’ve used previously
  #   from _FileBrowserDT import FileViewerDT
  # except ImportError:
  #   # If your dependency is named differently, adjust here
  #   from FileViewerDT import FileViewerDT

  
  file_row = {
    "description": title,
    "comments": comments,
    "file": file,                 # Media or None
    "web_url": web_url,           # string or None
    "youtube_url": youtube_url,   # string or None
  }

  viewer = FileViewerDT(file_rows=[file_row], start_index=0)
  alert(content=viewer, large=True, buttons=[])


def is_image(media_obj):
  if not media_obj: return False
  name = (getattr(media_obj, "name", "") or "").lower()
  return name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))

def get_youtube_thumb(url):
  import re
  m = re.search(r"(?:youtu\.be/|v=)([^?&]+)", url or "")
  return f"https://img.youtube.com/vi/{m.group(1)}/hqdefault.jpg" if m else None
  