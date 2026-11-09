Feature: Редактирование заметки

  Scenario: Обновление заметки по валидному ID
    Given я имею созданную заметку
    When я отправляю PUT запрос на "/notes/{note_id:d}" с данными:
      | New Title | New Content      |
      | Updated   | Content modified |
    Then статус ответа должен быть 200
    And тело ответа содержит "Updated"

  Scenario: Обновление заметки по невалидному ID
    When я отправляю PUT запрос на "/notes/{note_id:d}"
    And параметр note_id равен 99999
    When я отправляю PUT запрос на "/notes/99999" с данными:
      | New Title | New Content |
      | Any       | Value       |
    Then статус ответа должен быть 404