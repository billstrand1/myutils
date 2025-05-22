import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from . import admin
import pandas as pd

@anvil.server.callable
def add_new_member(contact_dict):
  print('Add User successfully called.\n')
  print(contact_dict)
  app_tables.users.add_row(**contact_dict)

@anvil.server.callable
def update_member(member, member_dict):
  print(f"Receiving {member['first_name']} to update with\n{member_dict}")
  # member_dict['updated'] = datetime.now()
  # member_dict['full_name'] = member_dict['last_name'] + ', ' + member_dict['first_name']
  member.update(**member_dict)


@anvil.server.callable
def get_directory():  
  results = app_tables.users.search(
  tables.order_by("last_name", ascending=True),enabled=True)
  return [r for r in results if not admin.has_role(r, 'no_directory')]

@anvil.server.callable
def get_directory_str():  
  results = app_tables.users.search(
    tables.order_by("last_name", ascending=True),enabled=True)
  directory = [r for r in results if not admin.has_role(r, 'no_directory')]
  
  for member in directory:
    name = f"{member['first_name']} {member{'last_name'}}
  
  #Need to make a 
  directory_df = pd.DataFrame(directory)
  directory_str = directory_df.to_string(index=False, justify='center', col_space=14)
  return directory_str
  
@anvil.server.callable
def delete_member(member): 
  if app_tables.users.has_row(member):
    member.delete()
  else:
    raise Exception("Member does not exist")

@anvil.server.callable
def get_email_list():
  all_users = get_directory()
  email_list = []
  for user in all_users:
      email_list.append(user['email'])
  email_df = pd.DataFrame(email_list)
  email_str = email_df.to_string(index=False, header=False)
  return email_str