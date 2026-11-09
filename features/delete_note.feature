Feature: Удаление заметки

  Scenario: Удаление заметки по валидному ID
    Given я имею созданную заметку
    When я отправляю DELETE запрос на "/notes/{note_id:d}"
    Then статус ответа должен быть 200

  Scenario: Удаление заметки по невалидному ID
    When я отправляю DELETE запрос на "/notes/{note_id:d}"
    And параметр note_id равен 99999
    Then статус ответа должен быть 404