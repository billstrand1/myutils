from ._anvil_designer import DirectoryTemplateDisplayOnlyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ...DirectoryEdit import DirectoryEdit
from ... import Globals

class DirectoryTemplateDisplayOnly(DirectoryTemplateDisplayOnlyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()

