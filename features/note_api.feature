Feature: Note Management API
  As a user or client application
  I want to manage notes via REST API
  So that I can store, read, update, and delete information securely

  # --- СОЗДАНИЕ ЗАМЕТКИ ---
  Scenario: Successfully create a note with valid data
    Given I generate a valid note dataset
    When I send a request to create a note
    Then the response status code should be 200
    And the response should contain the correct title and content

  Scenario: Unsuccessfully create a note with invalid data
    Given I generate an invalid note dataset with "missing_title"
    When I send a request to create a note
    Then the response status code should be 422

  # --- ПОЛУЧЕНИЕ СПИСКА ЗАМЕТОК ---
  Scenario: Get note list when there are no notes
    Given the database is empty
    When I request the list of all notes
    Then the response status code should be 200
    And the response should be an empty list

  Scenario: Get note list when notes exist
    Given at least one note exists in the database
    When I request the list of all notes
    Then the response status code should be 200
    And the response should contain a non-empty list of notes

  # --- ПОЛУЧЕНИЕ ПО ID ---
  Scenario: Get a specific note by valid ID
    Given a note is freshly created and its ID is saved
    When I request the note by its valid ID
    Then the response status code should be 200
    And the response should match the created note data

  Scenario: Get a specific note by invalid ID
    Given an invalid note ID "9999"
    When I request the note by this ID
    Then the response status code should be 404

  # --- РЕДАКТИРОВАНИЕ ПО ID ---
  Scenario: Successfully update a note by valid ID
    Given a note is freshly created and its ID is saved
    And I generate a valid note dataset for update
    When I send a request to update this note
    Then the response status code should be 200
    And the response should contain updated title and content

  Scenario: Unsuccessfully update a non-existent note
    Given an invalid note ID "9999"
    And I generate a valid note dataset for update
    When I send a request to update this note
    Then the response status code should be 404

  # --- УДАЛЕНИЕ ПО ID ---
  Scenario: Successfully delete a note by valid ID
    Given a note is freshly created and its ID is saved
    When I send a request to delete this note
    Then the response status code should be 200
    And the response body detail should say "Note deleted"

  Scenario: Unsuccessfully delete a non-existent note
    Given an invalid note ID "9999"
    When I send a request to delete this note
    Then the response status code should be 404
