from ._anvil_designer import FileRowDTOldTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..FileViewerDT import FileViewerDT
from ..FileViewerDT import FileViewerDT

class FileRowDTOld(FileRowDTOldTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("[FileRowDT] row created")
    
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

  # def form_show(self, **event_args):
  #   # self.item is a DT Row
  #   self.label_title.text = self.item["description"]

  def form_show(self, **event_args):
    # Description
    self.label_title.text = self.item["description"]

    # Get MIME type from the Media object
    media = self.item['file']
    mime = media.content_type.lower() if media else ""

    # Map MIME → human-readable type
    if mime.startswith("image/"):
      display_type = f"Image ({mime.split('/')[-1].upper()})"
    elif mime == "application/pdf":
      display_type = "PDF"
    elif mime.startswith("video/"):
      display_type = f"Video ({mime.split('/')[-1].upper()})"
    elif mime.startswith("text/"):
      display_type = f"Text ({mime.split('/')[-1].upper()})"
    else:
      display_type = f"Unknown ({mime})" if mime else "Unknown"

    self.label_type.text = display_type

#New One.

# class FileRowDT(FileRowDTTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
    
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
#     # Any code you write here will run before the form opens.
#   def form_show(self, **event_args):
#     row = self.item
  
#     # Title
#     self.label_title.text = row["description"]
  
#     # Comments (optional)
#     comments = row.get("comments", "") if isinstance(row, dict) else row['comments']
#     self.label_comments.text = comments or ""
  
#     # File / mime
#     media = row['file']
#     mime = media.content_type.lower() if media else ""
  
#     # Type & icon
#     if mime.startswith("image/"):
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
#     else:
#       display_type = f"Unknown ({mime})" if mime else "Unknown"
#       icon = "❓"
  
#     self.label_type.text = display_type
#     self.label_icon.text = icon
