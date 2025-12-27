from ._anvil_designer import TripEditorTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TripEditor(TripEditorTemplate):
  def __init__(self, trip_row=None, **properties):
    self.init_components(**properties)
    self.trip_row = trip_row

    self.trip_details.load_trip(trip_row)
    self.trip_assets_manager.load_trip(trip_row)

  @handle("button_save", "click")
  def button_save_click(self, **event_args):
    trip_data = self.trip_details.collect_data()

    if self.trip_row:
      anvil.server.call("update_trip", self.trip_row['id'], trip_data)
    else:
      self.trip_row = anvil.server.call("create_trip", trip_data)

    self.trip_assets_manager.set_trip(self.trip_row)
    alert("Trip saved")
