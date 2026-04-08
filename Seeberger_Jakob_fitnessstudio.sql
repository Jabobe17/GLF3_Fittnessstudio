PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS anmeldungen;
DROP TABLE IF EXISTS kurse;
DROP TABLE IF EXISTS mitglieder;
DROP TABLE IF EXISTS trainer;

CREATE TABLE trainer (
    trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vorname TEXT NOT NULL,
    nachname TEXT NOT NULL,
    spezialgebiet TEXT NOT NULL
);

CREATE TABLE kurse (
    kurs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bezeichnung TEXT NOT NULL,
    wochentag TEXT NOT NULL,
    uhrzeit TEXT NOT NULL,
    max_teilnehmer INTEGER NOT NULL CHECK (max_teilnehmer > 0),
    trainer_id INTEGER NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE mitglieder (
    mitglied_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vorname TEXT NOT NULL,
    nachname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    beitrittsdatum TEXT NOT NULL
);

CREATE TABLE anmeldungen (
    anmeldung_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mitglied_id INTEGER NOT NULL,
    kurs_id INTEGER NOT NULL,
    anmeldedatum TEXT NOT NULL,
    FOREIGN KEY (mitglied_id) REFERENCES mitglieder(mitglied_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (kurs_id) REFERENCES kurse(kurs_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_anmeldung UNIQUE (mitglied_id, kurs_id)
);

INSERT INTO trainer (vorname, nachname, spezialgebiet) VALUES
('Anna', 'Huber', 'Yoga'),
('Lukas', 'Gruber', 'Spinning'),
('Sophie', 'Mayer', 'Pilates');

INSERT INTO kurse (bezeichnung, wochentag, uhrzeit, max_teilnehmer, trainer_id) VALUES
('Yoga Basics', 'Montag', '18:00', 15, 1),
('Pilates Flow', 'Dienstag', '17:30', 12, 3),
('Spinning Power', 'Mittwoch', '19:00', 20, 2),
('Zumba Energy', 'Donnerstag', '18:30', 18, 2),
('Morning Stretch', 'Freitag', '07:30', 10, 1);

INSERT INTO mitglieder (vorname, nachname, email, beitrittsdatum) VALUES
('Max', 'Schneider', 'max.schneider@example.com', '2026-01-10'),
('Laura', 'Fischer', 'laura.fischer@example.com', '2026-01-15'),
('David', 'Weber', 'david.weber@example.com', '2026-02-01'),
('Julia', 'Bauer', 'julia.bauer@example.com', '2026-02-05'),
('Emma', 'Hofer', 'emma.hofer@example.com', '2026-02-11'),
('Noah', 'Leitner', 'noah.leitner@example.com', '2026-03-02');

INSERT INTO anmeldungen (mitglied_id, kurs_id, anmeldedatum) VALUES
(1, 1, '2026-03-10'),
(1, 3, '2026-03-11'),
(2, 1, '2026-03-12'),
(2, 2, '2026-03-12'),
(3, 3, '2026-03-13'),
(4, 4, '2026-03-14'),
(5, 5, '2026-03-15'),
(6, 2, '2026-03-16'),
(6, 4, '2026-03-16');
