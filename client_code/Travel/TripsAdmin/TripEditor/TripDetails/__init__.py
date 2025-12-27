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
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_trip(trip_row)
  
    # Any code you write here will run before the form opens.
  def load_trip(self, trip):
    if not trip:
      return
      
    self.text_trip_id.text = trip['trip_id']
    self.text_desc.text = trip['trip_description']
    self.text_country.text = trip['country']
    self.text_city.text = trip['city']
    self.date_start.date = trip['start_date']
    self.date_end.date = trip['end_date']
    self.text_notes.text = trip['notes']
    self.text_notes.text = trip['notes']    
    self.text_web_url.text = trip['web_url']
    self.text_youtube_url.text = trip['youtube_url']
    