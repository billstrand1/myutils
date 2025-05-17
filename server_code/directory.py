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


@anvil.server.callable
def get_directory():  #gets all users except super_user
  #Need to add a "no_directory" role for the search.
  return app_tables.users.search(
  tables.order_by("last_name", ascending=True),enabled=True)

@anvil.server.callable
def delete_member(member): 
  if app_tables.users.has_row(member):
    member.delete()
  else:
    raise Exception("Member does not exist")
