from pydantic import BaseModel
from typing import Any, Dict, Optional

class KeygenResponse(BaseModel):
    p: int
    q: int
    g: int
    public_key: int

class SchnorrProveRequest(BaseModel):
    params: Dict[str, int]
    secret: int
    message: Optional[str] = ""

class SchnorrProof(BaseModel):
    t: int
    s: int
    c: int

class SchnorrVerifyRequest(BaseModel):
    params: Dict[str, int]
    public_key: int
    proof: SchnorrProof
    message: Optional[str] = ""

class PedersenCommitRequest(BaseModel):
    p: int
    g: int
    h: int
    value: int

class PedersenCommitResponse(BaseModel):
    commitment: int
    randomness: int

class TorchEvalRequest(BaseModel):
    input_vector: list
    params: Optional[Dict[str, Any]] = None

class TorchEvalResponse(BaseModel):
    output: list
    commitment: int
    randomness: int
