from ._anvil_designer import TravelAccordionTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime

class TravelAccordion(TravelAccordionTemplate):
  def __init__(self, year=2025, **properties):
    self.init_components(**properties)
    self.year = year

  def form_show(self, **event_args):
    start = datetime.date(self.year, 1, 1)
    end   = datetime.date(self.year + 1, 1, 1)

    print('TravelAccordian about to call trips search')
    trips = list(app_tables.trips.search(
      tables.order_by("start_date", ascending=True),
      start_date=q.between(start, end)
    ))

    self.repeating_panel_trips.items = trips

