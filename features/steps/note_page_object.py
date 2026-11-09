# features/steps/note_page_object.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NoteApiService:
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

    @staticmethod
    def create_note(payload):
        url = f"{NoteApiService.BASE_URL}/notes"
        response = requests.post(url, json=payload)
        return response

    @staticmethod
    def list_notes():
        url = f"{NoteApiService.BASE_URL}/notes"
        response = requests.get(url)
        return response

    @staticmethod
    def get_note(note_id):
        url = f"{NoteApiService.BASE_URL}/notes/{note_id}"
        response = requests.get(url)
        return response

    @staticmethod
    def update_note(note_id, payload):
        url = f"{NoteApiService.BASE_URL}/notes/{note_id}"
        response = requests.put(url, json=payload)
        return response

    @staticmethod
    def delete_note(note_id):
        url = f"{NoteApiService.BASE_URL}/notes/{note_id}"
        response = requests.delete(url)
        return response