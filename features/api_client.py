import requests


class NoteApiClient:

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url

    def get_notes(self):
        return requests.get(f"{self.base_url}/notes")

    def create_note(self, payload):
        return requests.post(f"{self.base_url}/notes", json=payload)

    def get_note_by_id(self, note_id):
        return requests.get(f"{self.base_url}/notes/{note_id}")

    def update_note(self, note_id, payload):
        return requests.put(f"{self.base_url}/notes/{note_id}", json=payload)

    def delete_note(self, note_id):
        return requests.delete(f"{self.base_url}/notes/{note_id}")
