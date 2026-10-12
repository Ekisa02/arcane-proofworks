import hashlib
import secrets
from typing import Tuple

def sha256_int(*parts: bytes) -> int:
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return int.from_bytes(h.digest(), 'big')

def rand_bits(nbits: int = 256) -> int:
    return secrets.randbits(nbits)

def rand_range(low: int, high: int) -> int:
    # inclusive low, exclusive high
    width = high - low
    r = secrets.randbelow(width) + low
    return r

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')
