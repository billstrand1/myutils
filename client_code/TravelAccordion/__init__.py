from ._anvil_designer import TravelAccordionTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime

from anvil.tables import app_tables

class TravelAccordion(TravelAccordionTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("TravelAccordion __init__")

    trips = list(app_tables.trips.search(trip_id="25-06 Porto"))
    print("Trips found:", len(trips))

    self.repeating_panel_trips.items = trips

# class TravelAccordion(TravelAccordionTemplate):
#   def __init__(self, **properties):
#     self.init_components(**properties)
#     print("TravelAccordion __init__")

#   def form_show(self, **event_args):
#     print("TravelAccordion form_show")

#     trips = list(app_tables.trips.search(trip_id="25-06 Porto"))
#     print("Trips found:", len(trips))

#     # VERY visible proof
#     if not trips:
#       self.label_debug.text = "NO TRIPS FOUND"
#     else:
#       self.label_debug.text = f"FOUND {len(trips)} TRIP(S): {trips[0]['trip_id']}"

#     self.repeating_panel_trips.items = trips

