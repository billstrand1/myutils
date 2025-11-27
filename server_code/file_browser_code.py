import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_text_from_media(media):
  print('get_text_from_media(media) called')
  data = media.get_bytes()                 # Media object from Data Table
  text = data.decode("utf-8", errors="replace")

  max_chars = 20000
  if len(text) > max_chars:
    text = text[:max_chars] + "\n\n...[truncated]..."

  return text