import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_new_contact(contact_dict):
  print('Add User successfully called.')
  app_tables.users.add_row(**contact_dict)
