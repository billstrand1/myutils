from ._anvil_designer import HelpLoggedOutTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class HelpLoggedOut(HelpLoggedOutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def submit_button_click(self, **event_args):
    name = self.name_box.text.strip()
    email = self.email_box.text.strip()
    comment = self.comment_area.text.strip()

    # --- Validation ---
    if not name:
      Notification("Please enter your name.", title="Message", style="danger").show()
      return

    if not comment:
      Notification("Please enter your question or comment.", title="Message", style="danger").show()
      return

    if not email or not anvil.server.call('is_valid_email', email):
      Notification("Please enter a valid email address.", title="Message", style="danger").show()
      return  

    comment_dict = {
      "name-email": f"{name}, {email}", 
      "comment": comment
    }

    # --- Server call ---
    try:
      anvil.server.call('add_comment', comment_dict)

      alert("Question / Comment submitted,\nThank you.\n\nI'll reply shortly.", title="Received")
      # Clear the form
      self.comment_area.text = ""

    except Exception as e:
      Notification("Something went wrong. Please try again.",
                   title="Message", style="danger").show()


'''
        if not email or not self.is_valid_email(email):
            Notification("Please enter a valid email address.", title="Message", style="danger").show()
            return

        if not phone or not self.is_valid_phone(phone):
            Notification("Please enter a valid phone number (without spaces).", title="Message", style="danger").show()
            return

        if not message:
            Notification("Please enter your message or inquiry.", title="Message", style="danger").show()
            return        


'''