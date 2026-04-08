from ._anvil_designer import RowTemplate1Template
from anvil import *


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    get_open_form().oeffne_anmeldung(self.item["kurs_id"])