from typing import List, Dict

notes_db: Dict[int, Dict] = {}
next_id = 1

def get_all_notes() -> List[Dict]:
    return list(notes_db.values())

def find_note(note_id: int) -> Dict:
    return notes_db.get(note_id)

def create_note(title: str, content: str) -> Dict:
    global next_id
    note = {"id": next_id, "title": title, "content": content}
    notes_db[next_id] = note
    next_id += 1
    return note

def update_note(note_id: int, title: str, content: str) -> Dict:
    if note_id not in notes_db:
        return None
    notes_db[note_id]["title"] = title
    notes_db[note_id]["content"] = content
    return notes_db[note_id]

def delete_note(note_id: int) -> bool:
    return notes_db.pop(note_id, None) is not None