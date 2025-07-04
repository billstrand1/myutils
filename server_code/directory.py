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
def delete_member(member): 
  if app_tables.users.has_row(member):
    member.delete()
  else:
    raise Exception("Member does not exist")


@anvil.server.callable
def get_directory():  
  results = app_tables.users.search(
  tables.order_by("last_name", ascending=True),enabled=True)
  return [r for r in results if not admin.has_role(r, 'no_directory')]

@anvil.server.callable
def get_directory_html():
  results = app_tables.users.search(
    tables.order_by("last_name", ascending=True),
    tables.order_by("first_name", ascending=True),
    enabled=True
  )
  directory = [r for r in results if not admin.has_role(r, 'no_directory')]

  rows = []
  for i, r in enumerate(directory):
    bg = "#f9f9f9" if i % 2 == 0 else "#ffffff"
    rows.append(f"""
      <tr style='background-color:{bg};'>
        <td style='padding:8px; border:1px solid #ccc;'>{r['first_name']} {r['last_name']}</td>
        <td style='padding:8px; border:1px solid #ccc;'>
          <a href='mailto:{r["email"]}' style='color:#0645AD; text-decoration:underline;'>{r["email"] or ''}</a>
        </td>
        <td style='padding:8px; border:1px solid #ccc;'>{r['phone'] or ''}</td>
      </tr>
    """)
    
  html = f"""
    <table style='width:100%; font-family:Segoe UI, Helvetica, Arial, sans-serif; border-collapse:collapse;'>
      <thead>
        <tr style='background-color:#ddd;'>
          <th style='text-align:left; padding:8px; border:1px solid #ccc;'>
            <strong>Name</strong>
          </th>
          <th style='text-align:left; padding:8px; border:1px solid #ccc;'>
            <strong>Email Address</strong>
          </th>
          <th style='text-align:left; padding:8px; border:1px solid #ccc;'>
            <strong>Phone Number</strong>
          </th>
          
        </tr>
      </thead>

      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  """
  # print(html)
  return html



#--------------------EMAIL LISTS------------------------
@anvil.server.callable
def get_email_list():
  all_users = get_directory()
  email_list = []
  for user in all_users:
      email_list.append(user['email'])
  email_df = pd.DataFrame(email_list)
  email_str = email_df.to_string(index=False, header=False)
  return email_str


'''
    <table style='width:100%; font-family:Menlo,monospace; border-collapse:collapse;'>
    <table style='width:100%; font-family:Segoe UI, Helvetica, Arial, sans-serif; border-collapse:collapse;'>



'''