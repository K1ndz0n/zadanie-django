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

# Dokumentacja API - Zarządzanie zadaniami

## Logowanie

Endpoint: `POST /api/login/`

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin1", "password": "adminpassword"}'
```
Odpowiedź (token):
```json
{
  "token":"ea90d0e7ca358c9681aeabd181d22e9cbe7b2f16"
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
  "username": "nowyuser"
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
     -H "Authorization: Token 999cad5c35c88f63594536249b6cf57b07cd7716" \
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
     -H "Authorization: Token 999cad5c35c88f63594536249b6cf57b07cd7716" \
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



