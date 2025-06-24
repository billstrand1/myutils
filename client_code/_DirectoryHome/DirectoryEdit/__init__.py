from ._anvil_designer import DirectoryEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DirectoryEdit(DirectoryEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #Note: You cannot change your first or last name, only Admin can do that.
    