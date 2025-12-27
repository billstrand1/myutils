from ._anvil_designer import TripsAdminRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..TripEditor import TripEditor

class TripsAdminRow(TripsAdminRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_row()

  def refresh_row(self):
    trip = self.item
    if trip is None:
      return

    # Description / title
    trip_id = trip['trip_id']
    self.lbl_id.text = trip_id
    desc = trip['trip_description']
    self.lbl_desc.text = desc if desc else "(no description)"

    # Location
    country = trip['country']
    city = trip['city']

    if country and city:
      self.lbl_location.text = f"{city}, {country}"
    elif country:
      self.lbl_location.text = country
    elif city:
      self.lbl_location.text = city
    else:
      self.lbl_location.text = ""

    # Dates
    sd = trip['start_date']
    ed = trip['end_date']

    if sd and ed:
      self.lbl_dates.text = f"{sd:%Y-%m-%d} → {ed:%Y-%m-%d}"
    elif sd:
      self.lbl_dates.text = f"Start: {sd:%Y-%m-%d}"
    elif ed:
      self.lbl_dates.text = f"End: {ed:%Y-%m-%d}"
    else:
      self.lbl_dates.text = ""

  @handle("btn_edit", "click")
  def btn_edit_click(self, **event_args):
    # open_form("TripEditor", trip_row=self.item)

    open_form("Travel.TripsAdmin.TripEditor", trip_row=self.item)



