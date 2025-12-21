from ._anvil_designer import TripGroupRowTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TripGroupRow(TripGroupRowTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self._expanded = False
    self._loaded = False
    self._items = []

    self.panel_body.visible = False
    self.link_toggle.text = "▶"

  def form_show(self, **event_args):
    trip = self.item

    self.label_trip_title.text = trip['trip_id']

    # Dates (optional)
    sd = trip['start_date']
    ed = trip['end_date']
    if sd and ed:
      self.label_trip_dates.text = f"{sd} – {ed}"
      self.label_trip_dates.visible = True
    elif sd:
      self.label_trip_dates.text = f"{sd}"
      self.label_trip_dates.visible = True
    else:
      self.label_trip_dates.text = ""
      self.label_trip_dates.visible = False

    # ✅ Trip Description
    desc = trip['trip_description'] or ""
    self.label_trip_description.text = desc
    self.label_trip_description.visible = bool(desc)

    # Item count (filled after first expand)
    self.label_item_count.text = ""

  def link_toggle_click(self, **event_args):
    self._expanded = not self._expanded
    self.panel_body.visible = self._expanded
    self.link_toggle.text = "▼" if self._expanded else "▶"

    if self._expanded and not self._loaded:
      self._load_assets()
      self._loaded = True
      self.label_item_count.text = f"{len(self._items)} items"

  # ---------------- asset loading ----------------

  def _load_assets(self):
    trip = self.item
    tid  = trip['trip_id']
    desc = trip['trip_description'] or ""

    items = []

    # 1) Notes
    if trip['notes']:
      items.append(self._make_notes_item(tid, desc, trip['notes'], trip))

    # 2) Itinerary
    if trip['itinerary']:
      items.append(self._make_file_item(tid, desc, trip['itinerary'], trip))

    # 3) TripIt Read (NEW)
    if trip['tripit_read']:
      items.append(self._make_web_item(
        tid, desc, trip['tripit_read'], trip, label="TripIt"
      ))

    # 4) YouTube (trip)
    if trip['youtube_url']:
      items.append(self._make_youtube_item(tid, desc, trip['youtube_url'], trip))

    # 5) Web (trip)
    if trip['web_url']:
      items.append(self._make_web_item(tid, desc, trip['web_url'], trip))

    # 6) trip_data assets
    for r in app_tables.trip_data.search(trip_link=trip):
      if r['file']:
        items.append(self._make_file_item(tid, desc, r['file'], r))
      if r['youtube_url']:
        items.append(self._make_youtube_item(tid, desc, r['youtube_url'], r))
      if r['web_url']:
        items.append(self._make_web_item(tid, desc, r['web_url'], r))

    items.sort(key=self._sort_key)

    self._items = items
    self.repeating_panel_assets.items = items

  # ---------------- item factories ----------------

  def _make_notes_item(self, title, comments, notes, src):
    return dict(title=title, comments=comments, notes=notes,
                file=None, youtube_url=None, web_url=None, source_row=src)

  def _make_file_item(self, title, comments, media, src):
    return dict(title=title, comments=comments, notes="",
                file=media, youtube_url=None, web_url=None, source_row=src)

  def _make_youtube_item(self, title, comments, url, src):
    return dict(title=title, comments=comments, notes="",
                file=None, youtube_url=url, web_url=None, source_row=src)

  def _make_web_item(self, title, comments, url, src, label=None):
    item = dict(title=title, comments=comments, notes="",
                file=None, youtube_url=None, web_url=url, source_row=src)
    if label:
      item['web_label'] = label
    return item

  # ---------------- sorting ----------------

  def _sort_key(self, it):
    # 0 Notes
    if it.get('notes'):
      return 0

    # 1 Trip itinerary (file from trips row)
    if it.get('file') and it.get('source_row') == self.item:
      return 1

    # 2 TripIt read link
    if it.get('web_label') == 'TripIt':
      return 2

    # 3 Trip YouTube
    if it.get('youtube_url') and it.get('source_row') == self.item:
      return 3

    # 4 Trip web
    if it.get('web_url') and it.get('source_row') == self.item:
      return 4

    # 5 Other files (trip_data)
    if it.get('file'):
      return 5

    # 6 Other YouTube (trip_data)
    if it.get('youtube_url'):
      return 6

    # 7 Other web (trip_data)
    if it.get('web_url'):
      return 7

    return 99
