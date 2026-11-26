# IT-қолдау өтінімдерін тіркеу жүйесі

Казахоязычный список заявок IT-поддержки с созданием, редактированием и удалением. Статус новой заявки — «Жаңа». Заголовок проверяется на сервере через `clean_title()`.

## Локальный запуск

Откройте PowerShell в папке, где лежит `manage.py` этого проекта. Требуется Python 3.13.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    $secret = .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
    (Get-Content .env).Replace('replace-with-a-generated-key', $secret) | Set-Content -Encoding Ascii .env
}
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8004
```

Откройте `http://127.0.0.1:8004/`. SQLite создаётся автоматически при миграции. Переменные процесса имеют приоритет над `.env`. Если в терминале уже задана переменная `DEBUG`, удалите её командой `Remove-Item Env:DEBUG`, чтобы использовать значение из файла.

Для установки демонстрационных записей в свежую базу и проверки проекта выполните:

```powershell
.\.venv\Scripts\python.exe manage.py loaddata demo
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

Для проверки журнала сохраните корректную заявку, затем отправьте форму с заголовком `abc` и заполненным описанием. В консоли появятся `INFO` с ID и `WARNING` для невалидной формы. Для эксперимента с хостом задайте `DEBUG=False` и `ALLOWED_HOSTS=localhost`, перезапустите сервер и выполните `curl.exe -i http://127.0.0.1:8004/`. Ожидаются HTTP 400 и `ERROR django.security.DisallowedHost`. Верните `ALLOWED_HOSTS=localhost,127.0.0.1`, перезапустите сервер и повторите запрос. Ожидается HTTP 200.

Если `127.0.0.1:8004` занят другим проектом, запустите сервер на `127.0.0.2:8004`. Для браузера можно временно добавить этот адрес в переменную текущего терминала через `$env:ALLOWED_HOSTS='localhost,127.0.0.1,127.0.0.2'`. Перед экспериментом с `.env` удалите это переопределение через `Remove-Item Env:ALLOWED_HOSTS` и используйте `curl.exe -i -H "Host: 127.0.0.1:8004" http://127.0.0.2:8004/`.

## GitHub

Создайте пустой репозиторий `django-lab12-tickets` на GitHub. Выполните команды в каталоге этого проекта.

```powershell
git init -b main
git add .
git status --short
git commit -m "Add Django lab 12 tickets project"
git remote add origin https://github.com/YOUR-LOGIN/django-lab12-tickets.git
git push -u origin main
```

Перед коммитом проверьте, что в списке нет `.env`, локальной базы, виртуального окружения и собранной статики. Корневой `.gitignore` исключает `warehouse/`, который публикуется из собственной папки.

## PostgreSQL и Render

1. В Render создайте PostgreSQL и скопируйте **Internal Database URL**. Разместите веб-сервис в том же аккаунте и регионе.
2. Создайте **Web Service**, подключите GitHub-репозиторий `django-lab12-tickets`, выберите ветку `main` и среду **Python 3**. Оставьте **Root Directory** пустым.
3. Укажите **Build Command** `bash build.sh`. Скрипт установит зависимости, соберёт статику и применит миграции.
4. Укажите **Start Command** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.
5. Добавьте значения из таблицы и запустите деплой. После успешной сборки откройте выданный HTTPS-адрес. Проверьте список и отправку формы, затем откройте **Logs** веб-сервиса и найдите запись приложения.

| Переменная | Локально | Render |
| --- | --- | --- |
| `SECRET_KEY` | Сгенерированное значение в `.env` | Отдельный секрет, можно сгенерировать в Render |
| `DEBUG` | `True` для разработки, `False` для эксперимента | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Домен сервиса добавляется автоматически, дополнительные домены перечисляются через запятую без схемы |
| `DATABASE_URL` | Не задана для SQLite | Internal Database URL выделенной PostgreSQL |
| `CSRF_TRUSTED_ORIGINS` | Обычно не задана | Для дополнительных доменов можно перечислить полные HTTPS-адреса через запятую |

Render задаёт `RENDER`, `RENDER_EXTERNAL_HOSTNAME` и `PORT` автоматически. В облачном режиме при `DEBUG=False` включены перенаправление на HTTPS, HSTS и флаги Secure для cookies. Публичный адрес предназначен для демонстрации с учебными данными, поскольку формы доступны посетителям без входа.

- [Документация Render по Django](https://render.com/docs/deploy-django)
- [Подключение к Render PostgreSQL](https://render.com/docs/postgresql-creating-connecting)
