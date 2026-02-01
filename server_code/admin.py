import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_columns_in_user_table():
  columns_in_user_table = app_tables.users.list_columns()
  # Birthday = next((item for item in columns_in_birthday_list if item["name"] == "Birthday"), None)
  # if Birthday: 
  #     print('Birthday found')
  # else: 
  #     print('Birthday not found')
  return columns_in_user_table
  
@anvil.server.callable  
def has_role(user, role):
  if not user: # or 'roles' not in user:
    print('No user found.')
    return False

  try:
    result = role in user['roles']
    print(f"Checking role '{role}' in {user['roles']} → {result}")
    return result
  except Exception as e:
    print(f"Role check failed: {e}")
    return False
  else:
    return False

@anvil.server.callable
def am_i_admin():
  """Checks if the logged-in user is an admin using the has_role function."""
  return has_role(anvil.users.get_user(), 'admin')

  
# @anvil.server.callable
# def is_current_user_admin():
#   user = anvil.users.get_user()
#   # Use your existing logic here safely on the server
#   if user and 'roles' in user and user['roles'] is not None:
#     return 'admin' in user['roles']
#   return False