from ._anvil_designer import DirectoryDisplayOnlyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# from ... import Globals

class DirectoryDisplayOnly(DirectoryDisplayOnlyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_directory()

    
  def refresh_directory(self):
    self.refresh_data_bindings()
    self.directory_panel.items = anvil.server.call('get_directory')
    self.directory_lbl.role = None
    self.directory_lbl.display_font = 'menlo'
    self.directory_lbl.text = anvil.server.call('get_directory_str')
    self.directory_lbl.visible = True
