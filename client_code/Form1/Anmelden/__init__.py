from ._anvil_designer import AnmeldenTemplate
from anvil import *
import anvil.server

class Anmelden(AnmeldenTemplate):
  def __init__(self, kurs=None, **properties):
    self.init_components(**properties)

    self.kurs = kurs
    self.drop_down_1.items = anvil.server.call('get_mitglieder')

    if kurs is not None:
      self.label_1.text = f"Kurs: {kurs['bezeichnung']}"
    else:
      self.label_1.text = "Mitglied anmelden"

  def button_1_click(self, **event_args):
    try:
      anvil.server.call('anmelden', self.drop_down_1.selected_value, self.kurs)
      alert("Anmeldung erfolgreich.")
      self.raise_event('x-close-alert')
      get_open_form().raise_event('x-refresh')
    except Exception as e:
      alert(str(e))