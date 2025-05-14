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
    new_contact = {}
    save_clicked = alert(
        content=DirectoryEdit(item=new_contact),
        title="Add Contact",
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
    )
    if save_clicked:
      print(new_contact)
  

  def edit_contact_click(self, **event_args):
    alert("Edit button clicked....")
