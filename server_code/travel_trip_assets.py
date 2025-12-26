import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_assets_for_trip(trip_id):
  return list(
    app_tables.trip_data.search(
      trip=app_tables.trips.get(id=trip_id),
      order_by="sort_order"
    )
  )


