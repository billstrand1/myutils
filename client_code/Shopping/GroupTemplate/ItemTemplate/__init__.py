from ._anvil_designer import ItemTemplateTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# class ItemTemplate(ItemTemplateTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)
#     # Hide buttons if the current user isn't the owner
# # ItemTemplate1 Code

class ItemTemplate(ItemTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    current_user = anvil.users.get_user()

    # Permission Logic
    is_owner = self.item['user'] == current_user
    is_admin = False
    if current_user and 'roles' in current_user and current_user['roles'] is not None:
      is_admin = 'admin' in current_user['roles']

    has_permission = is_owner or is_admin

    # UI Control
    # The CheckBox is disabled for others, but the Label is always enabled (dark)
    self.check_box_1.enabled = has_permission 
    self.button_edit.visible = has_permission 
    self.button_delete.visible = has_permission 

    # Setting values
    self.label_item_name.text = self.item['item_name'] # The text stays dark
    self.check_box_1.checked = self.item['completed']

    # Optional: Visual cue for completed items (Strike-through or Grey)
    if self.item['completed']:
      self.label_item_name.foreground = "#888" # Grey out text ONLY if completed
      # self.label_item_name.italic = True # Optional styling
    else:
      self.label_item_name.foreground = "black" # Dark text for active items

    # 1. Get the current user (this is cached, so it's fast)
    # current_user = anvil.users.get_user()

    # # 2. Define ownership
    # is_owner = self.item['user'] == current_user

    # # 3. Define admin status
    # # Check if 'roles' exists and 'admin' is inside the list
    # is_admin = False
    # if current_user and 'roles' in current_user and current_user['roles'] is not None:
    #   is_admin = 'admin' in current_user['roles']

    # # 4. Apply permissions to the UI
    # has_permission = is_owner or is_admin

    # self.check_box_1.enabled = has_permission # Disables clicking
    # self.button_edit.visible = has_permission # Hides edit button
    # self.button_delete.visible = has_permission # Hides delete button

    # # 5. Set initial values
    # self.check_box_1.text = self.item['item_name']
    # self.check_box_1.checked = self.item['completed']

  @handle("check_box_1", "change")
  def check_box_1_change(self, **event_args):
    checked = self.check_box_1.checked
    try:
      anvil.server.call('update_item', self.item, {'completed': checked})
  
      # Instant visual feedback
      if checked:
        self.label_item_name.foreground = "#888"
      else:
        self.label_item_name.foreground = "black"
  
    except Exception as e:
      self.check_box_1.checked = not checked
      alert(str(e))
      
  # @handle("check_box_1", "change")
  # def check_box_1_change(self, **event_args):
  #   # This code only runs now if 'enabled' was True
  #   try:
  #     anvil.server.call('update_item', self.item, {'completed': self.check_box_1.checked})
  #   except Exception as e:
  #     # Fallback: if server rejects it, uncheck the box visually
  #     self.check_box_1.checked = not self.check_box_1.checked
  #     alert(str(e))

  
  # @handle("check_box_1", "change")
  # def check_box_1_change(self, **event_args):
  #   anvil.server.call('update_item', self.item, {'completed': self.check_box_1.checked})
  
  @handle("button_delete", "click")
  def button_delete_click(self, **event_args):
    if confirm(f"Delete {self.item['item_name']}?"):
      anvil.server.call('delete_item', self.item)
      # Tell the very top form to refresh everything
      self.parent.raise_event('x-refresh-all')

  @handle("button_edit", "click")
  def button_edit_click(self, **event_args):
    edit_box = TextBox(text=self.item['item_name'])
    if alert(content=edit_box, title="Edit Item", buttons=[("Save", True), ("Cancel", False)]):
      anvil.server.call('update_item', self.item, {'item_name': edit_box.text})
      self.parent.raise_event('x-refresh-all')