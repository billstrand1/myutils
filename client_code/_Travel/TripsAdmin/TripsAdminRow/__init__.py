from ._anvil_designer import TripsAdminRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..TripEditor import TripEditor

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
    state = trip['state']

    if country and city and state:
      self.lbl_location.text = f"{city}, {state} {country}"
    elif city and state:
      self.lbl_location.text = f"{city}, {state}"
    elif country and state:
      self.lbl_location.text = f"{state} {country}"
    elif country and city:
      self.lbl_location.text = f"{city}, {country}"
    elif country:
      self.lbl_location.text = country
    else:
      self.lbl_location.text = ""

  # Change Date Formatting:
    sd = trip['start_date']
    ed = trip['end_date']
    def trip_days(sd, ed):
      return (ed - sd).days + 1    
      
    def fmt_year(d):
      return d.strftime("'%y")
    
    def fmt_month_day(d):
      return d.strftime("%b %-d")  # macOS/Linux
      # Windows fallback:
      # return d.strftime("%b %d").replace(" 0", " ")
    
    if sd and ed:
      days = trip_days(sd, ed)
      day_label = "day" if days == 1 else "days"
      duration = f" [{days} {day_label}]"
    
      # Single-day trip (compact rule)
      if sd == ed:
        self.lbl_dates.text = (
          f"{fmt_month_day(sd)}, {fmt_year(sd)}{duration}"
        )
    
      elif sd.year == ed.year:
        if sd.month == ed.month:
          # Same month, same year
          self.lbl_dates.text = (
            f"{fmt_month_day(sd)} → {ed.day}, {fmt_year(ed)}{duration}"
          )
        else:
          # Different month, same year
          self.lbl_dates.text = (
            f"{fmt_month_day(sd)} → {fmt_month_day(ed)}, {fmt_year(ed)}{duration}"
          )
      else:
        # Different years
        self.lbl_dates.text = (
          f"{fmt_month_day(sd)}, {fmt_year(sd)} → "
          f"{fmt_month_day(ed)}, {fmt_year(ed)}{duration}"
        )
    
    elif sd:
      self.lbl_dates.text = f"{fmt_month_day(sd)}, {fmt_year(sd)}"
    
    elif ed:
      self.lbl_dates.text = f"{fmt_month_day(ed)}, {fmt_year(ed)}"
    
    else:
      self.lbl_dates.text = ""



  # @handle("btn_edit", "click")
  # def btn_edit_click(self, **event_args):
  #   open_form("_Travel.TripsAdmin.TripEditor", trip_row=self.item, mode='edit')

  @handle("btn_view", "click")
  def btn_view_click(self, **event_args):
    open_form("_Travel.TripsAdmin.TripEditor", trip_row=self.item, mode='view')


