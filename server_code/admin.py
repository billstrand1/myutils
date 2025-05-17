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
def has_role(role):
  user = anvil.users.get_user()
  return user and 'roles' in user and role in user['roles']
  