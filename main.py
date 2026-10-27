from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import legg_til_ny_vare, legg_til_ny_kategori, create_tables, oppdater_vare, sok_varer, hent_kategorier
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

class Kategori(BaseModel):
    navn: str

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )

@app.get("/nyvare")
def leggtilvare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="nyvare.html",
        context={"kategorier": hent_kategorier()},
    )

@app.get("/endrevare")
def endrevare(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="endrevare.html",
        context={"kategorier": hent_kategorier()},
    )

# Viser alle varer, eller bare de som passer med søket.
@app.get("/varer")
def visvarer(request: Request, sok: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="varer.html",
        context={"varer": sok_varer(sok.strip()), "sok": sok},
    )

@app.get("/nykategori")
def leggtilkategori(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="nykategori.html",
        context={},
    )


@app.post("/api/nyvare", status_code=201)
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
def add_kategori(kategori: Kategori):
    try:
        legg_til_ny_kategori(kategori.navn)

    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=409,
            detail="Kategorien finnes allerede.",
        ) from error

    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke opprette kategorien.",
        ) from error
    
    return {"success": True, "message": "Kategori lagt til."}


@app.get("/api/varer")
def search_varer(sok: str = ""):
    return sok_varer(sok.strip())

@app.put("/api/varer/{vare_id}")
def update_vare(vare_id: int, vare: Vare):
    try:
        updated = oppdater_vare(
            vare_id,
            vare.varenavn,
            vare.kategori,
            vare.antall_paa_lager,
            vare.kort_beskrivelse,
        )
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke oppdatere varen.",
        ) from error

    if not updated:
        raise HTTPException(status_code=404, detail="Fant ikke varen.")

    return {"success": True, "message": "Vare oppdatert."}
