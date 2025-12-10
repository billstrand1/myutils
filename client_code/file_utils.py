import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



def expand_file_rows(base_rows, copy_fields=None, map_fields=None):
  """
  Expand 'base' file rows (file, youtube_url, web_url, notes) into multiple rows.

  - If a row has 'notes', a NOTES row is created FIRST.
  - Then, one row each for file / youtube / web (if present).

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
      - 'notes'
      - 'file'         (only one of file/youtube/web is non-None)
      - 'youtube_url'
      - 'web_url'
      - 'source_row'   (the original underlying row)
      - any extra fields listed in copy_fields
  """


  if copy_fields is None:
    copy_fields = []
  if map_fields is None:
    map_fields = {}

  expanded = []

  for row in base_rows:
    def get_val(field_name):
      try:
        return row[field_name]
      except Exception:
        if isinstance(row, dict):
          return row.get(field_name)
        return None

    # Build the base payload
    # Base payload
    base = {
      "title": get_val("title"),
      "comments": get_val("comments"),
      "notes": get_val("notes"),   # 👈 NEW: pull trip notes
      "file": None,
      "youtube_url": None,
      "web_url": None,
      "source_row": row,
    }
    # Apply field mappings (trip_description → description, etc.)
    for src, dest in map_fields.items():
      base[dest] = get_val(src)

    # If no mapping provided, try native 'description'
    if base.get("description") is None:
      base["description"] = get_val("description")

    # Copy any extra passthrough fields
    for field_name in copy_fields:
      base[field_name] = get_val(field_name)

    # Collect content fields
    file_obj = get_val("file")
    youtube_url = get_val("youtube_url")
    web_url = get_val("web_url")

    # --- 1) NOTES ROW (highest priority) ----------------------------
    if base.get("notes"):
      item = dict(base)
      # Ensure it's a pure "notes" item; no media here
      item["file"] = None
      item["youtube_url"] = None
      item["web_url"] = None
      expanded.append(item)
      
    # Expand into 1–3 rows as needed
    if file_obj:
      item = dict(base)
      item["file"] = file_obj
      expanded.append(item)

    if youtube_url:
      item = dict(base)
      item["youtube_url"] = youtube_url
      expanded.append(item)

    if web_url:
      item = dict(base)
      item["web_url"] = web_url
      expanded.append(item)

  return expanded
