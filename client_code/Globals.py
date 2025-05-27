import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

# day_selected = 'False' #Friday


def validate_member_data(member):
  if not member['first_name']:
    return "Please enter first name."
  if not member['last_name']:
    return "Please enter last name."
  if not member['email'] or not anvil.server.call('is_valid_email', member['email']):
    return "Please enter a valid email address."
  if member.get('phone') and not anvil.server.call('is_valid_phone', member['phone']):
    return "Please enter a valid 10 digit phone number."
  if (member.get('birth_month') and not (1 <= member['birth_month'] <= 12)) or \
  (member.get('birth_day') and not (1 <= member['birth_day'] <= 31)):
    return "Birth date must be valid."
  if bool(member.get('birth_month')) ^ bool(member.get('birth_day')):
    return "Please enter both birth month & day, or neither."
  return None


'''
from time import sleep
    sleep(2.5)


'''