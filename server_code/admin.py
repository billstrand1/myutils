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

# @anvil.server.callable
# def has_role(user_row, role):
#   roles = user_row['roles']
#   print(f"{user_row['last_name']} roles: {user_row['roles']}, roles2:{roles}")
  
#   if isinstance(roles, list):
#     print('is_instance list True')
#     print(f"Checking role '{role}' in {user_row['roles']} → True")
#     return role in roles
#   elif isinstance(roles, str):
#     roles = roles.strip()
#     if roles == "":
#       return False
#     elif "," in roles:
#       return role in [r.strip() for r in roles.split(",")]
#     else:
#       return role == roles

#   return False
  