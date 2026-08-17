# Blog API — Контрольная работа №1

REST API для простого блога на Django и Django REST Framework.

## Как запустить

### 1. Установить зависимости

```bash
cd blog_api_project
pip install -r requirements.txt
```

### 2. Применить миграции

```bash
python manage.py migrate
```

### 3. Создать пользователя

```bash
python manage.py createsuperuser
```

### 4. Запустить сервер

```bash
python manage.py runserver
```

API доступно по адресу: `http://127.0.0.1:8000/api/v1/`

## Документация

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Аутентификация

Используется Token Authentication.

**Получить токен:**

```bash
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Использовать токен в запросах:**

```
Authorization: Token <your_token>
```

## API эндпоинты

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/v1/posts/` | Список постов (пагинация) | Гость — только опубликованные |
| POST | `/api/v1/posts/` | Создать пост | Только авторизованные |
| GET | `/api/v1/posts/{id}/` | Детали поста | Гость — только опубликованные |
| PUT/PATCH | `/api/v1/posts/{id}/` | Редактировать пост | Только автор поста |
| DELETE | `/api/v1/posts/{id}/` | Удалить пост | Только автор поста |
| GET | `/api/v1/posts/{id}/comments/` | Список комментариев | Гость — только одобренные |
| POST | `/api/v1/posts/{id}/comments/` | Добавить комментарий | Только авторизованные |
| PUT/PATCH | `/api/v1/comments/{id}/` | Редактировать комментарий | Только автор комментария |
| DELETE | `/api/v1/comments/{id}/` | Удалить комментарий | Только автор комментария |

## Модели

- **User** — стандартная модель Django (django.contrib.auth)
- **Post** — author, title, body, created_at, updated_at, is_published
- **Comment** — post, author, body, created_at, updated_at, is_approved

## Права доступа

- Гости могут только читать опубликованные посты
- Создавать посты и комментарии могут только авторизованные пользователи
- Редактировать и удалять посты/комментарии может только их автор
