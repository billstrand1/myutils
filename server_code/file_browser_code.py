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

@anvil.server.callable
def expand_file_rows(base_rows):
  """
  Take a list of 'base' rows (each may have file, youtube_url, web_url),
  and return a flat list where each item has exactly one of those set.

  base_rows can be:
    - app_tables.files.search(...) results (Row objects), or
    - any objects/dicts with the expected keys.
  """
  expanded = []

  for row in base_rows:
    # You can adapt these field names if yours differ
    description = row['description']
    comments = row['comments']
    file_obj = row.get('file', None) if isinstance(row, dict) else row['file']
    youtube_url = row.get('youtube_url', None) if isinstance(row, dict) else row['youtube_url']
    web_url = row.get('web_url', None) if isinstance(row, dict) else row['web_url']

    # Base fields copied into all expanded items
    base = {
      'description': description,
      'comments': comments,
      'source_row': row,   # original Row; FileRowDT can ignore this
    }

    if file_obj:
      expanded.append({
        **base,
        'file': file_obj,
        'youtube_url': None,
        'web_url': None,
      })

    if youtube_url:
      expanded.append({
        **base,
        'file': None,
        'youtube_url': youtube_url,
        'web_url': None,
      })

    if web_url:
      expanded.append({
        **base,
        'file': None,
        'youtube_url': None,
        'web_url': web_url,
      })

  return expanded
