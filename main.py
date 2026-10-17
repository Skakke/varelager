from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import legg_til_ny_vare, create_tables
from fastapi import HTTPException
import sqlite3
from pydantic import BaseModel

app = FastAPI()

create_tables()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

class Vare(BaseModel):
    varenavn: str
    kategori: str
    antall_paa_lager: int
    kort_beskrivelse: str

@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.post("/api/varer", status_code=201)
def add_vare(vare: Vare):
    try:
        saved = legg_til_ny_vare(
            vare.varenavn,
            vare.kategori,
            vare.antall_paa_lager,
            vare.kort_beskrivelse,
        )
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke lagre varen.",
        ) from error

    if not saved:
        raise HTTPException(status_code=500, detail="Varen ble ikke lagret.")

    return {"success": True, "message": "Vare lagt til."}
