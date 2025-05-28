from ._anvil_designer import SignupHomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .TeeTimeTemplate import TeeTimeTemplate
from .. import Globals
from m3 import components
from .AddTeeTime import AddTeeTime

class SignupHome(SignupHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.signup_panel.add_component(TeeTimeTemplate())
    # Any code you write here will run before the form opens.

# ------------------Comment out before cloning, run from data_functions Server Code
    print('Calling for log-in')
    anvil.server.call('force_debug_login_shr_utils')
    self.user = anvil.users.get_user()
    

  #date, course, tee times
  
  # def validate_tee_time_data(tee_time):
  #   if not tee_time['date']:
  #     return "Please enter date."
  #   if not tee_time['course']:
  #     return "Please select a course."
  #   if not tee_time['tee_times']:
  #     return "Please select a course."
      
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
  
  def button_add_click(self, **event_args):
    print('Add Tee Time clicked')
    user = anvil.users.get_user()
    if not user:
      user = anvil.users.login_with_form()

    
    # print(f" {user['first_name']} {.user['last_name']} is adding a new Tee Time")
      
    

    new_tee_time = {'date': None,
                   'course': '',
                   'tee_time': '',
                   'comments': '',
                    'day_number': None
                   }

    tee_time_add_form = AddTeeTime(item=new_tee_time)

    while True: # Keep looping until valid input is provided
      save_clicked = alert(
        content=tee_time_add_form,
        title="Add Tee Time",
        large=True,
        buttons=[("Save", True), ("Cancel", False)],
      )

      if not save_clicked:
        return  # or break

      #Need to add validation code here:

      

      new_tee_time['owner'] = user
      
      day_number = Globals.get_day_number(new_tee_time['date'])
      new_tee_time['day_number'] = day_number
      
      anvil.server.call('add_new_tee_time', new_tee_time)
      print(f"New Tee Time: {new_tee_time}")
      break
      

      


    
      
    

