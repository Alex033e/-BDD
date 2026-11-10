
from fastapi import FastAPI, HTTPException
from models import Note, NoteCreate, NoteUpdate
import database as db

app = FastAPI(title="Note Service API")

@app.get("/notes", response_model=list[Note])
def list_notes():
    return db.get_all_notes()

@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate):
    return db.create_note(note.title, note.content)

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = db.find_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteUpdate):
    updated = db.update_note(note_id, note.title, note.content)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if not db.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted"}