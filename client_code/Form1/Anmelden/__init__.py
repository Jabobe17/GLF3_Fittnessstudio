from ._anvil_designer import AnmeldenTemplate
from anvil import *
import anvil.server


class Anmelden(AnmeldenTemplate):
  def __init__(self, kurs_id=None, **properties):
    self.init_components(**properties)

    self.kurs_id = kurs_id
    self.lade_mitglieder()

  def lade_mitglieder(self):
    self.repeating_panel_1.items = anvil.server.call("get_freie_mitglieder", self.kurs_id)