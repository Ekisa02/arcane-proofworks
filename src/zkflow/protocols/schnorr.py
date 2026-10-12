from typing import Dict, Tuple
from ..utils.crypto import sha256_int, rand_range, int_to_bytes
import secrets

# For clarity and reproducibility in examples, we use a standardized 2048-bit MODP group (RFC 3526 group 14) parameters.
# These are safe for demonstration. In production, use vetted crypto libraries.

RFC_2048_P = int(
    """
    FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
    29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
    EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
    E485B576 625E7EC6 F44C42E9 A63A3620 FFFFFFFF FFFFFFFF
    """.replace('\n', '').replace(' ', ''), 16)
# Choose q as (p-1)//2 for simplicity in demonstration (not a true subgroup order in general)

P = RFC_2048_P
Q = (P - 1) // 2
G = 2


def generate_group() -> Dict[str, int]:
    return {"p": P, "q": Q, "g": G}


def keygen(params: Dict[str, int]) -> Tuple[int, int]:
    p = params['p']
    q = params['q']
    g = params['g']
    # secret x in [1, q-1]
    x = rand_range(1, q)
    y = pow(g, x, p)
    return x, y


def prove(params: Dict[str, int], secret: int, message: str = "") -> Dict[str, int]:
    p = params['p']
    q = params['q']
    g = params['g']
    y = pow(g, secret, p)
    # random nonce r
    r = rand_range(1, q)
    t = pow(g, r, p)
    # compute challenge c = H(g || y || t || m) mod q
    c = sha256_int(int_to_bytes(g), int_to_bytes(y), int_to_bytes(t), message.encode('utf-8')) % q
    s = (r + c * secret) % q
    return {"t": t, "s": s, "c": c}


def verify(params: Dict[str, int], public_key: int, proof: Dict[str, int], message: str = "") -> bool:
    p = params['p']
    q = params['q']
    g = params['g']
    t = proof['t']
    s = proof['s']
    c = proof['c']
    # recompute challenge to guard against tampering
    c_check = sha256_int(int_to_bytes(g), int_to_bytes(public_key), int_to_bytes(t), message.encode('utf-8')) % q
    if c_check != c:
        return False
    left = pow(g, s, p)
    right = (t * pow(public_key, c, p)) % p
    return left == right
