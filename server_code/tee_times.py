import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from datetime import date

# @anvil.server.callable
# def get_day_number(date_value):
#   return date_value.isoweekday()

@anvil.server.callable
def get_friday_players():
  print('Calling get friday players')
  
@anvil.server.callable
def get_saturday_players():
  print('Calling get saturday players')

@anvil.server.callable
def add_new_tee_time(tee_time):
  app_tables.tee_times.add_row(**tee_time)
  