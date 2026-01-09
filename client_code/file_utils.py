import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


def expand_file_rows(base_rows, copy_fields=None, map_fields=None, include_empty=False):
  """
  Expand base rows into multiple rows suitable for FileBrowserDT / FileViewerDT.

  Guarantees each expanded row contains exactly ONE media type:
    - file OR youtube_url OR web_url
  Notes-only rows contain none of those three.

  map_fields can map Trips columns to viewer columns, including:
    itinerary -> file
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

    # Start with the viewer schema keys
    base = {
      "title": get_val("title", ""),
      "comments": get_val("comments", ""),
      "notes": get_val("notes", ""),
      "file": get_val("file", None),
      "youtube_url": get_val("youtube_url", None),
      "web_url": get_val("web_url", None),
      "source_row": row,
    }

    # Apply mappings (Trips -> Viewer schema)
    for src, dest in map_fields.items():
      base[dest] = get_val(src)

    # Copy passthrough fields (e.g., trip_id)
    for field_name in copy_fields:
      base[field_name] = get_val(field_name)

    # Pull values from the mapped base
    file_obj = base.get("file")
    youtube_url = base.get("youtube_url")
    web_url = base.get("web_url")
    notes_text = (base.get("notes") or "").strip()

    made_any = False

    # ---------- 1) NOTES-ONLY ROW ----------
    if notes_text:
      notes_item = dict(base)
      notes_item["file"] = None
      notes_item["youtube_url"] = None
      notes_item["web_url"] = None
      expanded.append(notes_item)
      made_any = True

    # For subsequent media rows: do not carry notes forward
    base_media = dict(base)
    base_media["notes"] = ""

    # Helper to make a “pure” item (only one field set)
    def make_item(kind):
      item = dict(base_media)
      item["file"] = None
      item["youtube_url"] = None
      item["web_url"] = None
      if kind == "file":
        item["file"] = file_obj
      elif kind == "youtube":
        item["youtube_url"] = youtube_url
      elif kind == "web":
        item["web_url"] = web_url
      return item

    # ---------- 2) FILE / YOUTUBE / WEB ROWS (pure) ----------
    if file_obj:
      expanded.append(make_item("file"))
      made_any = True

    if youtube_url:
      expanded.append(make_item("youtube"))
      made_any = True

    if web_url:
      expanded.append(make_item("web"))
      made_any = True

    # ---------- 3) PLACEHOLDER (optional) ----------
    if include_empty and not made_any:
      placeholder = dict(base_media)
      placeholder["file"] = None
      placeholder["youtube_url"] = None
      placeholder["web_url"] = None
      expanded.append(placeholder)

  return expanded
