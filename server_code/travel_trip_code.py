import anvil.email
import anvil.users
import anvil.tables as tables
from anvil.tables import order_by
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime


@anvil.server.callable
def get_all_trips_admin():
  print('getting all trips admin')
  # return list(app_tables.trips.search(order_by="start_date"))
  # tables.order_by("name", ascending=False)
  return list(app_tables.trips.search(tables.order_by("start_date", ascending=False)))
  # return list(get_trips_for_year(2025))

@anvil.server.callable
def get_all_trips_admin_search(search_query=None):
  # 1. Get the base search (optionally restricted by user/permissions)
  # Replace 'trips' with your actual table name if different
  all_trips = app_tables.trips.search(tables.order_by("start_date", ascending=False))

  if not search_query:
    return all_trips

  # 2. If there is a query, filter using 'any_of' and 'ilike'
  # The % signs allow for partial matches (e.g. "Paris" matches "Paris, France")
  term = f"%{search_query}%"

  filtered_trips = app_tables.trips.search(
    tables.order_by("start_date", ascending=False),
    q.any_of(
      trip_id=q.ilike(term),
      trip_description=q.ilike(term),
      city=q.ilike(term),
      country=q.ilike(term),
      state=q.ilike(term)
    )
  )

  return filtered_trips
  
@anvil.server.callable
def get_trips_for_year(year):
  print(f'getting trips for year {year}')
  start = datetime.date(year, 1, 1)
  end   = datetime.date(year + 1, 1, 1)

  rows = app_tables.trips.search(
    tables.order_by("start_date", ascending=False),
    start_date=q.between(start, end)
  )
  
  return list(rows)

@anvil.server.callable
def create_trip(data):
  if not data.get("country"):
    raise Exception("Country is required")

  print(f"data to add to trips row:\n{data}")
  return app_tables.trips.add_row(**data)
  

@anvil.server.callable
def update_trip(trip_row, data):
  # trip_row.update(**data)
  #From 2A.3:
  # clear_itin = data.pop("_clear_itinerary", False)
  # if clear_itin:
  #   data["itinerary"] = None
  #   trip_row.update(**data)

  #Step 2 of fix:
  ## Defensive: ensure Media overwrite is respected
  trip_row.update(
    trip_id=data.get("trip_id"),
    trip_description=data.get("trip_description"),
    country=data.get("country"),
    city=data.get("city"),
    state=data.get("state"),
    start_date=data.get("start_date"),
    end_date=data.get("end_date"),
    notes=data.get("notes"),
    tripit_edit=data.get("tripit_edit"),
    tripit_read=data.get("tripit_read"),
    miles=data.get("miles"),
    web_url=data.get("web_url"),
    youtube_url=data.get("youtube_url"),
    itinerary=data.get("itinerary"),  # ← THIS IS THE IMPORTANT LINE
    thumbnail=data.get("thumbnail"),   # NEW
  )
