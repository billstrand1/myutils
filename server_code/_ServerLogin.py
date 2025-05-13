import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def force_debug_login_shr_utils():
  print('DONT FORGET TO COMMENT OUT FORCED LOGIN')
  anvil.users.force_login(app_tables.users.get(email="joe@test.com"))

  # bill.strand@yahoo.com
  # billstrand1@yahoo.com
  # joe@test.com