from ._anvil_designer import TripsAdminTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TripsAdmin(TripsAdminTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Load trips into the repeating panel
    self.load_trips()

  def load_trips(self):
    """
    Fetch trips from the server and bind them to the repeating panel.
    """
    trips = anvil.server.call("get_all_trips_admin")
    # alert(f"Loaded {len(trips)} trips")
    self.rp_trips.items = trips
    # trips = anvil.server.call("get_all_trips_admin")
    # self.rp_trips.items = trips


  @handle("btn_new_trip", "click")
  def btn_new_trip_click(self, **e):
      """
      Open TripEditor in 'new trip' mode.
      """
      print('New trip button clicked')
      open_form("TripEditor", trip_row=None)

