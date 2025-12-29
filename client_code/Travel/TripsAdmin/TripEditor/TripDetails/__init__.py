from ._anvil_designer import TripDetailsTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TripDetails(TripDetailsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def load_trip(self, trip):
    if trip is None:
      return
      
    self.txt_trip_id.text = trip['trip_id']
    self.txt_description.text = trip['trip_description']
    self.txt_country.text = trip['country']
    self.txt_city.text = trip['city']
    self.dp_start.date = trip['start_date']
    self.dp_end.date = trip['end_date']
    self.txt_notes.text = trip['notes']

  def collect_data(self):
    if not self.txt_country.text:
      raise Exception("Country is required")

    return {
      "trip_id": self.txt_trip_id.text,
      "trip_description": self.txt_description.text,
      "country": self.txt_country.text,
      "city": self.txt_city.text,
      "start_date": self.dp_start.date,
      "end_date": self.dp_end.date,
      "notes": self.txt_notes.text,
    }
