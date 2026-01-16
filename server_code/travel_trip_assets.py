import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


def infer_asset_type(file, web_url, youtube_url):
  if youtube_url:
    return "video"
  if web_url:
    return "link"
  if file:
    name = (file.name or "").lower()
    if name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
      return "image"
    if name.endswith(".pdf"):
      return "pdf"
    return "file"
  return None


@anvil.server.callable
def get_assets_for_trip(trip_row):
  return list(
    app_tables.trip_data.search(tables.order_by("sort_order", ascending=True), trip_link=trip_row,      
    )
  )

# @anvil.server.callable
# def add_asset(trip_row, data):
#   existing = app_tables.trip_data.search(trip_link=trip_row)
#   max_order = max([a['sort_order'] for a in existing], default=0)

#   if data.get("is_thumbnail"):
#     for a in app_tables.trip_data.search(trip_link=trip_row, is_thumbnail=True):
#       a['is_thumbnail'] = False

#   app_tables.trip_data.add_row(
#     trip_link=trip_row,
#     file=data['file'],
#     description=data['description'],
#     notes=data['notes'],
#     asset_type=data['asset_type'],
#     is_thumbnail=data['is_thumbnail'],
#     sort_order=max_order + 1
#   )
@anvil.server.callable
def add_asset(trip_row, data):
  file = data.get("file")
  web_url = data.get("web_url")
  youtube_url = data.get("youtube_url")

  inputs = [bool(file), bool(web_url), bool(youtube_url)]
  if sum(inputs) != 1:
    raise Exception("Exactly one asset input is required (file OR web_url OR youtube_url)")

  asset_type = infer_asset_type(file, web_url, youtube_url)
  
  # inputs = [
  #   bool(data.get("file")),
  #   bool(data.get("web_url")),
  #   bool(data.get("youtube_url")),
  # ]

  # if sum(inputs) != 1:
  #   raise Exception("Exactly one asset input is required")

  
  # asset_type = infer_asset_type(
  #   data.get("file"),
  #   data.get("web_url"),
  #   data.get("youtube_url")
  # )

  if not asset_type:
    raise Exception("Unable to determine asset type")

  if data.get("is_thumbnail"):
    for a in app_tables.trip_data.search(trip_link=trip_row, is_thumbnail=True):
      a['is_thumbnail'] = False

  existing = app_tables.trip_data.search(trip_link=trip_row)
  max_order = max([a['sort_order'] for a in existing], default=0)

  app_tables.trip_data.add_row(
    trip_link=trip_row,
    file=data['file'],
    web_url=data['web_url'],
    youtube_url=data['youtube_url'],
    description=data['description'],
    notes=data['notes'],
    asset_type=asset_type,
    # is_thumbnail=data['is_thumbnail'],
    sort_order=max_order + 1
  )



@anvil.server.callable
def update_asset(asset_row, data):
  #2B.5:
  clear_file = bool(data.get("clear_file"))
  new_file = data.get("file")
  web_url = data.get("web_url")
  youtube_url = data.get("youtube_url")

  effective_file = None
  if clear_file:
    effective_file = None
  elif new_file:
    effective_file = new_file
  else:
    effective_file = asset_row['file']

    # Enforce exactly one input based on effective state
  inputs = [bool(effective_file), bool(web_url), bool(youtube_url)]
  if sum(inputs) != 1:
    raise Exception("Exactly one asset input is required (file OR web_url OR youtube_url)")

    # Enforce single thumbnail per trip
  if data.get("is_thumbnail"):
    for a in app_tables.trip_data.search(trip_link=asset_row['trip_link'], is_thumbnail=True):
      a['is_thumbnail'] = False

    # Infer asset type server-side (using effective inputs)
  asset_type = infer_asset_type(effective_file, web_url, youtube_url)

  asset_row.update(
    file=effective_file,
    web_url=web_url,
    youtube_url=youtube_url,
    description=data.get("description"),
    notes=data.get("notes"),
    asset_type=asset_type,
    # is_thumbnail=bool(data.get("is_thumbnail")),
  )

  #------2B.5----
  # inputs = [
  #   bool(data.get("file")),
  #   bool(data.get("web_url")),
  #   bool(data.get("youtube_url")),
  # ]

  # if sum(inputs) != 1:
  #   raise Exception("Exactly one asset input is required")

  # asset_type = infer_asset_type(
  #   data.get("file") or asset_row['file'],
  #   data.get("web_url"),
  #   data.get("youtube_url")
  # )

  # if data.get("is_thumbnail"):
  #   for a in app_tables.trip_data.search(trip_link=asset_row['trip_link'], is_thumbnail=True):
  #     a['is_thumbnail'] = False

  # asset_row.update(
  #   file=data['file'] or asset_row['file'],
  #   web_url=data['web_url'],
  #   youtube_url=data['youtube_url'],
  #   description=data['description'],
  #   notes=data['notes'],
  #   asset_type=asset_type,
  #   is_thumbnail=data['is_thumbnail']
  # )


@anvil.server.callable
def delete_asset(asset_row):
  # Defensive check
  if not asset_row:
    raise Exception("Asset not found")

  asset_row.delete()
