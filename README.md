<div align="center">

# Filesave Server #

**Открытый проект простого сервера для сохранения файлов.**

![commits](https://img.shields.io/github/commit-activity/t/SaySmokeGraf/filesave_server?logo=github&label=commits&color=blue)
![commit activity](https://img.shields.io/github/commit-activity/w/SaySmokeGraf/filesave_server?logo=github&label=commit%20activity&color=blue)
![last commit](https://img.shields.io/github/last-commit/SaySmokeGraf/filesave_server?logo=github&label=last%20commit&color=blue)
![release](https://img.shields.io/github/v/release/SaySmokeGraf/filesave_server?logo=github&label=release&color=blue)

![contributors](https://img.shields.io/github/contributors/SaySmokeGraf/filesave_server?logo=github&color=green)
[![backender](https://img.shields.io/badge/backender-SaySmokeGraf-green?logo=python)](https://github.com/SaySmokeGraf/)
[![frontender](https://img.shields.io/badge/frontender-Tanrari-green?logo=javascript)](https://github.com/Tanrari/)

![Python](https://img.shields.io/badge/Python-black?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-black?logo=fastapi)
![JavaScript](https://img.shields.io/badge/JavaScript-black?logo=javascript)
![CSS](https://img.shields.io/badge/CSS-black?logo=css)
![HTML](https://img.shields.io/badge/HTML-black?logo=html5)

</div>

## О проекте ##

Данный проект сервера для сохранения файлов предназначен для
самостоятельной развертки на удобной платформе и личного использования.

## Функционал ##

### Бэкенд ###

Пишется на Python + FastAPI, БД - SQLite.

- Корень - перенаправляет на статические файлы фронтенда.
- Файловое API - для взаимодействия с файлами пользователя. Требуют
    токена.
- API аутентификации-авторизации - для входа на сервис. Возвращают
    JWT-токен. Содержат зависимости, используемые в файловом API для
    проверки токена.
- Модерирование новых пользователей (в разработке)

### Фронтенд ###

Пишется на JavaScript + CSS + HTML.

- Страница с файловым менеджером - содержит базовый необходимый
    функционал для загрузки/скачивания/удаления файлов.
- Страница для входа (регистрация - в разработке).
- Сохранение токена в куки.
- Редиректы, прогрессбары и уведомления для пользователя, связанные с
    его действиями и ответами от сервера.

### Связь бэкенда и фронтенда ###

На данный момент представляет собой монолит (по техническим причинам),
в дальнейшем планируется перенос в микросервисную архитектуру в
отдельных Docker-контейнерах.

### Документация ###

Стандартная OpenAPI (Swagger) документация от FastAPI при запущенном
сервере.

## Использование ##

### Зависимости ###

- Python 3.10+
- Библиотеки из requirements.txt

### Порядок ###

1. Расположить папку с проектом в удобном месте.
2. Настроить константы в конфиг-файлах под нужды.
3. Сгененрировать и расположить по местам секретные ключи.
4. Запустить из корневой папки командой `fastapi run`.
5. Использовать в браузере по адресу `http://<ip>:8000/`, где ip - либо
    `localhost` для доступа с того же устройства, либо IP сервера в
    локальной сети.

### Конфиг файлы ###

- `app/config.py` - конфиг главного приложения. Изменение пользователем
    не предполагается.

- `app/api/auth/managers/config.py` - конфиг для классов-менеджеров для
    аутентификации и авторизации. Константы для настройки:

    - `PATH_SECRET_USERS` - путь до секретного ключа для JWT-токенов.
        Важно строго создать этот путь заранее и расположить ключ для
        правильного функционирования.

    - `ACCESS_TOKEN_EXPIRE_DAYS`, `ACCESS_TOKEN_EXPIRE_MINUTES` - время
        истечения токена: дни и минуты соответственно. В создании токена
        используется их сумма. Константы две для большей гибкости
        настройки на стадии разработки.

- `app/api/auth/managers/dbmanager/config.py` - конфиг для менеджера БД
    пользователей. Константы для настройки:

    - `PATH_DB_DIR` - путь до папки с БД пользователей. Саму БД и папку
        (как и папки по пути) создавать не обязательно: предусмотрено
        автоматическое создание всего пути и БД с нужными таблицами при
        отсутствии онных.

- `app/api/files/config.py` - конфиг для файлового API. Константы для
    настройки:

    - `PATH_STORAGE` - путь до хранилища файлов пользователей. Папку
        (как и папки по пути) создавать не обязательно: предусмотрено
        автоматическое создание всего пути.

    - `PATH_DISK` - диск, на котором расположено хранилище. Нужно для
        проверки свободного места.

    - `RESERVED_DISK_SPACE` - зарезервированное место на диске в байтах.
        Это место предполагается свободным от файлов пользователей.

    