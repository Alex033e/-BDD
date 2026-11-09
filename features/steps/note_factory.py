# features/steps/note_factory.py
import random
from faker import Faker

fake = Faker()

class NoteFactory:
    @staticmethod
    def generate_valid_note():
        return {
            "title": fake.sentence(nb_words=4, variable_nb_words=True),
            "content": fake.text(max_nb_chars=200)
        }

    @staticmethod
    def generate_invalid_note():
        return {"title": "", "content": fake.text()}