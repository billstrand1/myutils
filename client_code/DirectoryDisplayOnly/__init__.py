from ._anvil_designer import DirectoryDisplayOnlyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# import m3.components as m3
# from ..DirectoryEdi÷t import DirectoryEdit
from .. import Globals

class DirectoryDisplayOnly(DirectoryDisplayOnlyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.directory_panel.items = anvil.server.call('get_directory')
    self.refresh_directory()
    self.directory_panel.set_event_handler('x-delete-member', self.delete_member)
    # self.directory_panel.set_event_handler('x-refresh_directory', self.refresh_directory)

    # ------------------VERIFY FALSE AFTER TESTING
    DEBUG = True
    if DEBUG:
      print("Calling for log-in, DON'T FORGET TO set DEBUG=False")
      anvil.server.call('force_debug_login_shr_utils')

    user = anvil.users.get_user()
    print(f"DirectoryDisplay user = {user['first_name']}")
    admin = anvil.server.call('has_role', user, 'admin')
    self.button_add_member.visible = bool(admin)


  # def validate_member_data(self, member):
  #   if not member['first_name']:
  #     return "Please enter first name."
  #   if not member['last_name']:
  #     return "Please enter last name."
  #   if not member['email'] or not anvil.server.call('is_valid_email', member['email']):
  #     return "Please enter a valid email address."
  #   if member.get('phone') and not anvil.server.call('is_valid_phone', member['phone']):
  #     return "Please enter a valid 10 digit phone number."
  #   if (member.get('birth_month') and not (1 <= member['birth_month'] <= 12)) or \
  #   (member.get('birth_day') and not (1 <= member['birth_day'] <= 31)):
  #     return "Birth date must be valid."
  #   if bool(member.get('birth_month')) ^ bool(member.get('birth_day')):
  #     return "Please enter both birth month & day, or neither."
  #   return None

  def refresh_directory(self):
    self.refresh_data_bindings()
    self.directory_panel.items = anvil.server.call('get_directory')

  def delete_member(self, member, **event_args):
    # Delete the score
    anvil.server.call('delete_member', member)
    self.refresh_directory()

  def button_add_member_click(self, **event_args):
    user = anvil.users.get_user()
    if user:
      print(f" {user['first_name']} {user['last_name']} is adding a new Member")

    new_contact = {'first_name': '',
                   'last_name': '',
                   'email': '',
                   'signup_name': '',
                   'phone': '',
                   'birth_month': None,
                   'birth_day': None}

    player_add_form = DirectoryEdit(item=new_contact)

    while True: # Keep looping until valid input is provided
      save_clicked = alert(
        content=player_add_form,
        title="Add Contact",
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
      )

      if save_clicked:
        print(new_contact)
        print(f"First Name: {new_contact['first_name']}")

        # error = self.validate_member_data(new_contact)
        error = Globals.validate_member_data(new_contact)

        if error:
          alert(error, title="Input Error")
          continue

        #Set to appropriate string modes
        if new_contact['first_name']:
          new_contact['first_name'] = new_contact['first_name'].title()
        if new_contact['last_name']:
          new_contact['last_name'] = new_contact['last_name'].title()
        if new_contact['email']:
          new_contact['email'] = new_contact['email'].lower()

        # if not new_contact['first_name']:
        #   alert ("Please enter first name.", title="Input Error")
        #   continue

        # if not new_contact['last_name']:
        #   alert ("Please enter last name.", title="Input Error")
        #   continue

        # email = new_contact['email']
        # if not email or not anvil.server.call('is_valid_email', email):
        #   alert ("Please enter valid email address.", title="Input Error")
        #   continue

        # phone = new_contact['phone']
        # if phone:
        #   if not anvil.server.call('is_valid_phone', phone):
        #     alert ("Please enter a valid 10 digit phone number.", title="Input Error")
        #     continue

        # birth_month = new_contact['birth_month']
        # birth_day = new_contact['birth_day']

        # if birth_month:
        #   if not (1 <= birth_month <= 12):
        #     alert(content="Birth month must be between 1 and 12.", title="Input Error")
        #     continue
        # if birth_day:
        #   if not (1 <= birth_day <= 31):
        #     alert(content="Birth day must be between 1 and 31.", title="Input Error")
        #     continue
        # if birth_day and not birth_month:
        #   alert(content="Please enter both birth month & day, or neither.", title="Input Error")
        #   continue
        # if not birth_day and  birth_month:
        #   alert(content="Please enter both birth month & day, or neither.", title="Input Error")
        #   continue

        if not new_contact['signup_name']:
          new_contact['signup_name'] = f"{new_contact['last_name']}, {new_contact['first_name']}"

      break

    ##Now work on Server Code to add contacts.
    new_contact['password_hash'] = '$2a$10$u5ACOKz.JMvf2hP.aC8gNOXxmA17vbcayt0CJFkeE.MpKM5tLMgXu'
    new_contact['roles'] = None
    new_contact['enabled'] = True
    # new_contact['signup_name'] = f"{new_contact['last_name']}, {new_contact['first_name']}"
    new_contact['couple_id'] = new_contact['last_name'].lower()


    anvil.server.call('add_new_member', new_contact)

    if user:
      message = f"{new_contact['first_name']} {new_contact['last_name']}, {new_contact['email']} added by {user['first_name']} {user['last_name']}."
      anvil.server.call('email_change', message)
      Notification(f"{new_contact['first_name']} added, thanks {user['first_name']}.").show()
    else:
      message = f"{new_contact['first_name']} {new_contact['last_name']} added to directory."
      Notification(f"{new_contact['first_name']} added, thanks.").show()
      anvil.server.call('email_change', message)
    self.refresh_directory()
