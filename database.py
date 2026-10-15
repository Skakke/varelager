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

# Legger til kategorier i databasen, kjøres fra et setupvindu eller lignende.
def add_categories():
    # Oppretter en tilkobling til SQLite-databasen.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO kategorier (id,navn) VALUES (?, ?)
    """, [
        (1, 'Elektronikk'),
        (2, 'Klær'),
        (3, 'Mat'),
        (4, 'Møbler')
    ])

    conn.commit()
    conn.close()

def legg_til_ny_vare(navn, kategori, kort_beskrivelse):
    # Oppretter en tilkobling til SQLite-databasen.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor();
    cursor.execute("""
    INSERT INTO varer (varenavn, kategori, kort_beskrivelse) 
    VALUES (?, ?, ?)
    """, (navn, kategori, kort_beskrivelse))

    conn.commit()
    conn.close()

