Aplikacja działa w środowisku docker, w celu zbudowania oraz uruchomienia aplikacji należy w terminalu w głównym folderze projektu wpisać:

```bash
docker compose build
docker compose up
```

Aplikacja działa na 127.0.0.1:8000
Uruchomiony zostaje kontener zawierający aplikację oraz bazę danych w postgresie

  `login: admin, hasło: admin, nazwa bazy danych: postgres` - dane dostępu do bazy

Przy pierwszym uruchomieniu aplikacji zostaną utworzone 2 konta:

  `login: admin, hasło: admin - konto admina`
  
  `login: user, hasło: user - konto użytkownika`

# Dokumentacja API

## Logowanie

Endpoint: `POST /api/login/`

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
```
Odpowiedź (token):
```json
{
  "token":"<twoj_token>"
}
```

## Rejestracja

Endpoint:  `POST /api/register/`

```bash
curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "haslo123"}'
```
Odpowiedź:
```json
{
  "id": 5,
  "username": "testuser"
}
```

## Pobieranie listy użytkowników

Endpoint: `GET /api/user-list/`
```bash
curl http://localhost:8000/api/user-list/
```
Odpowiedź:
```json
[
  {"id": 1, "username": "admin1"},
  {"id": 2, "username": "user"}
]
```

## Tworzenie nowego zadania

Endpoint: `POST /api/task/create/`
Wymaga autoryzacji (token lub login + hasło)

```bash
curl -X POST http://localhost:8000/api/task/create/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token <twoj_token>" \
     -d '{"name": "Nowe zadanie", "description": "Opis zadania", "status": "new", "user_id": 1}'
```
Odpowiedź:
```json
{
  "task_id": 10,
  "name": "Nowe zadanie",
  "description": "Opis zadania",
  "status": "new",
  "user_id": 1
}
```

## Edycja zadania - cały rekord

Endpoint: `PUT /api/task/edit/<task_id>/`
Wymaga autoryzacji

```bash
curl -X PUT http://localhost:8000/api/task/edit/10/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token <twoj_token>" \
     -d '{"name": "Zaktualizowane zadanie", "description": "Nowy opis", "status": "in_progress", "user_id": 1}'
```
Odpowiedź:
```json
{
  "task_id": 10,
  "name": "Zaktualizowane zadanie",
  "description": "Nowy opis",
  "status": "in_progress",
  "user_id": 1
}
```

## Edycja zadania - wybrane dane

Endpoint: `PATCH /api/task/edit/<task_id>/`
Wymaga autoryzacji

```bash
curl -X PATCH http://localhost:8000/api/task/edit/10/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token <twoj_token>" \
     -d '{"name": "Zaktualizowane zadanie", "status": "in_progress"}'
```
Odpowiedź:
```json
{
  "task_id": 10,
  "name": "Zaktualizowane zadanie",
  "description": "Nowy opis",
  "status": "in_progress",
  "user_id": 1
}
```

## Usunięcie zadanie

Endpoint: `DELETE /api/task/edit/<task_id>/`
Wymaga autoryzacji oraz uprawnień admina

```bash
curl -X DELETE http://localhost:8000/api/task/edit/1/ \
  -H "Authorization: Token <twoj_token>"
```
Odpowiedź:
```json
{
    "message": "zadanie usunięte pomyślnie"
}
```

## Pobieranie szczegółów zadania

Endpoint: `GET /api/task/info/<task_id>/`

```bash
curl http://localhost:8000/api/task/info/10/
```
Odpowiedź:
```json
{
  "id": 10,
  "name": "Zaktualizowane zadanie",
  "description": "Nowy opis",
  "status": "in_progress",
  "user_id": 1,
  "username": "admin1"
}
```

## Lista zadadń z filtrowaniem

Endpoint: `GET /api/tasks/`

Przykład filtrowania po słowie w polach nazwa oraz opis:
```bash
curl http://localhost:8000/api/tasks/?search=gotowanie
```
Przykład filtrowania po id przypisanego użytkownika:
```bash
curl http://localhost:8000/api/tasks/?user_id=3
```
Odpowiedź
```json
[
  {
    "id": 1,
    "name": "Zadanie testowe",
    "description": "Opis testowy",
    "status": "new",
    "user_id": 3
  },
  {
    "id": 2,
    "name": "Drugie zadanie",
    "description": "Kolejny opis",
    "status": "new",
    "user_id": 3
  }
]
```

## Historia zmian z filtowaniem

Endpoint: `GET /api/history/`

Przykład filtrowania po dacie (zmiany przed następującą datą(RRRR-MM-DD)):
```bash
curl http://localhost:8000/api/history/?history_date_before=2025-01-01
```

Przykład filtrowania po dacie (zmiany po następującej dacie):
```bash
curl http://localhost:8000/api/history/?history_date_after=2025-01-01
```

Przykład filtrowania po dacie (zmiany wprowadzone podanego dnia):
```bash
curl http://localhost:8000/api/history/?history_date_at=2025-01-01
```
Przykłąd filtrowania po id zadania:
```bash
curl http://localhost:8000/api/history/?id=3
```

Odpowiedź będzie taka sama jak w poprzednim

