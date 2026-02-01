from ._anvil_designer import _ShoppingTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from .GroupTemplate import GroupTemplate

class _Shopping(_ShoppingTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # ------------------Comment out before cloning, run from data_functions Server Code
    # print('Calling for log-in')
    # anvil.server.call('force_debug_login_shr_utils')   

    user = anvil.users.get_user()
    if not user:
      user = anvil.users.login_with_form()
    print(f"{user['last_name']} is logged in") 
    
    # Check admin status ONCE on startup
    # anvil.users.login_with_form()
    # self.is_admin = anvil.server.call('am_i_admin')
    
    Globals.check_permissions()
    self.refresh_list()

    # Get grouped items from server
    items = anvil.server.call('get_grouped_items')

    # Pass the admin status to the RepeatingPanel
    # This allows the GroupTemplate to know if the user is an admin
    self.repeating_panel_main.items = items
    
    # Listen for refresh requests from the nested templates
    self.repeating_panel_main.set_event_handler('x-refresh-all', self.refresh_list)
    self.refresh_list()

  def refresh_list(self, **event_args):
    self.repeating_panel_main.items = anvil.server.call('get_grouped_items')
  
  @handle("button_add", "click")
  def button_add_click(self, **event_args):
    name = self.text_box_new_item.text
    if name:
      anvil.server.call('add_shopping_item', name)
      self.text_box_new_item.text = ""
      self.refresh_list()

  @handle("text_box_new_item", "pressed_enter")
  def text_box_new_item_pressed_enter(self, **event_args):
    self.button_add_click()
