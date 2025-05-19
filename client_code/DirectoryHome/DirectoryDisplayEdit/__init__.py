from ._anvil_designer import DirectoryDisplayEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import m3.components as m3
from ... import Globals
from ..DirectoryEdit import DirectoryEdit

class DirectoryDisplayEdit(DirectoryDisplayEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_directory()
    self.directory_panel.set_event_handler('x-delete-member', self.delete_member)
          
  
  def refresh_directory(self):
    self.refresh_data_bindings()
    self.directory_panel.items = anvil.server.call('get_directory')
  
  def delete_member(self, member, **event_args):
    anvil.server.call('delete_member', member)
    self.refresh_directory()
