from behave import given, when, then
from features.api_client import NoteApiClient
from features.note_factory import NoteFactory

# Инициализируем Page Object
api = NoteApiClient()

# Вспомогательная функция для очистки базы данных для BDD тестов (опционально)
def clear_in_memory_db():
    import database as db
    db.notes_db.clear()
    db.next_id = 1

# --- ШАГИ ДЛЯ СОЗДАНИЯ ---
@given('I generate a valid note dataset')
def step_impl(context):
    context.payload = NoteFactory.create_valid_data()

@given('I generate an invalid note dataset with "{scenario_type}"')
def step_impl(context, scenario_type):
    context.payload = NoteFactory.create_invalid_data(scenario_type)

@when('I send a request to create a note')
def step_impl(context):
    context.response = api.create_note(context.payload)
    if context.response.status_code == 200:
        context.created_note = context.response.json()

# --- ШАГИ ДЛЯ СПИСКА ЗАМЕТОК ---
@given('the database is empty')
def step_impl(context):
    clear_in_memory_db()

@given('at least one note exists in the database')
def step_impl(context):
    clear_in_memory_db()
    payload = NoteFactory.create_valid_data(title="Existing Note")
    api.create_note(payload)

@when('I request the list of all notes')
def step_impl(context):
    context.response = api.get_notes()

@then('the response should be an empty list')
def step_impl(context):
    assert context.response.json() == []

@then('the response should contain a non-empty list of notes')
def step_impl(context):
    data = context.response.json()
    assert isinstance(data, list) and len(data) > 0

# --- ШАГИ ДЛЯ ПОЛУЧЕНИЯ И РАБОТЫ С ID ---
@given('a note is freshly created and its ID is saved')
def step_impl(context):
    payload = NoteFactory.create_valid_data()
    res = api.create_note(payload)
    context.created_note = res.json()
    context.target_id = context.created_note['id']

@given('an invalid note ID "{invalid_id}"')
def step_impl(context, invalid_id):
    context.target_id = int(invalid_id)

@when('I request the note by its valid ID')
@when('I request the note by this ID')
def step_impl(context):
    context.response = api.get_note_by_id(context.target_id)

# --- ШАГИ ДЛЯ РЕДАКТИРОВАНИЯ ---
@given('I generate a valid note dataset for update')
def step_impl(context):
    context.update_payload = NoteFactory.create_valid_data(title="Updated Title", content="Updated Content")

@when('I send a request to update this note')
def step_impl(context):
    context.response = api.update_note(context.target_id, context.update_payload)

# --- ШАГИ ДЛЯ УДАЛЕНИЯ ---
@when('I send a request to delete this note')
def step_impl(context):
    context.response = api.delete_note(context.target_id)

# --- ШАГИ АССЕРТОВ (ПРОВЕРОК) ---
@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@then('the response should contain the correct title and content')
def step_impl(context):
    data = context.response.json()
    assert data['title'] == context.payload['title']
    assert data['content'] == context.payload['content']
    assert 'id' in data

@then('the response should match the created note data')
def step_impl(context):
    data = context.response.json()
    assert data['id'] == context.created_note['id']
    assert data['title'] == context.created_note['title']

@then('the response should contain updated title and content')
def step_impl(context):
    data = context.response.json()
    assert data['title'] == context.update_payload['title']
    assert data['content'] == context.update_payload['content']

@then('the response body detail should say "{message}"')
def step_impl(context, message):
    data = context.response.json()
    assert data.get('detail') == message
