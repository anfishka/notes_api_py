from fastapi import FastAPI, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import jsonpatch
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from database import SessionLocal, engine, Base, get_db
from models import Note
from crud import create_note, get_notes, get_note_by_id, update_note, delete_note
import jsonpatch

# Инициализация базы данных
Base.metadata.create_all(bind=engine)


app = FastAPI()

class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

# Получить все заметки
@app.get("/notes")
def read_notes(db: Session = Depends(get_db)):
    return get_notes(db)

# Получить заметку по ID
@app.get("/notes/{note_id}")
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Создать новую заметку


@app.patch("/notes/{note_id}")
def patch_note(
    note_id: int,
    note_update: NoteUpdate = Body(...),  # Явно указываем, что это тело запроса
    db: Session = Depends(get_db)
):
    # Получить существующую заметку
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    # Проверить, какие поля были переданы, и обновить их
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    # Сохранить изменения
    db.commit()
    db.refresh(note)

    return {
        "message": "Note updated successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
    }
# Удалить заметку
@app.delete("/notes/{note_id}")
def delete_existing_note(note_id: int, db: Session = Depends(get_db)):
    note = delete_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted"}
