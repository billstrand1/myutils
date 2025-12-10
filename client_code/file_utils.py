import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


def expand_file_rows(base_rows, copy_fields=None, map_fields=None):
  """
  Expand base rows (which may contain file, youtube_url, web_url, notes) into
  multiple rows suitable for FileBrowserDT / FileViewerDT.

  Output rows have:
    - 'title'
    - 'comments'
    - 'notes'
    - 'file'
    - 'youtube_url'
    - 'web_url'
    - 'source_row'
    + any extra fields from copy_fields

  For rows with 'notes':
    - A FIRST item is created that is **notes-only** (no file/youtube/web).
    - Subsequent media items for that row have notes cleared (notes="").
  """
  if copy_fields is None:
    copy_fields = []
  if map_fields is None:
    map_fields = {}

  expanded = []

  for row in base_rows:
    def get_val(field_name, default=None):
      try:
        return row[field_name]
      except Exception:
        if isinstance(row, dict):
          return row.get(field_name, default)
        return default

    # Base payload with possible notes
    base = {
      "title": None,
      "comments": get_val("comments", ""),
      "notes": get_val("notes", ""),
      "file": None,
      "youtube_url": None,
      "web_url": None,
      "source_row": row,
    }

    # Apply mapping from Trips fields → viewer fields (title/comments/notes)
    for src, dest in map_fields.items():
      base[dest] = get_val(src)

    # If title/comments were not supplied via mapping, fall back to native fields
    if base["title"] is None:
      base["title"] = get_val("title", "")
    if not base["comments"]:
      base["comments"] = get_val("comments", "")

    # Copy any extra passthrough fields
    for field_name in copy_fields:
      base[field_name] = get_val(field_name)

    # Media / URLs from the base row
    file_obj = get_val("file", None)
    youtube_url = get_val("youtube_url", None)
    web_url = get_val("web_url", None)

    # ---------- 1) NOTES-ONLY ROW (if notes exist) ----------
    base_notes = dict(base)
    has_notes = bool((base_notes.get("notes") or "").strip())
    if has_notes:
      # Notes-only item: no media/urls
      base_notes["file"] = None
      base_notes["youtube_url"] = None
      base_notes["web_url"] = None
      expanded.append(base_notes)

      # For media items, we do NOT carry notes forward
      base_no_notes = dict(base)
      base_no_notes["notes"] = ""
    else:
      base_no_notes = base

    # ---------- 2) FILE / YOUTUBE / WEB rows (no notes) ----------
    if file_obj:
      item = dict(base_no_notes)
      item["file"] = file_obj
      expanded.append(item)

    if youtube_url:
      item = dict(base_no_notes)
      item["youtube_url"] = youtube_url
      expanded.append(item)

    if web_url:
      item = dict(base_no_notes)
      item["web_url"] = web_url
      expanded.append(item)

  return expanded



# def expand_file_rows(base_rows, copy_fields=None, map_fields=None):
#   """
#   Expand base rows (which may contain file, youtube_url, web_url) into
#   multiple rows suitable for FileBrowserDT / FileViewerDT.

#   Output rows have:
#     - 'title'
#     - 'comments'
#     - 'notes'
#     - 'file'
#     - 'youtube_url'
#     - 'web_url'
#     - 'source_row'
#     + any extra fields from copy_fields

#   map_fields example for Trips:
#     {
#       'trip_id': 'title',
#       'trip_description': 'comments',
#       'notes': 'notes'
#     }
#   """
#   if copy_fields is None:
#     copy_fields = []
#   if map_fields is None:
#     map_fields = {}

#   expanded = []

#   for row in base_rows:
#     def get_val(field_name, default=None):
#       try:
#         return row[field_name]
#       except Exception:
#         if isinstance(row, dict):
#           return row.get(field_name, default)
#         return default

#     # Base payload
#     base = {
#       "title": None,
#       "comments": get_val("comments", ""),
#       "notes": get_val("notes", ""),
#       "file": None,
#       "youtube_url": None,
#       "web_url": None,
#       "source_row": row,
#     }

#     # Apply mapping from source fields → target fields (title/comments/notes)
#     for src, dest in map_fields.items():
#       base[dest] = get_val(src)

#     # If title/comments were not supplied via mapping, fall back to native fields
#     if base["title"] is None:
#       base["title"] = get_val("title", "")
#     if not base["comments"]:
#       base["comments"] = get_val("comments", "")

#     # Copy any extra passthrough fields
#     for field_name in copy_fields:
#       base[field_name] = get_val(field_name)

#     # Media / URLs
#     file_obj = get_val("file", None)
#     youtube_url = get_val("youtube_url", None)
#     web_url = get_val("web_url", None)

#     # 1) NOTES ROW? (only if you still want a separate notes-only item)
#     # If you prefer notes always in header only and not as an item, comment this block out.
#     if base["notes"]:
#       item = dict(base)
#       expanded.append(item)

#     # 2) FILE / YOUTUBE / WEB rows
#     if file_obj:
#       item = dict(base)
#       item["file"] = file_obj
#       expanded.append(item)

#     if youtube_url:
#       item = dict(base)
#       item["youtube_url"] = youtube_url
#       expanded.append(item)

#     if web_url:
#       item = dict(base)
#       item["web_url"] = web_url
#       expanded.append(item)

#   return expanded


# def expand_file_rows(base_rows, copy_fields=None, map_fields=None):
#   """
#   Expand 'base' file rows (file, youtube_url, web_url, notes) into multiple rows.

#   - If a row has 'notes', a NOTES row is created FIRST.
#   - Then, one row each for file / youtube / web (if present).

#   This is designed to feed FileBrowserDT / FileRowDT.

# NEW:   Args:
#     base_rows: Iterable of Anvil rows or dicts.
#     copy_fields: Extra field names to copy unchanged into each expanded row.
#     map_fields: Dict mapping { 'source_field': 'target_field' }
#                 Example: { 'trip_description': 'description' }
                
#   Args:
#     base_rows: An iterable of rows, e.g. app_tables.files.search(...)
#                Each row may have:
#                  - 'description'
#                  - 'comments'
#                  - 'file'
#                  - 'youtube_url'
#                  - 'web_url'
#                plus any optional extra fields.
#     copy_fields: Optional list of extra field names to copy from the base
#                  row into each expanded row (e.g. ['trip_id', 'sort_order']).

#  Returns:
#     A list of dicts. Each dict has:
#       - 'description'
#       - 'comments'
#       - 'notes'
#       - 'file'         (only one of file/youtube/web is non-None)
#       - 'youtube_url'
#       - 'web_url'
#       - 'source_row'   (the original underlying row)
#       - any extra fields listed in copy_fields
#   """


#   if copy_fields is None:
#     copy_fields = []
#   if map_fields is None:
#     map_fields = {}

#   expanded = []

#   for row in base_rows:
#     def get_val(field_name):
#       try:
#         return row[field_name]
#       except Exception:
#         if isinstance(row, dict):
#           return row.get(field_name)
#         return None

#     # Build the base payload
#     # Base payload
#     base = {
#       "title": get_val("title"),
#       "comments": get_val("comments"),
#       "notes": get_val("notes"),   # 👈 NEW: pull trip notes
#       "file": None,
#       "youtube_url": None,
#       "web_url": None,
#       "source_row": row,
#     }
#     # Apply field mappings (trip_description → description, etc.)
#     for src, dest in map_fields.items():
#       base[dest] = get_val(src)

#     # If no mapping provided, try native 'description'
#     if base.get("description") is None:
#       base["description"] = get_val("description")

#     # Copy any extra passthrough fields
#     for field_name in copy_fields:
#       base[field_name] = get_val(field_name)

#     # Collect content fields
#     file_obj = get_val("file")
#     youtube_url = get_val("youtube_url")
#     web_url = get_val("web_url")

#     # --- 1) NOTES ROW (highest priority) ----------------------------
#     if base.get("notes"):
#       item = dict(base)
#       # Ensure it's a pure "notes" item; no media here
#       item["file"] = None
#       item["youtube_url"] = None
#       item["web_url"] = None
#       expanded.append(item)
      
#     # Expand into 1–3 rows as needed
#     if file_obj:
#       item = dict(base)
#       item["file"] = file_obj
#       expanded.append(item)

#     if youtube_url:
#       item = dict(base)
#       item["youtube_url"] = youtube_url
#       expanded.append(item)

#     if web_url:
#       item = dict(base)
#       item["web_url"] = web_url
#       expanded.append(item)

#   return expanded
