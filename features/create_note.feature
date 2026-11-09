Feature: Создание заметки

  Scenario Outline: Успешное создание заметки с валидными данными
    Given я подготавливаю данные для создания заметки
    When я отправляю POST запрос на "/notes" с телом:
      | Title   | Content        |
      | <Title> | <Content>      |
    Then статус ответа должен быть 201
    And тело ответа содержит поле "title" со значением "<Title>"

    Examples:
      | Title    | Content           |
      | My Note  | Text text text    |
      | Another  | Some content here |

  Scenario: Создание заметки с невалидными данными (пустой заголовок)
    When я отправляю POST запрос на "/notes" с текстом:
      | Title | Content     |
      |       | Bad content |
    Then статус ответа должен быть 422