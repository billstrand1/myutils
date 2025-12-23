from ._anvil_designer import _TravelAccordionTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class _TravelAccordion(_TravelAccordionTemplate):
  def __init__(self, year=None, **properties):
    self.init_components(**properties)
    # print("TravelAccordion __init__")
    # self.label_status.text = "Loading trips…"
    current_year = datetime.date.today().year
    
    # Build year list (adjust range as desired)
    years = list(range(current_year, current_year - 10, -1))
    
    trips = anvil.server.call("get_trips_for_year", year)
  
    self._all_trips = trips
    self.repeating_panel_trips.items = trips
  
    self.label_status.text = ""


    # start_2023 = datetime.date(2023, 1, 1)
    # end_2023   = datetime.date(2024, 1, 1)   # exclusive upper bound

    # start_2024 = datetime.date(2024, 1, 1)
    # end_2024   = datetime.date(2025, 1, 1)   # exclusive upper bound

    # trips = app_tables.trips.search(
    #   tables.order_by("start_date", ascending=True),
    #   start_date = q.between(start_2024, end_2024)
    # )
    print("Trips found:", len(trips))    

    # trips = list(app_tables.trips.search())
    # print("Trips found:", len(trips))
    
    self._all_trips = list(trips)
    self.repeating_panel_trips.items = self._all_trips    
    self.repeating_panel_trips.items = trips

  def text_box_search_change(self, **event_args):
    term = (self.text_box_search.text or "").strip().lower()

    if not term:
      self.repeating_panel_trips.items = self._all_trips
      return
  
    def matches(trip):
      return (
        term in (trip['trip_id'] or "").lower() or
        term in (trip['trip_description'] or "").lower()
      )
  
    filtered = [t for t in self._all_trips if matches(t)]
    self.repeating_panel_trips.items = filtered

  #---------Trying Expand All / Collapse All---------
  @handle("link_expand_all", "click")
  def link_expand_all_click(self, **event_args):
    print('ExpandAll clicked')
    for row in self.repeating_panel_trips.get_components():
      if hasattr(row, "expand"):
        row.expand()

  @handle("link_collapse_all", "click")
  def link_collapse_all_click(self, **event_args):
    print('CollapseAll clicked')
    for row in self.repeating_panel_trips.get_components():
      if hasattr(row, "collapse"):
        row.collapse()

  @handle("text_box_search", "pressed_enter")
  def text_box_search_pressed_enter(self, **event_args):
    self.text_box_search_change()
