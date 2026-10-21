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
def legg_til_ny_kategori(navn):
    # Oppretter en tilkobling til SQLite-databasen.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO kategorier (navn) VALUES (?)
    """, [navn])

    conn.commit()
    conn.close()

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

