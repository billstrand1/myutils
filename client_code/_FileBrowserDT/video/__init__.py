from ._anvil_designer import videoTemplate
from anvil import *
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js.window import document

class video(videoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.video_dom = document.createElement('video')
    self.video_dom.controls=True
    anvil.js.get_dom_node(self).appendChild(self.video_dom)
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

  @property
  def source(self):
    '''The source of Video Component'''
    return self.source

  @source.setter
  def source(self,source):
    self.video_dom.src=source

  @property
  def height(self):
    '''Height of Video Component in px'''
    return self.height

  @height.setter
  def height(self,height):
    self.video_dom.style.height=f'{height}px'

  @property
  def width(self):
    '''Width of Video Component in px'''
    return self.width

  @width.setter
  def width(self,width):
    self.video_dom.style.width=f'{width}px'


