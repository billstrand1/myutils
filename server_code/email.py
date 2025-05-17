import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#-------------------EMAIL DT CHANGES--------------------------------
# Email Bill when DT changes are made
@anvil.server.callable
def email_change(message, subject="Change to DT", from_name="Data Table Changes"):
  print('Emailing Bill')
  emails = ['billstrand1@gmail.com']
  anvil.email.send(from_name=from_name,
                   to=emails,
                   from_address="DT",
                   subject=subject,
                   text=message
                  )  