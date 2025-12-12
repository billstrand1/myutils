from ._anvil_designer import TeeTimeTemplateTemplate
from anvil import *
import m3.components as m3
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TeeTimeTemplate(TeeTimeTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
      
    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    if not user:
      user = anvil.users.login_with_form()

    self.admin = False
    if user:
      self.admin = anvil.server.call('has_role', user, 'admin')
      print(f'Admin: {self.admin}')
      
    self.day_switch.selected = False
    print (f"day_switch: {self.day_switch.selected}")
    self.set_date_and_comment_labels()
    self.reset_display()

  def day_switch_change(self, **event_args):
    self.reset_display()

    
  def set_date_and_comment_labels(self):
    date_selected = app_tables.date_of_play.search()
    print(f"Len date_selected = {len(date_selected)}")
    if len(date_selected) > 0:
      for date_info in date_selected:
        self.date_this_friday = date_info['date_friday']
        self.comment_this_friday = date_info['comment_friday']
        self.date_this_saturday = date_info['date_saturday']
        self.comment_this_saturday = date_info['comment_saturday']

        # self.friday_date_label_text = 'For: ' + self.date_this_friday.strftime("%A %b %d, '%y")
        # self.saturday_date_label_text = 'For: ' + date_this_saturday.strftime("%A %b %d, '%y")
        


  def set_button_menus(self, day):
    print (f"day_switch: {self.day_switch.selected}")
    if day == 'Friday':
      self.button_menu.text = 'For: ' + self.date_this_friday.strftime("%A %b %d, '%y")
      # self.friday_comment_box.visible = True
      # self.saturday_comment_box.visible = False
      
      if self.admin:
        #Set Admin button Menus
        self.friday_comment_box.visible = True
        self.friday_comment_label.visible = False
        pass
      else:
        #Set User button Menus
        self.friday_comment_box.visible = False
        self.friday_comment_label.visible = True
        
      
    else:
      print (f"day_switch: {self.day_switch.selected}")
      # Saturday
      self.button_menu.text = 'For: ' + self.date_this_saturday.strftime("%A %b %d, '%y")
      self.saturday_comment_box.visible = True     
      self.friday_comment_box.visible = False

      

    if self.admin:
      self.friday_comment_box.visible = True
      pass
      
    
  # Set up Friday Signup Options.
  #Menu will be two part - Member and Admin
  def reset_display(self, **event_args):
    if not self.day_switch.selected:
      #Display Friday Stuff
      self.set_button_menus('Friday')
      self.friday_comment_box.text = self.comment_this_friday
      self.repeating_panel_tee_times.items = anvil.server.call('get_friday_players')      
    else:
      #Display Saturday Stuff
      self.set_button_menus('Saturday')
      self.repeating_panel_tee_times.items = anvil.server.call('get_saturday_players')

    
    
    # self.directory_panel.clear()
    # self.directory_panel.add_component(DirectoryDisplayHTML())


