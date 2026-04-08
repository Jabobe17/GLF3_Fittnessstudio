import anvil.server
from anvil.tables import app_tables
import datetime


@anvil.server.callable
def get_kurse():
  daten = []

  for kurs in app_tables.kurse.search():
    trainer = kurs['trainer']
    trainer_name = f"{trainer['vorname']} {trainer['nachname']}"

    teilnehmerzahl = len(list(app_tables.anmeldung.search(kurs=kurs)))

    daten.append({
      'Kurse': kurs['bezeichnung'],
      'Wochentag': kurs['wochentag'],
      'Uhrzeit': kurs['uhrzeit'],
      'Trainer': trainer_name,
      'Teilnehmer': str(teilnehmerzahl),
      'kurs_row': kurs
    })

  return daten


@anvil.server.callable
def get_mitglieder():
  return [
    (f"{m['vorname']} {m['nachname']}", m)
    for m in app_tables.mitglieder.search()
  ]


@anvil.server.callable
def anmelden(mitglied, kurs):
  if mitglied is None:
    raise Exception("Bitte ein Mitglied auswählen.")

  if kurs is None:
    raise Exception("Kein Kurs ausgewählt.")

  schon_da = app_tables.anmeldung.get(mitglied=mitglied, kurs=kurs)
  if schon_da:
    raise Exception("Dieses Mitglied ist bereits angemeldet.")

  aktuelle_anzahl = len(list(app_tables.anmeldung.search(kurs=kurs)))
  max_teilnehmer = kurs['max_teilnehmer']

  if aktuelle_anzahl >= max_teilnehmer:
    raise Exception("Dieser Kurs ist bereits voll.")

  app_tables.anmeldung.add_row(
    mitglied=mitglied,
    kurs=kurs,
    anmeldedatum=datetime.date.today()
  )