import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

@anvil.server.callable
def get_trips_for_year(year):
  start = datetime.date(year, 1, 1)
  end   = datetime.date(year + 1, 1, 1)

  rows = app_tables.trips.search(
    tables.order_by("start_date", ascending=True),
    start_date=q.between(start, end)
  )

  # Return rows directly (LiveObjects are fine)
  return list(rows)

@anvil.server.callable
def create_trip(data):
  if not data.get("country"):
    raise Exception("Country is required")

  return app_tables.trips.add_row(
    trip_title=data.get("trip_title"),
    trip_description=data.get("trip_description"),
    start_date=data.get("start_date"),
    end_date=data.get("end_date"),
    country=data.get("country").strip(),
    city=(data.get("city") or "").strip(),
    country_code=(data.get("country_code") or "").strip(),
  )


@anvil.server.callable
def update_trip(trip_id, data):
  trip = app_tables.trips.get(id=trip_id)
  if not trip:
    raise Exception("Trip not found")

  if not data.get("country"):
    raise Exception("Country is required")

  trip.update(
    trip_title=data.get("trip_title"),
    trip_description=data.get("trip_description"),
    start_date=data.get("start_date"),
    end_date=data.get("end_date"),
    country=data.get("country").strip(),
    city=(data.get("city") or "").strip(),
    country_code=(data.get("country_code") or "").strip(),
  )




