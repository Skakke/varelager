from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import legg_til_ny_vare, create_tables
from fastapi import HTTPException
import sqlite3
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates



app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )

@app.get("/leggtilvare")
def leggtilvare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="leggtilvare.html",
        context={},
    )

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


@app.post("/api/kategorier", status_code=201)
def add_kategori(kategori: str):
    try:
        saved = legg_til_ny_kategori(kategori)
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke opprette kategorien.",
        ) from error

    if not saved:
        raise HTTPException(status_code=500, detail="Kategorien ble ikke lagret.")

    return {"success": True, "message": "Kategori lagt til."}