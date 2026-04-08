import anvil.server
from anvil.files import data_files
import sqlite3
import datetime

DB_NAME = "Seeberger_Jakob_fitnessstudio.db"


def get_db():
  conn = sqlite3.connect(data_files[DB_NAME])
  conn.row_factory = sqlite3.Row
  return conn


@anvil.server.callable
def get_kurse():
  conn = get_db()
  cur = conn.cursor()

  cur.execute("""
    SELECT
      k.kurs_id,
      k.bezeichnung,
      k.wochentag,
      k.uhrzeit,
      t.vorname || ' ' || t.nachname AS trainer,
      COUNT(a.anmeldung_id) AS teilnehmer
    FROM kurse k
    JOIN trainer t ON k.trainer_id = t.trainer_id
    LEFT JOIN anmeldungen a ON k.kurs_id = a.kurs_id
    GROUP BY k.kurs_id, k.bezeichnung, k.wochentag, k.uhrzeit, trainer
    ORDER BY k.wochentag, k.uhrzeit
  """)

  daten = []
  for row in cur.fetchall():
    daten.append({
      "Kurse": row["bezeichnung"],
      "Wochentag": row["wochentag"],
      "Uhrzeit": row["uhrzeit"],
      "Trainer": row["trainer"],
      "Teilnehmer": str(row["teilnehmer"]),
      "kurs_id": row["kurs_id"]
    })

  conn.close()
  return daten


@anvil.server.callable
def get_freie_mitglieder(kurs_id):
  conn = get_db()
  cur = conn.cursor()

  cur.execute("""
    SELECT m.mitglied_id, m.vorname, m.nachname
    FROM mitglieder m
    WHERE m.mitglied_id NOT IN (
      SELECT a.mitglied_id
      FROM anmeldungen a
      WHERE a.kurs_id = ?
    )
    ORDER BY m.nachname, m.vorname
  """, (kurs_id,))

  daten = []
  for row in cur.fetchall():
    daten.append({
      "Mitglied": f"{row['vorname']} {row['nachname']}",
      "mitglied_id": row["mitglied_id"]
    })

  conn.close()
  return daten


@anvil.server.callable
def anmelden(mitglied_id, kurs_id):
  with data_files.editing(DB_NAME) as db_path:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
      INSERT INTO anmeldungen (mitglied_id, kurs_id, anmeldedatum)
      VALUES (?, ?, ?)
    """, (mitglied_id, kurs_id, datetime.date.today().isoformat()))

    conn.commit()
    conn.close()