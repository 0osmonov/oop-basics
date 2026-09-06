import redis
from django.conf import settings

CONFIRMATION_CODE_TTL = 5 * 60  # 5 минут
CONFIRMATION_CODE_PREFIX = 'confirmation_code:'


def get_redis_client():
    return redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )


def confirmation_key(email):
    return f'{CONFIRMATION_CODE_PREFIX}{email.lower()}'


def save_confirmation_code(email, code):
    client = get_redis_client()
    client.setex(confirmation_key(email), CONFIRMATION_CODE_TTL, code)


def get_confirmation_code(email):
    client = get_redis_client()
    return client.get(confirmation_key(email))


def delete_confirmation_code(email):
    client = get_redis_client()
    client.delete(confirmation_key(email))
