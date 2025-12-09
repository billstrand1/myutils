import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# def expand_file_rows(base_rows):
#   """
#   Take a list of 'base' rows (each may have file, youtube_url, web_url),
#   and return a flat list where each item has exactly one of those set.

#   base_rows can be:
#     - app_tables.files.search(...) results (Row objects), or
#     - any objects/dicts with the expected keys.
#   """
#   expanded = []

#   for row in base_rows:
#     # You can adapt these field names if yours differ
#     description = row['description']
#     comments = row['comments']
#     file_obj = row.get('file', None) if isinstance(row, dict) else row['file']
#     youtube_url = row.get('youtube_url', None) if isinstance(row, dict) else row['youtube_url']
#     web_url = row.get('web_url', None) if isinstance(row, dict) else row['web_url']

#     # Base fields copied into all expanded items
#     base = {
#       'description': description,
#       'comments': comments,
#       'source_row': row,   # original Row; FileRowDT can ignore this
#     }

#     if file_obj:
#       expanded.append({
#         **base,
#         'file': file_obj,
#         'youtube_url': None,
#         'web_url': None,
#       })

#     if youtube_url:
#       expanded.append({
#         **base,
#         'file': None,
#         'youtube_url': youtube_url,
#         'web_url': None,
#       })

#     if web_url:
#       expanded.append({
#         **base,
#         'file': None,
#         'youtube_url': None,
#         'web_url': web_url,
#       })

#   return expanded

# MyUtils / Client Module: utils.py

def expand_file_rows(base_rows, copy_fields=None, map_fields=None):
  """
  Expand 'base' file rows (which may contain file, youtube_url, web_url)
  into a flat list where each item has exactly ONE of those fields set.

  This is designed to feed FileBrowserDT / FileRowDT.

NEW:   Args:
    base_rows: Iterable of Anvil rows or dicts.
    copy_fields: Extra field names to copy unchanged into each expanded row.
    map_fields: Dict mapping { 'source_field': 'target_field' }
                Example: { 'trip_description': 'description' }
                
  Args:
    base_rows: An iterable of rows, e.g. app_tables.files.search(...)
               Each row may have:
                 - 'description'
                 - 'comments'
                 - 'file'
                 - 'youtube_url'
                 - 'web_url'
               plus any optional extra fields.
    copy_fields: Optional list of extra field names to copy from the base
                 row into each expanded row (e.g. ['trip_id', 'sort_order']).

  Returns:
    A list of dicts. Each dict has:
      - 'description'
      - 'comments'
      - 'file'         (only one of these 3 is non-None)
      - 'youtube_url'
      - 'web_url'
      - 'source_row'   (the original underlying row)
      - any extra fields listed in copy_fields
  """
  if copy_fields is None:
    copy_fields = []

  expanded = []

  for row in base_rows:
    # Helper to read either an Anvil row or a plain dict safely
    def get_val(field_name):
      # Row object (Anvil)
      try:
        return row[field_name]
      except (KeyError, TypeError):
        # Maybe it's a dict, or the key is missing
        if isinstance(row, dict):
          return row.get(field_name)
        return None

    description = get_val('description')
    comments = get_val('comments')
    file_obj = get_val('file')
    youtube_url = get_val('youtube_url')
    web_url = get_val('web_url')

    # Base payload shared by all expanded items for this row
    base = {
      'description': description,
      'comments': comments,
      'file': None,
      'youtube_url': None,
      'web_url': None,
      'source_row': row,   # keep original DB row handy
    }

    # Copy any extra fields requested (e.g. trip_id, sort_order)
    for field_name in copy_fields:
      base[field_name] = get_val(field_name)

    # Now expand into 1–3 rows depending on what this item actually has
    if file_obj:
      item = dict(base)
      item['file'] = file_obj
      expanded.append(item)

    if youtube_url:
      item = dict(base)
      item['youtube_url'] = youtube_url
      expanded.append(item)

    if web_url:
      item = dict(base)
      item['web_url'] = web_url
      expanded.append(item)

  return expanded
