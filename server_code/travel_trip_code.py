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
  clear_itin = data.pop("_clear_itinerary", False)
  if clear_itin:
    data["itinerary"] = None
    trip_row.update(**data)
