from ._anvil_designer import GroupTemplateTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class GroupTemplate(GroupTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # self.item is a dict like {'name': 'Susan', 'items': [...]}
    self.label_header.text = f"{self.item['name']}'s List:"
    self.repeating_panel_items.items = self.item['items']

    # If a child deletes an item, pass the refresh signal up to the main form
    self.repeating_panel_items.set_event_handler('x-refresh-all', 
      lambda **e: self.parent.raise_event('x-refresh-all'))