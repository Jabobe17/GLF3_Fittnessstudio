from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
from .Anmelden import Anmelden


class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lade_kurse()

  def lade_kurse(self):
    self.repeating_panel_1.items = anvil.server.call("get_kurse")

  def oeffne_anmeldung(self, kurs_id):
    alert(
      content=Anmelden(kurs_id=kurs_id),
      title="Mitglied anmelden",
      large=True,
      buttons=[]
    )
    self.lade_kurse()