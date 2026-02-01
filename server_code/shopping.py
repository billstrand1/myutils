import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime


@anvil.server.callable
def add_shopping_item(item_name, quantity=None):
  user = anvil.users.get_user()
  if not user:
    raise Exception("Login required")

    # Add row using the logged-in user's info
  app_tables.shopping_list.add_row(
    user=user,
    first_name=user['first_name'], 
    item_name=item_name,
    quantity=quantity,
    completed=False,
    created=datetime.now(),
    updated=datetime.now()
  )

@anvil.server.callable
def get_grouped_items():
  """Returns a list of dictionaries grouped by user name."""
  all_items = app_tables.shopping_list.search()

  # Group items by first_name in Python
  groups = {}
  for row in all_items:
    name = row['first_name'] or "Unknown"
    if name not in groups:
      groups[name] = []
    groups[name].append(row)

    # Format for the RepeatingPanel: [{'name': 'Susan', 'items': [...]}, ...]
  return [{'name': name, 'items': items} for name, items in groups.items()]

# @anvil.server.callable
# def update_item(item_row, updates):
#   user = anvil.users.get_user()
#   # Security check: only the owner can update
#   if item_row['user'] == user:
#     updates['updated'] = datetime.now()
#     item_row.update(**updates)
#   else:
#     raise Exception("Permission denied: You do not own this item.")

@anvil.server.callable
def update_item(item_row, updates):
  user = anvil.users.get_user()
  # Permission: Owner OR Admin
  if item_row['user'] == user or has_role(user, 'admin'):
    updates['updated'] = datetime.now()
    item_row.update(**updates)
  else:
    raise Exception("Permission denied: You do not own this item.")
    
# @anvil.server.callable
# def delete_item(item_row):
#   user = anvil.users.get_user()
#   # Security check: only the owner can delete
#   if item_row['user'] == user:
#     item_row.delete()
#   else:
#     raise Exception("Permission denied: You do not own this item.")

@anvil.server.callable
def delete_item(item_row):
  user = anvil.users.get_user()
# Permission: Owner OR Admin
  if item_row['user'] == user or has_role(user, 'admin'):
    item_row.delete()
  else:
    raise Exception("Permission denied: You do not own this item.")