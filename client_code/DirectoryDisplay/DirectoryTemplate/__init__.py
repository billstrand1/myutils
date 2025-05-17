from ._anvil_designer import DirectoryTemplateTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DirectoryTemplate(DirectoryTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_delete_click(self, **event_args):
    user = anvil.users.get_user()
    user_full_name = f"{user['first_name']} {user['last_name']}"
    print(f"Directory Delete accessed by: {user_full_name}")
    self.member_copy = dict(self.item)

    member_to_delete = f"{self.member_copy['first_name']} {self.member_copy['last_name']}"
    print(f"{member_to_delete} is about to be deleted.")
    question = f"Are you sure you want to delete {member_to_delete} from the Directory?"
    delete = anvil.alert(
      content=question,
      title="Confirm Delete Member",
      buttons=[("Yes", True), ("No", False)],
      large=False
    )
    if delete:
      self.parent.raise_event('x-delete-member', member=self.item)    

    #Email to Bill of the deletion:
    # board_member = 
    message = (f"{user_full_name} DELETED {member_to_delete} \n{self.member_copy} in the User Table")
    print(message)
    anvil.server.call('email_change', message, subject='Deleting Member')    

