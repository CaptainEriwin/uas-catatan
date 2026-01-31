import os
from datetime import datetime, date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "notesdb")

client = MongoClient(MONGODB_URL)
db = client[MONGODB_DB]
notes = db["notes"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteIn(BaseModel):
    tanggal: date
    kegiatan: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/notes")
def list_notes():
    items = []
    for n in notes.find({}, {"_id": 0}).sort("created_at", -1):
        items.append(n)
    return items

@app.post("/notes")
def create_note(note: NoteIn):
    doc = {
        "tanggal": note.tanggal.isoformat(),
        "kegiatan": note.kegiatan,
        "created_at": datetime.utcnow().isoformat(),
    }
    notes.insert_one(doc)
    return doc
