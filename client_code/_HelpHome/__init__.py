from ._anvil_designer import _HelpHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._HelpLoggedIn import _HelpLoggedIn
from ._HelpLoggedOut import _HelpLoggedOut

class _HelpHome(_HelpHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    #------------------VERIFY FALSE AFTER TESTING
    # DEBUG = False
    # if DEBUG:
    #   print("MyUtils Calling for log-in, DON'T FORGET TO set DEBUG=False")
    #   anvil.server.call('force_debug_login_shr_utils')
      
    self.help_panel.clear()
    
    user = anvil.users.get_user()
    if user:
      self.help_panel.add_component(_HelpLoggedIn())
    else:
      self.help_panel.add_component(_HelpLoggedOut())
      
