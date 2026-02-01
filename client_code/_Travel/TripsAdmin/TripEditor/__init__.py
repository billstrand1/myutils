from ._anvil_designer import TripEditorTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users


class TripEditor(TripEditorTemplate):
  def __init__(self, trip_row=None, mode="view", **properties):
    self.init_components(**properties)
    self.trip_row = trip_row
    self.mode = mode   # ← MUST come before _apply_mode()
    
    if trip_row:
      self.lbl_title.text = 'Edit Trip'
    else:
      self.lbl_title.text = 'New Trip'
      
    self.trip_details.load_trip(trip_row)
    self.trip_assets_manager.load_trip(trip_row)

    self._apply_mode()

    # Later:
    # can_edit = anvil.users.get_user()['is_admin']
    # self.btn_edit.visible = is_view and can_edit
    
    # TripIt links: ONLY visible for new trips
    # is_new = trip_row is None
    # self.trip_details.txt_tripit_edit.visible = is_new
    # self.trip_details.txt_tripit_read.visible = is_new
    # self.trip_details.txt_tripit_edit.enabled = is_new
    # self.trip_details.txt_tripit_read.enabled = is_new


  @handle("button_save", "click")
  def button_save_click(self, **event_args):
    trip_data = self.trip_details.collect_data()

    if self.trip_row:
      anvil.server.call("update_trip", self.trip_row, trip_data)
    else:
      self.trip_row = anvil.server.call("create_trip", trip_data)

    # self.trip_assets_manager.set_trip(self.trip_row)
    n=Notification("Trip Saved",  title= 'Success.')#("Trip saved")
    n.show()
    # open_form("_Travel.TripsAdmin")
    

  @handle("button_cancel", "click")
  def button_cancel_click(self, **event_args):
    alert("Changes not saved", timeout=2)
    # open_form("_Travel.TripsAdmin")

  @handle("btn_return_home", "click")
  def btn_return_home_click(self, **event_args):
    if confirm(
      "Return to Trips Admin?\nAny unsaved changes will be lost.",
      title="Return to Trips"
    ):
      open_form("_Travel.TripsAdmin")


  def _apply_mode(self):
    # mode = getattr(self, "mode", "edit")
    # is_view = self.mode == "view"
    is_view = self.mode == "view"

    # TripDetails controls
    self.trip_details.set_read_only(is_view)

    # Assets: view-only still allowed
    self.trip_assets_manager.set_read_only(is_view)

    # Buttons
    self.button_save.visible = not is_view
    self.button_cancel.visible = not is_view
    self.btn_edit.visible = is_view
    
    # Return Home always available
    self.btn_return_home.visible = True

    if self.mode == "view":
      self.lbl_title.text = "View Trip"
    else:
      self.lbl_title.text = "Edit Trip"

  @handle("btn_edit", "click")
  def btn_edit_click(self, **event_args):
    self.mode = "edit"
    self._apply_mode()


