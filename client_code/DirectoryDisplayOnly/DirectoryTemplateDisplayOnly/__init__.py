from ._anvil_designer import DirectoryTemplateDisplayOnlyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...DirectoryEdit import DirectoryEdit
from ... import Globals

class DirectoryTemplateDisplayOnly(DirectoryTemplateDisplayOnlyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()

    # ------------------VERIFY FALSE AFTER TESTING
    # DEBUG = True
    # if DEBUG:
    #   print("Calling for log-in, DON'T FORGET TO set DEBUG=False")
    #   anvil.server.call('force_debug_login_shr_utils')

    # user = anvil.users.get_user()

    # if user:
    #   print(f"in DirectoryTemplate, user = {user['email']}")
    #   admin = anvil.server.call('has_role', user, 'admin')
    #   self.link_edit.visible = bool(admin)
    #   self.link_delete.visible = bool(admin)

    #   if user['email'] == self.item['email']:
    #     print('user found')
    #     self.link_edit.visible = True
    # else:
    #   print('user not found in DirectoryTemplate')

  # def link_delete_click(self, **event_args):
  #   user = anvil.users.get_user()
  #   user_full_name = f"{user['first_name']} {user['last_name']}"
  #   print(f"Directory Delete accessed by: {user_full_name}")
  #   self.member_copy = dict(self.item)

  #   member_to_delete = f"{self.member_copy['first_name']} {self.member_copy['last_name']}"

  #   question = f"Are you sure you want to delete {member_to_delete} from the Directory?"
  #   delete = anvil.alert(
  #     content=question,
  #     title="Confirm Delete Member",
  #     buttons=[("Yes", True), ("No", False)],
  #     large=False
  #   )
  #   if delete:
  #     self.parent.raise_event('x-delete-member', member=self.item)
  #     message = (f"{user_full_name} DELETED {member_to_delete} \n{self.member_copy} in the User Table")
  #     print(message)
  #     anvil.server.call('email_change', message, subject='Deleting Member')

  # def link_edit_click(self, **event_args):
  #   print('entering link_edit_click')
  #   user = anvil.users.get_user()

  #   print(f"Directory Edit accessed by: {user['first_name']} {user['last_name']}")
  #   self.member_copy = dict(self.item)
  #   print(f"{self.member_copy['first_name']} {self.member_copy['last_name']} about to be edited.")

  #   member_edit_form = DirectoryEdit(item=self.member_copy)

  #   while True: # Keep looping until valid input is provided
  #     save_clicked = alert(
  #       content=member_edit_form,
  #       title="Edit Contact",
  #       large=True,
  #       buttons=[("Save", True), ("Cancel", False)],
  #     )

  #     if save_clicked:
  #       # print(self.member_copy)
  #       print(f"First Name: {self.member_copy['first_name']}")

  #       error = Globals.validate_member_data(self.member_copy)
  #       if error:
  #         alert(error, title="Input Error")
  #         continue

  #       if self.member_copy['first_name']:
  #         # print('setting First name to Title: ')
  #         self.member_copy['first_name'] = self.member_copy['first_name'].title()
  #       if self.member_copy['last_name']:
  #         print('setting Last name to Title')
  #         self.member_copy['last_name'] = self.member_copy['last_name'].title()
  #       if self.member_copy['email']:
  #         print('setting Email to Lower')
  #         self.member_copy['email'] = self.member_copy['email'].lower()

  #       # if not self.member_copy['first_name']:
  #       #   alert ("Please enter first name.", title="Input Error")
  #       #   continue

  #       # if not self.member_copy['last_name']:
  #       #   alert ("Please enter last name.", title="Input Error")
  #       #   continue

  #       # email = self.member_copy['email']
  #       # if not email or not anvil.server.call('is_valid_email', email):
  #       #   alert ("Please enter valid email address.", title="Input Error")
  #       #   continue

  #       # phone = self.member_copy['phone']
  #       # if phone:
  #       #   if not anvil.server.call('is_valid_phone', phone):
  #       #     alert ("Please enter a valid 10 digit phone number.", title="Input Error")
  #       #     continue

  #       # birth_month = self.member_copy['birth_month']
  #       # birth_day = self.member_copy['birth_day']

  #       # if birth_month:
  #       #   if not (1 <= birth_month <= 12):
  #       #     alert(content="Birth month must be between 1 and 12.", title="Input Error")
  #       #     continue
  #       # if birth_day:
  #       #   if not (1 <= birth_day <= 31):
  #       #     alert(content="Birth day must be between 1 and 31.", title="Input Error")
  #       #     continue
  #       # if birth_day and not birth_month:
  #       #   alert(content="Please enter both birth month & day, or neither.", title="Input Error")
  #       #   continue
  #       # if not birth_day and  birth_month:
  #       #   alert(content="Please enter both birth month & day, or neither.", title="Input Error")
  #       #   continue

  #       if not self.member_copy['signup_name']:
  #         self.member_copy['signup_name'] = f"{self.member_copy['last_name']}, {self.member_copy['first_name']}"

  #     break


  #   anvil.server.call('update_member', self.item, self.member_copy)
  #   print('calling parent refresh')
  #   # self.parent.raise_event('x-refresh-directory')
  #   self.refresh_data_bindings()

  #   if user:
  #     message = f"{self.member_copy['first_name']} {self.member_copy['last_name']}, {self.member_copy['email']} updated by {user['first_name']} {user['last_name']}."
  #     anvil.server.call('email_change', message)
  #     Notification(f"{self.member_copy['first_name']} updated, thanks {user['first_name']}.").show()
  #   else:
  #     message = f"{self.member_copy['first_name']} {self.member_copy['last_name']} added to directory."
  #     Notification(f"{self.member_copy['first_name']} added, thanks.").show()
  #     anvil.server.call('email_change', message)
