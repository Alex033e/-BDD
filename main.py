# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модели Pydantic
class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Временное хранилище (вместо БД)
notes_db: List[Note] = []
note_counter = 1

# --- ОЧИСТКА БАЗЫ ПРИ СТАРТЕ ---
# Эта строка выполняется ОДИН РАЗ при запуске сервера (uvicorn).
# Она гарантирует, что список notes_db всегда пустой при старте тестов.
notes_db.clear()
# --------------------------------

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    global note_counter
    note_data = note.dict()
    note_data["id"] = note_counter
    note_counter += 1
    notes_db.append(Note(**note_data))
    return Note(**note_data)

@app.get("/notes", status_code=200)
def list_notes():
    return notes_db

@app.get("/notes/{note_id}", status_code=200)
def get_note(note_id: int):
    for note in notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}", status_code=200)
def update_note(note_id: int, note: NoteUpdate):
    for i, db_note in enumerate(notes_db):
        if db_note.id == note_id:
            update_data = note.dict(exclude_unset=True)
            updated_note = db_note.copy(update=update_data)
            notes_db[i] = updated_note
            return updated_note
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}", status_code=200)
def delete_note(note_id: int):
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            return {"detail": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")