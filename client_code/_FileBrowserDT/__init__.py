from ._anvil_designer import _FileBrowserDTTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .FileViewerDT import FileViewerDT
from .FileRowDT import FileRowDT
# from file_utils import *
from .. import file_utils as fu
# from anvil import app_tables
# import MyUtils.utils as fu  # adjust path if needed


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
    print(f"len(items) = {len(items)}")

    self.repeating_panel_files.items = items


# class _FileBrowserDT(_FileBrowserDTTemplate):
#   def __init__(self, items=None, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     print("Opening FileBrowserDT")

#     # `items` should normally be a list of already-expanded rows
#     # (dicts or Rows) with keys: title, comments, notes, file, youtube_url, web_url.
#     # If None, we default to using the Files table and expand it here.
#     if items is None:


#       print("items is None, loading from app_tables.files and expanding...")
#       base_rows = app_tables.files.search()
#       items = fu.expand_file_rows(
#         base_rows,
#         # For Files table, field names already match the viewer schema:
#         # title, comments, notes, file, youtube_url, web_url
#         copy_fields=[],
#         map_fields={}  # no mapping required for Files table
#       )

#     # Store and display
#     items = list(items)
#     if items:
#       print(f"len items = {len(items)}")

#     self.repeating_panel_files.items = items



# class _FileBrowserDT(_FileBrowserDTTemplate):
#   def __init__(self, items=None, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     # Any code you write here will run before the form opens.
#     print("Opening FileBrowserDT")
#     # Any code you write here will run before the form opens.

#     if items is None:
#       print('items is none, searching....')
#       # items = app_tables.files.search(title='Rick Roll')
#       items = app_tables.files.search()
#       expanded_rows = fu.expand_file_rows(items)
#       # expanded_rows = anvil.server.call('expand_file_rows', items)
      
#       #Try new expanded file rows:

#     # items = list(items)
#     print(items)
#     if items:
#       print(f'len items = {len(items)}')

    
#     self.repeating_panel_files.items = expanded_rows #items
