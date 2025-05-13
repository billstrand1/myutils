from ._anvil_designer import HelpLoggedInTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class HelpLoggedIn(HelpLoggedInTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    #------------------VERIFY FALSE AFTER TESTING
    # DEBUG = True
    # if DEBUG:
    #   print("Calling for log-in, DON'T FORGET TO set DEBUG=False")
    #   anvil.server.call('force_debug_login_shr_utils')
    
    user = anvil.users.get_user()
    full_name = f"{user['first_name']} {user['last_name']}"
    self.name_label.text = (f"{full_name}, {user['email']}")


  def submit_button_click(self, **event_args):
    name_email = self.name_label.text
    comment = self.comment_area.text.strip()

    # --- Validation ---
    if not comment:
      Notification("Please enter your question or comment.", title="Message", style="danger").show()
      return

    comment_dict = {
      "name-email": name_email, 
      "comment": comment
    }

    # --- Server call ---
    try:
      anvil.server.call('add_comment', comment_dict)  
      alert("Question / Comment submitted,\nthank you.\n\nI'll reply shortly.", title="Received")
      # Clear the form
      self.comment_area.text = ""

    except Exception as e:
      Notification("Something went wrong. Please try again.",
                   title="Message", style="danger").show()
