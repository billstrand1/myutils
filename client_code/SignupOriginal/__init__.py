from ._anvil_designer import SignupOriginalTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SignupOriginal(SignupOriginalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # ------------------Comment out before cloning, run from data_functions Server Code
    # print('Calling for log-in')
    # anvil.server.call('force_debug_login_shr_utils')
    # self.user = anvil.users.get_user()

    user = anvil.users.get_user()
    if not user:
      user = anvil.users.login_with_form()
    print(f"{user['last_name']} is logged in") 
    
    #-----Do not want this running in Globals, make it upon first form_show.
    print('globals checking for past activities')
    past_activities = anvil.server.call('get_past_activities')
    print(f"globals, past_activities size = {len(past_activities)}")
    if len(past_activities) > 0:
      for activity in past_activities:
        anvil.server.call('delete_activity', activity)
    # Any code you write here will run before the form opens.

  def button_add_click(self, **event_args):
    pass
    
