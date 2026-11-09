from behave import given, when, then
from steps.note_page_object import NoteApiService

api_service = NoteApiService()

# --- Шаги для создания (Create) ---
@given('я подготавливаю данные для создания заметки')
def step_impl(context):
    context.note_payload = {"title": "Temp", "content": "Temp"}

@when('я отправляю POST запрос на "/notes" с телом:')
def step_impl(context):
    payload = {"title": context.table[0]["Title"], "content": context.table[0]["Content"]}
    context.response = api_service.create_note(payload)

@when('я отправляю POST запрос на "/notes" с текстом:')
def step_impl(context):
    payload = {"title": context.table[0]["Title"], "content": context.table[0]["Content"]}
    context.response = api_service.create_note(payload)

@then('статус ответа должен быть 201')
def step_impl(context):
    assert context.response.status_code == 201

@then('статус ответа должен быть 422')
def step_impl(context):
    assert context.response.status_code == 422

@then('тело ответа содержит поле "title" со значением "{title}"')
def step_impl(context, title):
    body = context.response.json()
    assert body.get('title') == title

# --- Шаги для получения списка (List) ---
@given('я создал новую заметку ранее')
def step_impl(context):
    api_service.create_note({"title": "Temp", "content": "Temp"})

@when('я отправляю GET запрос на "/notes"')
def step_impl(context):
    context.response = api_service.list_notes()

@then('статус ответа должен быть 200')
def step_impl(context):
    assert context.response.status_code == 200

@then('тело ответа содержит пустой список')
def step_impl(context):
    body = context.response.json()
    assert isinstance(body, list) and len(body) == 0

@then('тело ответа содержит больше одной записи')
def step_impl(context):
    body = context.response.json()
    assert isinstance(body, list) and len(body) > 0

# --- Шаги для получения одной (Get) ---
@given('я имею созданную заметку')
def step_impl(context):
    resp = api_service.create_note({"title": "Temp", "content": "Temp"})
    assert resp.status_code == 201
    context.created_note = resp.json()
    context.note_id = context.created_note['id']

@when('я отправляю GET запрос на "/notes/{note_id:d}"')
def step_impl(context, note_id):
    context.response = api_service.get_note(note_id)

@then('статус ответа должен быть 404')
def step_impl(context):
    assert context.response.status_code == 404

@then('тело ответа содержит "title"')
def step_impl(context):
    body = context.response.json()
    assert 'title' in body

# --- Шаги для удаления (Delete) ---
@when('я отправляю DELETE запрос на "/notes/{note_id:d}"')
def step_impl(context, note_id):
    context.response = api_service.delete_note(note_id)

@when('параметр note_id равен {note_id:d}')
def step_impl(context, note_id):
    context.note_id = note_id

# --- Шаги для обновления (Update) ---
@when('я отправляю PUT запрос на "/notes/{note_id:d}" с данными:')
def step_impl(context, note_id):
    payload = {
        "title": context.table[0]["New Title"],
        "content": context.table[0]["New Content"]
    }
    context.response = api_service.update_note(note_id, payload)

@when('я отправляю PUT запрос на "/notes/{note_id:d}"')
def step_impl(context, note_id):
    context.response = api_service.update_note(note_id, {"title": "X", "content": "Y"})

@then('тело ответа содержит "Updated"')
def step_impl(context):
    body = context.response.json()
    assert 'Updated' in body.get('title', '') or 'Updated' in body.get('content', '')