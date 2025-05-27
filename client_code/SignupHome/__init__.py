from ._anvil_designer import SignupHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .TeeTimeTemplate import TeeTimeTemplate
from .. import Globals
from m3 import components


class SignupHome(SignupHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.signup_panel.add_component(TeeTimeTemplate())
    # Any code you write here will run before the form opens.


      
    

