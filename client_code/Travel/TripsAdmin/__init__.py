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
    self.load_trips()

    def load_trips(self):
      self.rp_trips.items = anvil.server.call("get_all_trips")

    def btn_new_trip_click(self, **e):
      open_form("TripEditor", trip_row=None)
      
