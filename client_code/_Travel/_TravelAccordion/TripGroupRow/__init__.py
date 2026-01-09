from ._anvil_designer import TripGroupRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class TripGroupRow(TripGroupRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    
    self._expanded = False
    self._loaded = False
    self._items = []

    trip = self.item

    # ---- Header fields ----
    self.label_trip_title.text = trip['trip_id']
    self.label_trip_description.text = trip['trip_description'] or ""

    # Dates (formatted)
    self.label_trip_dates.text = self._format_dates(
      trip['start_date'], trip['end_date']
    )

    # Item count (filled after assets load)
    # self.label_item_count.text = ""
    count = self._precompute_item_count()
    self.label_item_count.text = f"• {count} items" if count else ""


    # Accordion initial state
    self.panel_body.visible = False
    self.link_toggle.text = "▶"

    self._load_thumbnail()

  # ---------------- accordion toggle ----------------

  def link_toggle_click(self, **event_args):
    self._expanded = not self._expanded
    self.panel_body.visible = self._expanded
    self.link_toggle.text = "▼" if self._expanded else "▶"

    if self._expanded and not self._loaded:
      self._load_assets()
      self._loaded = True
      # ✅ Now we know the count
      # self.label_item_count.text = f"• {len(self._items)} items"

  # ---------------- asset loading ----------------

  def _load_assets(self):
    trip = self.item
    tid  = trip['trip_id']
    desc = trip['trip_description'] or ""

    items = []

    # 1) Notes
    if trip['notes']:
      items.append(self._notes_item(tid, desc, trip['notes'], trip))

    # 2) Itinerary
    if trip['itinerary']:
      items.append(self._file_item(tid, desc, trip['itinerary'], trip))

    # 3) TripIt Read
    if trip['tripit_read']:
      items.append(self._web_item(tid, desc, trip['tripit_read'], trip, label="TripIt"))

    # 4) YouTube (trip)
    if trip['youtube_url']:
      items.append(self._youtube_item(tid, desc, trip['youtube_url'], trip))

    # 5) Web (trip)
    if trip['web_url']:
      items.append(self._web_item(tid, desc, trip['web_url'], trip))

    # 6) trip_data assets
    for r in app_tables.trip_data.search(trip_link=trip):
      if r['file']:
        items.append(self._file_item(tid, desc, r['file'], r))
      if r['youtube_url']:
        items.append(self._youtube_item(tid, desc, r['youtube_url'], r))
      if r['web_url']:
        items.append(self._web_item(tid, desc, r['web_url'], r))

    items.sort(key=self._sort_key)

    self._items = items
    self.repeating_panel_assets.items = items


  def _load_thumbnail(self):
    """
    Load the 64x64 thumbnail image for this trip, if one exists.
    """
    trip = self.item
  
    thumb_rows = app_tables.trip_data.search(
      trip_link=trip,
      is_thumbnail=True
    )
  
    thumb_row = next(iter(thumb_rows), None)
  
    if thumb_row and thumb_row['file']:
      self.image_thumbnail.source = thumb_row['file']
      self.image_thumbnail.visible = True
    else:
      self.image_thumbnail.source = None
      self.image_thumbnail.visible = False

  # ---------------- item factories ----------------

  def _notes_item(self, title, comments, notes, src):
    return {
      'title': title,
      'comments': comments,
      'notes': notes,
      'file': None,
      'youtube_url': None,
      'web_url': None,
      'source_row': src
    }

  def _file_item(self, title, comments, media, src):
    return {
      'title': title,
      'comments': comments,
      'notes': "",
      'file': media,
      'youtube_url': None,
      'web_url': None,
      'source_row': src
    }

  def _youtube_item(self, title, comments, url, src):
    return {
      'title': title,
      'comments': comments,
      'notes': "",
      'file': None,
      'youtube_url': url,
      'web_url': None,
      'source_row': src
    }

  def _web_item(self, title, comments, url, src, label=None):
    item = {
      'title': title,
      'comments': comments,
      'notes': "",
      'file': None,
      'youtube_url': None,
      'web_url': url,
      'source_row': src
    }
    if label:
      item['web_label'] = label
    return item

  # ---------------- sorting ----------------

  def _sort_key(self, it):
    if it.get('notes'):
      return 0
    if it.get('file') and it.get('source_row') == self.item:
      return 1
    if it.get('web_label') == 'TripIt':
      return 2
    if it.get('youtube_url') and it.get('source_row') == self.item:
      return 3
    if it.get('web_url') and it.get('source_row') == self.item:
      return 4
    if it.get('file'):
      return 5
    if it.get('youtube_url'):
      return 6
    if it.get('web_url'):
      return 7
    return 99

  # ---------------- helpers ----------------

  def _format_dates(self, start_date, end_date):
    if not start_date:
      return ""

    if not end_date or start_date == end_date:
      return start_date.strftime("%b %d, %Y")

    if start_date.year == end_date.year:
      if start_date.month == end_date.month:
        return f"{start_date.strftime('%b %d')}–{end_date.strftime('%d, %Y')}"
      return f"{start_date.strftime('%b %d')}–{end_date.strftime('%b %d, %Y')}"

    return f"{start_date.strftime('%b %d, %Y')}–{end_date.strftime('%b %d, %Y')}"

  def _precompute_item_count(self):
    trip = self.item
    count = 0
  
    if trip['notes']:
      count += 1
    if trip['itinerary']:
      count += 1
    if trip['tripit_read']:
      count += 1
    if trip['youtube_url']:
      count += 1
    if trip['web_url']:
      count += 1
  
    for r in app_tables.trip_data.search(trip_link=trip):
      if r['file'] or r['youtube_url'] or r['web_url']:
        count += 1
  
    return count

  def expand(self):
    if not self._expanded:
      self.link_toggle_click()
  
  def collapse(self):
    if self._expanded:
      self.link_toggle_click()

