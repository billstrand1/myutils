import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def add_comment(comment_dict): #name, email, comments):
  app_tables.comments.add_row(
    comment_info = comment_dict, 
    created=datetime.now()
  )

  # Send yourself an email each time feedback is submitted
  emails = ['billstrand1@gmail.com']
  anvil.email.send(to=emails, # Change this to your email address!
                   subject= "Question from app",
                   text = f"{comment_dict}")