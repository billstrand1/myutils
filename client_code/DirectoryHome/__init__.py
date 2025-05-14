from ._anvil_designer import DirectoryHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
from ..DirectoryEdit import DirectoryEdit

class DirectoryHome(DirectoryHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #Had to go back to Links in the ButtonMenu, I couldn't get the click() to work.

    menu_add = m3.MenuItem(text="Create New Contact", tag='create')
    menu_edit = m3.MenuItem(text="Edit Contact", tag='edit')    
    self.MultiButton.menu_items = [menu_add, menu_edit]

    menu_add.add_event_handler('click', self.add_contact_click)
    menu_edit.add_event_handler('click', self.edit_contact_click)


  #Do the WhileTrue loop here....
  def add_contact_click(self, **event_args):
    user = anvil.users.get_user()
    if user:
      print(f" {user['first_name']} {user['last_name']} is adding a new Member")
    new_contact = {'first_name': '',
                  'last_name': '',
                   'email': '',
                   'phone': '',
                   'birth_month': '',
                   'birth_day': ''}
    
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
        
        if not new_contact['first_name']:
          alert ("Please enter first name.", title="Input Error")
          continue

        if not new_contact['last_name']:
          alert ("Please enter last name.", title="Input Error")
          continue

        email = new_contact['email']
        if not email or not anvil.server.call('is_valid_email', email):
          alert ("Please enter valid email address.", title="Input Error")
          continue     

        phone = new_contact['phone']
        if phone:
          if not anvil.server.call('is_valid_phone', phone):          
            alert ("Please enter a valid phone number (without spaces).", title="Input Error")
            continue

        birth_month = new_contact['birth_month']
        birth_day = new_contact['birth_day']
        if birth_month:
          if not (1 <= birth_month <= 12):
            alert(content="Birth month must be between 1 and 12.", title="Input Error")
            continue
        if birth_day:
          if not (1 <= birth_day <= 31):
            alert(content="Birth day must be between 1 and 31.", title="Input Error")
            continue   
        if birth_day and not birth_month:
          alert(content="Please enter both birth month & day, or neither.", title="Input Error")
          continue
        if not birth_day and  birth_month:
          alert(content="Please enter both birth month & day, or neither.", title="Input Error")
          continue
            
      break

      #Now work on Server Code to add contacts.
      
    # new_member['password_hash'] = '$2a$10$u5ACOKz.JMvf2hP.aC8gNOXxmA17vbcayt0CJFkeE.MpKM5tLMgXu' 

  def edit_contact_click(self, **event_args):
    alert("Edit button clicked....")
