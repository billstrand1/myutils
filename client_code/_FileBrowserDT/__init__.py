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


'''




'''


class _FileBrowserDT(_FileBrowserDTTemplate):
  def __init__(self, items=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    print("Opening FileBrowserDT")
    # Any code you write here will run before the form opens.

    if items is None:
      print('items is none, searching....')
      # items = app_tables.files.search(title='Rick Roll')
      items = app_tables.files.search()
      expanded_rows = fu.expand_file_rows(items)
      # expanded_rows = anvil.server.call('expand_file_rows', items)
      
      #Try new expanded file rows:

    # items = list(items)
    print(items)
    if items:
      print(f'len items = {len(items)}')

    
    self.repeating_panel_files.items = expanded_rows #items
