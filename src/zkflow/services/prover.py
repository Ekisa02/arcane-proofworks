from ..protocols import schnorr

# Lightweight orchestration helpers (kept intentionally small and focused)

def client_side_schnorr_flow(secret: int, message: str = ""):
    params = schnorr.generate_group()
    x, y = schnorr.keygen(params)
    # In a real client flow, you would only keep x and publish y
    proof = schnorr.prove(params, secret, message)
    return {"params": params, "public_key": y, "proof": proof}
