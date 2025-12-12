from ._anvil_designer import DirectoryDisplayHTMLTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DirectoryDisplayHTML(DirectoryDisplayHTMLTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
    self.html = anvil.server.call('get_directory_html')
  
