
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from models import Note
from typing import Optional


def create_note(db: Session, title: str, content: str):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session):
    return db.query(Note).all()

def get_note_by_id(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def update_note(db: Session, note_id: int, title: Optional[str] = None, content: Optional[str] = None):
    # Получить существующую заметку
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        if title is not None:  # Обновить только если передано
            note.title = title
        if content is not None:  # Обновить только если передано
            note.content = content
        db.commit()
        db.refresh(note)
    return note


def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note
