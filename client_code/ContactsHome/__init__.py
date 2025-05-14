from ._anvil_designer import ContactsHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
from ..ContactsEdit import ContactsEdit

class ContactsHome(ContactsHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #Had to go back to Links in the ButtonMenu, I couldn't get the click() to work.

  #   menu_item_1 = m3.MenuItem(text="Create New Contact", tag='create')
  #   menu_item_2 = m3.MenuItem(text="Edit Contact", tag='edit')    
  #   self.MultiButton.menu_items = [menu_item_1, menu_item_2]

  #   self.MultiButton.set_event_handler('x-change', self.menu_item_selected)
    
  # def menu_item_selected(self, **event_args):
  #   item = event_args.get('value')  # This is the MenuItem that was clicked
  #   if not item:
  #     return

  #   action = item.tag
  #   if action == "create":
  #     alert("Creating new contact...")
  #   elif action == "import":
  #     alert("Importing contacts...")
  #   elif action == "export":
  #     alert("Exporting contacts...")
  
  def add_contacts_click(self, **event_args):
    new_contact = {}
    save_clicked = alert(
        content=ContactsEdit(item=new_contact),
        title="Add Contact",
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
    )
    if save_clicked:
      print(new_contact)
    


  def link_1_click(self, **event_args):
    alert("Edit button clicked....")
