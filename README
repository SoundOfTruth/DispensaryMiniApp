## Описание
ВКР mini app
## Стек технологий
- **Backend**: Python 3.13, FastAPI, SQLAlchemy, uv, pytest
- **Frontend**: Vue Js, Vue Router, Pinia
- **Контейнеризация**: Docker, Docker Compose
- **Web-сервер**: Nginx

### 1. Клонирование репозитория

```bash
git clone https://github.com/SoundOfTruth/DispensaryMiniApp.git
cd DispensaryMiniApp
```

### 2. Enviroment
Для запуска проекта необходимо создать и заполнить .env файл по примеру .env.example в папке infra-dev
При запуске проекта для production, нужно заполнить в папке infra .env и .env.cerbot по примеру .env.cerbot.example и выполнить скрипт
```bash
bash init_cert.sh
```

### 3. Запуск контейнеров

Запуск контейнеров для dev
```bash
cd infra-dev
docker compose -f docker-compose-dev.yml up -d
```

Запуск контейнеров для production
```bash
cd infra
docker compose up -d
```

### 4. Панель администратора
Для создание суперпользователя необходимо запустить скрипт
Для dev:
```bash
docker exec -it KOD-dev-backend bash
uv run createsuperuser
```
Для production:
```bash
docker exec -it KOD-backend bash
uv run createsuperuser
```
После нужно заполнить данные и выйти через Ctr + D
Панель администратора доступна по адресу /admin