import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_friday_players():
  print('Calling get friday players')
  
@anvil.server.callable
def get_saturday_players():
  print('Calling get saturday players')
  