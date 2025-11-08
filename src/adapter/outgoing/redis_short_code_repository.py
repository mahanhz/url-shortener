import random
import string

from src.adapter.outgoing.database import redis_client
from src.application.port.outgoing.short_code_repository import ShortCodeRepository

BASE = 62
# Base62 alphabet (0-9, a-z, A-Z)
BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


class RedisShortCodeRepository(ShortCodeRepository):
    async def short_code(self) -> str:
        counter = redis_client.incr("short_code_counter")
        return base62_short_code(counter)


def base62_short_code(counter: int) -> str:
    # Convert counter to Base62
    base62_id = encode_base62(counter)

    # If shorter than 8 chars, pad with random Base62 chars on the left (or right)
    if len(base62_id) < 8:
        pad_length = 8 - len(base62_id)
        random_padding = "".join(random.choices(BASE62_ALPHABET, k=pad_length))
        base62_id = base62_id + random_padding  # pad on right if preferred

    # Pad with leading zeros (or '0' in Base62 alphabet) to ensure 8 chars
    return base62_id


def encode_base62(num: int) -> str:
    """Encodes a given integer ``num``."""

    chs = []
    while num > 0:
        num, r = divmod(num, BASE)
        chs.insert(0, BASE62_ALPHABET[r])

    if not chs:
        return "0"

    return "".join(chs)
