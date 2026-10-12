from ..utils.crypto import rand_range, int_to_bytes, sha256_int

# Pedersen commitments in the same multiplicative group as Schnorr

def pedersen_generators(p: int):
    # For demonstration we pick small, but fixed other generator
    # In practice choose generators with provable independence
    g = 2
    # h is derived by hashing g to produce another generator-ish element
    hv = sha256_int(int_to_bytes(p), b"pedersen-h") % p
    if hv == 0:
        hv = 3
    return g, hv


def pedersen_commit(p: int, g: int, h: int, value: int):
    # randomness r in [0, p-1]
    r = rand_range(1, p)
    commit = (pow(g, value, p) * pow(h, r, p)) % p
    return commit, r


def pedersen_verify(p: int, g: int, h: int, value: int, randomness: int, commitment: int):
    recomputed = (pow(g, value, p) * pow(h, randomness, p)) % p
    return recomputed == commitment
