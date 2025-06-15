Aplikacja działa w środowisku docker, w celu zbudowania oraz uruchomienia aplikacji należy w terminalu w głównym folderze projektu wpisać:
  `docker compose build`
  
  `docker compose up`

Aplikacja działa na 127.0.0.1:8000
Uruchomiony zostaje kontener zawierający aplikację oraz bazę danych w postgresie

  `login: admin, hasło: admin, nazwa bazy danych: postgres` - dane dostępu do bazy

Przy pierwszym uruchomieniu aplikacji zostaną utworzone 2 konta:

  `login: admin, hasło: admin - konto admina`
  
  `login: user, hasło: user - konto użytkownika`

# Dokumentacja API - Zarządzanie zadaniami

## Logowanie (pobranie tokena)

Endpoint: `POST /api/login/`

Wysyłamy JSON z danymi:

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin1", "password": "adminpassword"}'
```
Przykładowa odpowiedź:
```json
{"token":"ea90d0e7ca358c9681aeabd181d22e9cbe7b2f16"}
```

    


