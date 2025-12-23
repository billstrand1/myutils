import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_trips_for_year(year):
  import datetime

  start = datetime.date(year, 1, 1)
  end   = datetime.date(year + 1, 1, 1)

  rows = app_tables.trips.search(
    tables.order_by("start_date", ascending=True),
    start_date=q.between(start, end)
  )

  # Return rows directly (LiveObjects are fine)
  return list(rows)

