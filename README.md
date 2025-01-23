# web-addlist-mikrotik
Web Add Adress list Mikrotik

![Screenshot_2025_01_23-2](https://github.com/user-attachments/assets/d026791c-b004-4ca3-99de-2ee2bc04f4be)


Этот проект представляет собой систему для добавления доменов в список адресов MikroTik через API. Состоит из фронтенда (HTML + JavaScript) и бэкенда на Python (Flask). Также используется SSH для выполнения команд на MikroTik.

## Требования

- MikroTik с настроенным доступом по SSH
- Docker (для запуска бэкенда)
- Python 3.11 (если запускать бэкенд локально)

## Установка и запуск

### 1. Настройка MikroTik
Убедитесь, что на MikroTik настроен доступ по SSH:

1. Разрешите доступ по SSH.
2. Создайте пользователя с правами `full` для подключения из бэкенда.
3. Убедитесь, что список `whitelist` существует или создаётся автоматически при добавлении доменов.

### 2. Настройка бэкенда

#### Запуск через Docker
1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/FoxGD3D/web-addlist-mikrotik.git
    cd web-addlist-mikrotik/backend
    ```
    1.1 Добавте свои значения:
   ```bash
    nano app.py
    ```
   ```bash
   Замените на свои значения
       MIKROTIK_HOST = "Enter-Mikrotik-IP"
       MIKROTIK_USER = Enter-Mikrotik-USER"
       MIKROTIK_PASSWORD = "Enter-Mikrotik-PASS"
    ```
   Так же введите имя списка:
    ```bash
   <LIST-NAME>
    ```

3. Соберите Docker-образ:
    ```bash
    docker build -t flask-backend .
    ```

4. Запустите контейнер:
    ```bash
    docker run -d -p 5001:5001 flask-backend
    ```

#### Локальный запуск
1. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. Запустите сервер:
    ```bash
    python app.py
    ```

### 3. Настройка фронтенда
1. Поместите содержимое `index.html` на хостинг, например, в папку `/var/www/html` или в директорию панели управления (например, BrainyCP).

2. Убедитесь, что в `index.html` правильно указан URL бэкенда:
    ```javascript
    fetch('http://<IP_адрес_бэкенда>:5001/api/unlock', {
    ```

### 4. Проверка работы
1. Откройте фронтенд в браузере.
2. Введите домен в поле и нажмите "Добавить".
3. Если всё настроено правильно, вы увидите сообщение об успешном добавлении домена.

## Структура проекта

```
.
├── backend              # Бэкенд
│   ├── app.py           # Код бэкенда на Flask
│   ├── requirements.txt # Зависимости Python
├── frontend             # Фронтенд
│   ├── index.html       # Код фронтенда
├── README.md            # Документация
```

## API

### POST /api/unlock
Добавляет домен в список `whitelist` на MikroTik.

**Параметры:**
- `domain` (строка): Домен, который нужно добавить.

**Пример запроса:**
```bash
curl -X POST http://<IP_адрес_бэкенда>:5001/api/unlock \
    -H "Content-Type: application/json" \
    -d '{"domain": "example.com"}'
```

**Пример ответа:**
```json
{
    "message": "Домен example.com успешно добавлен в whitelist"
}
```

**Ошибки:**
- `Ошибка при подключении`: Проблемы с подключением к MikroTik.
- `Ошибка выполнения команды`: Ошибка выполнения команды на MikroTik.

## Лицензия
Проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

## Авторы
- [FoxGD3D](https://github.com/FoxGD3D)

