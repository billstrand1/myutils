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

    self.drop_down_year.items = [(str(y), y) for y in range(current_year, current_year - 30, -1)]
    
    # Force a valid default year
    selected_year = year or current_year
    self.drop_down_year.selected_value = selected_year

    # Load trips for selected year
    self._load_year(selected_year)
    

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

  @handle("drop_down_year", "change")
  def drop_down_year_change(self, **event_args):
    year = self.drop_down_year.selected_value
    if year:
      self._load_year(year)

  
  def _load_year(self, year):
    # Clear UI
    self.repeating_panel_trips.items = []
    self.text_box_search.text = ""
  
    # Optional: show loading message
    if hasattr(self, "label_status"):
      self.label_status.text = f"Loading {year} trips…"
  
    trips = anvil.server.call("get_trips_for_year", year)
    # trips = app_tables.trips.get(trip_id='25-06 Porto')
    
    self._all_trips = trips
    self.repeating_panel_trips.items = trips
  
    if hasattr(self, "label_status"):
      self.label_status.text = ""

