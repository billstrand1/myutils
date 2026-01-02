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

    # self.link_download.icon = "fa:external-link"
    # self.link_download.tooltip = "Open in New Tab"
    # self.link_download.visible = True

    
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

    self._update_itinerary_status()

    self.btn_open_web_url.visible = bool(trip['web_url'])
    self.btn_open_youtube_url.visible = bool(trip['youtube_url'])
    self.btn_open_tripit_edit.visible = bool(trip['tripit_edit'])
    self.btn_open_tripit_read.visible = bool(trip['tripit_read'])


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

  def _update_itinerary_status(self):
    # New file selected in this session
      if self.file_itinerary.file:
        name = getattr(self.file_itinerary.file, "name", None) or "(selected file)"
        self.lbl_itinerary_status.text = f"Selected: {name}"
        return

    # Existing file on the trip
      if self.trip_row and self.trip_row['itinerary']:
        existing = self.trip_row['itinerary']
        name = getattr(existing, "name", None) or "(existing file)"
        self.lbl_itinerary_status.text = f"Current: {name}"
      else:
        self.lbl_itinerary_status.text = "No itinerary file"

  @handle("file_itinerary", "change")
  def file_itinerary_change(self, file, **event_args):
    self._update_itinerary_status()

  def _open_url(self, url):
    if not url:
      alert("No URL to open")
      return
    open_form("UrlRedirect", url=url)

  @handle("btn_open_web_url", "click")
  def btn_open_web_url_click(self, **e):
    self._open_url(self.txt_web_url.text)
  
  @handle("btn_open_youtube_url", "click")
  def btn_open_youtube_url_click(self, **e):
    self._open_url(self.txt_youtube_url.text)
  
  @handle("btn_open_tripit_edit", "click")
  def btn_open_tripit_edit_click(self, **e):
    self._open_url(self.txt_tripit_edit.text)
  
  @handle("btn_open_tripit_read", "click")
  def btn_open_tripit_read_click(self, **e):
    self._open_url(self.txt_tripit_read.text)



