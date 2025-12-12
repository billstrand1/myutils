from ._anvil_designer import _FileBrowserDTTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .FileViewerDT import FileViewerDT
from .FileRowDT import FileRowDT

from .. import file_utils as fu

'''




'''

class _FileBrowserDT(_FileBrowserDTTemplate):
  def __init__(self, items=None, **properties):
    self.init_components(**properties)

    print("Opening FileBrowserDT")

    # If caller didn't pass items, load Files table by default
    if items is None:
      # from anvil.tables import app_tables
      # import MyUtils.utils as fu  # adjust if needed

      print("items is None, searching app_tables.files...")
      base_rows = app_tables.files.search()
      items = fu.expand_file_rows(base_rows)

    # IMPORTANT: Always bind the repeater to *items*
    items = list(items) if items else []
    print(f"from FileBrowserDT: len(items) = {len(items)}")

    self.repeating_panel_files.items = items

