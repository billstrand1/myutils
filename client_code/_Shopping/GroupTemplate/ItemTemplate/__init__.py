from ._anvil_designer import ItemTemplateTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import Globals

class ItemTemplate(ItemTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    current_user = anvil.users.get_user()
    is_owner = self.item['user'] == current_user

    has_permission = is_owner or Globals.is_admin
    # print(f"has_permission: {has_permission}, Globals.is_admin: {Globals.is_admin}")

    # UI Control
    self.check_box_1.enabled = has_permission
    self.button_edit.visible = has_permission
    self.button_delete.visible = has_permission

    # UI Control
    # The CheckBox is disabled for others, but the Label is always enabled (dark)
    self.check_box_1.enabled = has_permission 
    self.button_edit.visible = has_permission 
    self.button_delete.visible = has_permission 

    # Setting values
    self.label_item_name.text = self.item['item_name'] # The text stays dark
    self.check_box_1.checked = self.item['completed']

    # Text display
    self.label_item_name.text = self.item['item_name']
    self.check_box_1.checked = self.item['completed']
    self.label_item_name.foreground = "#888" if self.item['completed'] else "black"

  @handle("check_box_1", "change")
  def check_box_1_change(self, **event_args):
    is_checked = self.check_box_1.checked
    anvil.server.call('update_item', self.item, {'completed': is_checked})
  
    # Manually update the label color immediately
    self.label_item_name.foreground = "#888" if is_checked else "black"
      
  
  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):
    if confirm(f"Delete {self.item['item_name']}?"):
      anvil.server.call('delete_item', self.item)
      # Tell the very top form to refresh everything
      self.parent.raise_event('x-refresh-all')

  @handle("button_edit", "click")
  def button_edit_click(self, **event_args):
    # edit_box = TextBox(text=self.item['item_name'])
    
    # if alert(content=edit_box, title="Edit Item", buttons=[("Save", True), ("Cancel", False)]):
    #   anvil.server.call('update_item', self.item, {'item_name': edit_box.text})
    #   self.parent.raise_event('x-refresh-all')

      # 1. Create the edit box
    edit_box = TextBox(text=self.item['item_name'])

    # 2. Show the alert
    if alert(content=edit_box, title="Edit Item", buttons=[("Save", True), ("Cancel", False)]):
      new_name = edit_box.text

      # 3. Call the server
      anvil.server.call('update_item', self.item, {'item_name': new_name})

      # 4. FIX: Manually update the local UI components
      # This ensures the user sees the change immediately
      self.item['item_name'] = new_name
      self.label_item_name.text = new_name 

      # 5. Optional: If you want a full list refresh (to re-sort etc.)
      # get_open_form().refresh_list()