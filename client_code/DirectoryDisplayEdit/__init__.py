from ._anvil_designer import DirectoryDisplayEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import m3.components as m3
from ..DirectoryEdit import DirectoryEdit
from .. import Globals

class DirectoryDisplayEdit(DirectoryDisplayEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.directory_panel.items = anvil.server.call('get_directory')
    self.refresh_directory()
    self.directory_panel.set_event_handler('x-delete-member', self.delete_member)
          
    user = anvil.users.get_user()
    if user:
      print(f"DirectoryDisplay user = {user['first_name']}")

  
  def refresh_directory(self):
    self.refresh_data_bindings()
    self.directory_panel.items = anvil.server.call('get_directory')
  
  def delete_member(self, member, **event_args):
    # Delete the score
    anvil.server.call('delete_member', member)
    self.refresh_directory()
