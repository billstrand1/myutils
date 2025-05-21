from ._anvil_designer import _DirectoryHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import m3.components as m3
from .DirectoryEdit import DirectoryEdit
from .DirectoryDisplayEdit import DirectoryDisplayEdit
from .DirectoryDisplayOnly import DirectoryDisplayOnly

from .. import Globals
from m3 import components

class _DirectoryHome(_DirectoryHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # #------------------VERIFY FALSE AFTER TESTING
    #ToDO:  icons for buttons:
    
    # DEBUG = True
    # if DEBUG:
    #   print("Calling for log-in DirectoryHome, DON'T FORGET TO set DEBUG=False")
    #   anvil.server.call('force_debug_login_shr_utils')

    user = anvil.users.get_user()
    if not user:
      user = anvil.users.login_with_form()
      
    admin = False
    if user:
      admin = anvil.server.call('has_role', user, 'admin')
      print(f'Admin: {admin}')
    

    if admin:
      # --------Menu Items
      menu_add = m3.MenuItem(text="Add New Member", leading_icon='mi:add')
      menu_edit = m3.MenuItem(text="Edit or Delete Members", leading_icon='mi:edit')    
      self.MultiButton.menu_items = [menu_add, menu_edit]        
      
      menu_add.add_event_handler('click', self.button_add_click)
      menu_edit.add_event_handler('click', self.edit_contacts_click)
    else:
      menu_edit_yourself = m3.MenuItem(text="Edit Your Conact Info", leading_icon='mi:edit')
      self.MultiButton.menu_items = [menu_edit_yourself]
      menu_edit_yourself.add_event_handler('click', self.edit_current_contact_click)

    self.directory_panel.clear()
    self.directory_panel.add_component(DirectoryDisplayOnly())

  #Only visible to Admin:
  def button_add_click(self, **event_args):
      user = anvil.users.get_user()
      if user:
        print(f" {user['first_name']} {user['last_name']} is adding a new Member")
  
      new_contact = {'first_name': '',
                    'last_name': '',
                    'email': '',
                    'signup_name': '',
                    'phone': '',
                    'birth_month': None,
                    'birth_day': None,
                    'roles': None}
  
      player_add_form = DirectoryEdit(item=new_contact)
  
      while True: # Keep looping until valid input is provided
        save_clicked = alert(
          content=player_add_form,
          title="Add Member",
          large=True,
          buttons=[("Save", True), ("Cancel", False)],
        )

        if not save_clicked:
          return  # or break

        error = Globals.validate_member_data(new_contact)
        player_add_form.first_name_box.error = False
        player_add_form.last_name_box.error = False
        player_add_form.email_box.error = False
        if error:
          if error == "Please enter first name.":
            player_add_form.first_name_box.error = True
          elif error == "Please enter last name.":
            player_add_form.last_name_box.error = True
          elif error == "Please enter a valid email address.":
            player_add_form.email_box.error = True                        
          alert(error, title="Input Error")
          continue

        #Set to appropriate string modes
        new_contact['first_name'] = new_contact['first_name'].title()
        new_contact['last_name'] = new_contact['last_name'].title()     
        new_contact['email'] = new_contact['email'].lower()          

        if not new_contact['signup_name']:
          new_contact['signup_name'] = f"{new_contact['last_name']}, {new_contact['first_name']}"
  
        break
  
      ##Now work on Server Code to add contacts.
      new_contact['password_hash'] = '$2a$10$u5ACOKz.JMvf2hP.aC8gNOXxmA17vbcayt0CJFkeE.MpKM5tLMgXu' 
      new_contact['enabled'] = True
      new_contact['couple_id'] = new_contact['last_name'].lower()   
      anvil.server.call('add_new_member', new_contact)
    
      message = f"{new_contact['first_name']} {new_contact['last_name']} added to directory."
      Notification(f"{new_contact['first_name']} added, thanks.").show()
      anvil.server.call('email_change', message, subject='Member Added')
    
      self.refresh_directory()
      
    
  def refresh_directory(self):
    self.refresh_data_bindings()
    self.directory_panel.clear()
    self.directory_panel.add_component(DirectoryDisplayOnly())


  def edit_contacts_click(self, **event_args):
    # alert("Edit button clicked....")
    self.directory_panel.clear()
    self.directory_panel.add_component(DirectoryDisplayEdit()) 


  def edit_current_contact_click(self, **event_args):
    # alert("Edit button clicked....")
    # self.directory_panel.clear()
    # self.directory_panel.add_component(DirectoryDisplayEdit()) 

    # ---------------TRY TO ONLY EDIT EXISTING MEMBER
    # def link_edit_click(self, **event_args):
    #   print('entering link_edit_click')
    user = anvil.users.get_user()    
    print(f"Directory Edit accessed by: {user['first_name']} {user['last_name']}")
    
    self.member_copy = dict(user)
    first_name = self.member_copy['first_name']
    last_name = self.member_copy['last_name']
    print(f"{first_name} {last_name} about to be edited.")
    
    member_edit_form = DirectoryEdit(item=self.member_copy)
    
    while True: # Keep looping until valid input is provided
      save_clicked = alert(
        content=member_edit_form,
        title="Edit Member",
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
      )
    
      if not save_clicked:
        return
    
        # if save_clicked:
        # print(self.member_copy)
      print(f"First Name: {self.member_copy['first_name']}")
    
      error = Globals.validate_member_data(self.member_copy)
      if error:
        alert(error, title="Input Error")
        continue

      # Keep first/last from changing.  Format email
      self.member_copy['first_name'] = first_name #self.member_copy['first_name'].title()
      self.member_copy['last_name'] = last_name #self.member_copy['last_name'].title()
      self.member_copy['email'] = self.member_copy['email'].lower()   
      if not self.member_copy['signup_name']:
        self.member_copy['signup_name'] = f"{self.member_copy['last_name']}, {self.member_copy['first_name']}"       
    
        # Save and notify
      anvil.server.call('update_member', user, self.member_copy)
      self.refresh_directory()
      
      # if user:
      message = f"{self.member_copy['first_name']} {self.member_copy['last_name']}, {self.member_copy['email']} updated by {user['first_name']} {user['last_name']}."
      anvil.server.call('email_change', message, subject='User Directory Edit')
      Notification(f"{self.member_copy['first_name']} updated, thanks.").show()
      # else: 
      #   message = f"{self.member_copy['first_name']} {self.member_copy['last_name']} added to directory."
      #   Notification(f"{self.member_copy['first_name']} added, thanks.").show()
      #   anvil.server.call('email_change', message, subject='User Directory Edit')
      break
    

    
