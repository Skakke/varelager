# SQLite database setup.

import sqlite3

# Database filnavn.
DB_FILE = "database.db"

# Lager nødvendige tabeller i databasen.
def create_tables():
    # Oppretter en tilkobling til SQLite-databasen.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS varer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        varenavn TEXT NOT NULL,
        antall_paa_lager INTEGER NOT NULL,
        kategori INT,
        kort_beskrivelse TEXT 
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kategorier (
        id INTEGER PRIMARY KEY,
        navn TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Legger til kategori i databasen
def legg_til_ny_kategori(navn):
    # Oppretter en tilkobling til SQLite-databasen.
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO kategorier (navn) VALUES (?)
        """, [navn])

        conn.commit()
        return cursor.rowcount == 1
    finally:
        conn.close()
    
# Legger til vare i databasen
def legg_til_ny_vare(navn, kategori, antall_paa_lager, kort_beskrivelse):
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.execute("""
            INSERT INTO varer (
                varenavn, kategori, antall_paa_lager, kort_beskrivelse
            )
            VALUES (?, ?, ?, ?)
        """, (navn, kategori, antall_paa_lager, kort_beskrivelse))
        conn.commit()
        return cursor.rowcount == 1
    finally:
        conn.close()

# Oppdaterer en eksisterende vare. Returnerer False hvis varen ikke finnes.
def oppdater_vare(vare_id, navn, kategori, antall_paa_lager, kort_beskrivelse):
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.execute("""
            UPDATE varer
            SET varenavn = ?, kategori = ?, antall_paa_lager = ?, kort_beskrivelse = ?
            WHERE id = ?
        """, (navn, kategori, antall_paa_lager, kort_beskrivelse, vare_id))
        conn.commit()
        return cursor.rowcount == 1
    finally:
        conn.close()


# Søker etter varer der varenummeret (id) er lik søkeordet, eller navnet inneholder det.
# Tomt søkeord gir alle varer.
def sok_varer(sokeord):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
            SELECT id, varenavn, kategori, antall_paa_lager, kort_beskrivelse
            FROM varer
            WHERE id = ? OR varenavn LIKE ?
            ORDER BY id = ? DESC, varenavn
        """, [sokeord, f"%{sokeord}%", sokeord]).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

# Henter alle kategorier, sortert på navn.
def hent_kategorier():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT id, navn FROM kategorier ORDER BY navn").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

# Sletter en vare fra databasen. Returnerer False hvis varen ikke finnes.
def slett_vare(id):
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.execute("DELETE FROM varer WHERE id = ?", [id])
        conn.commit()
        return cursor.rowcount == 1
    finally:
        conn.close()
