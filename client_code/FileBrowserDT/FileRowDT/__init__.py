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
    # print("labels exist?", hasattr(self, "label_title"), hasattr(self, "label_type"))
    # if hasattr(self, "label_title"):
    #   self.label_title.text = "TEST TITLE"
    # if hasattr(self, "label_type"):
    #   self.label_type.text = "TEST TYPE"
    print("Row init; components:",
          [c.name for c in self.get_components() if hasattr(c, "name")])
    row = self.item  # the data table row

    # Title
    self.label_title.text = row["description"]

    # MIME / Type
    media = row['file']
    mime = media.content_type.lower() if media else ""

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

  # def form_show(self, **event_args):
  #   # Description
  #   self.label_title.text = self.item["description"]

  #   # Get MIME type from the Media object
  #   media = self.item['file']
  #   mime = media.content_type.lower() if media else ""

  #   # Map MIME → human-readable type
  #   if mime.startswith("image/"):
  #     display_type = f"Image ({mime.split('/')[-1].upper()})"
  #   elif mime == "application/pdf":
  #     display_type = "PDF"
  #   elif mime.startswith("video/"):
  #     display_type = f"Video ({mime.split('/')[-1].upper()})"
  #   elif mime.startswith("text/"):
  #     display_type = f"Text ({mime.split('/')[-1].upper()})"
  #   else:
  #     display_type = f"Unknown ({mime})" if mime else "Unknown"

  #   self.label_type.text = display_type
  #   self.label_title.visible = True
  #   self.label_type.visible = True
