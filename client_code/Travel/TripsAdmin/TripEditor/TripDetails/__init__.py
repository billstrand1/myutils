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
    self.trip_row = None
    
  def load_trip(self, trip):
    self.trip_row = trip
    if trip is None:
      return
      
    self.txt_trip_id.text = trip['trip_id']
    self.txt_description.text = trip['trip_description']
    self.txt_country.text = trip['country']
    self.txt_city.text = trip['city']
    self.dp_start.date = trip['start_date']
    self.dp_end.date = trip['end_date']
    self.txt_notes.text = trip['notes']
    self.txt_state.text = trip['state']

    self.txt_tripit_edit.text = trip['tripit_edit']
    self.txt_tripit_read.text = trip['tripit_read']
    self.checkbox_miles.checked = trip['miles']
    self.txt_web_url.text = trip['web_url']
    self.txt_youtube_url.text = trip['youtube_url']

  def collect_data(self):
    if not self.txt_country.text:
      alert('Country is required')
      raise Exception("Country is required")

    return {
      "trip_id": self.txt_trip_id.text,
      "trip_description": self.txt_description.text,
      "country": self.txt_country.text,
      "city": self.txt_city.text,
      "state": self.txt_state.text,
      "start_date": self.dp_start.date,
      "end_date": self.dp_end.date,
      "notes": self.txt_notes.text,

      "tripit_edit": self.txt_tripit_edit.text,
      "tripit_read": self.txt_tripit_read.text,
      "miles": self.checkbox_miles.checked,
      "web_url": self.txt_web_url.text,
      "youtube_url": self.txt_youtube_url.text,

      # itinerary file (keep existing if not replaced)
      "itinerary": (
        self.file_itinerary.file
        if self.file_itinerary.file is not None
        else (self.trip_row['itinerary'] if self.trip_row else None)
      ),
    }