from fastapi import APIRouter
from .schemas import *
from ..protocols import schnorr, commitments
from ..models.torch_circuit import ToyCircuit

router = APIRouter()

@router.post('/schnorr/keygen', response_model=KeygenResponse)
def schnorr_keygen():
    params = schnorr.generate_group()
    sk, pk = schnorr.keygen(params)
    return {"p": params['p'], "q": params['q'], "g": params['g'], "public_key": pk}

@router.post('/schnorr/prove', response_model=SchnorrProof)
def schnorr_prove(req: SchnorrProveRequest):
    params = req.params
    secret = req.secret
    msg = req.message or ""
    proof = schnorr.prove(params, secret, msg)
    return proof

@router.post('/schnorr/verify')
def schnorr_verify(req: SchnorrVerifyRequest):
    ok = schnorr.verify(req.params, req.public_key, req.proof, req.message or "")
    return {"valid": ok}

@router.post('/pedersen/commit', response_model=PedersenCommitResponse)
def pedersen_commit(req: PedersenCommitRequest):
    commit, r = commitments.pedersen_commit(req.p, req.g, req.h, req.value)
    return {"commitment": commit, "randomness": r}

@router.post('/torch/evaluate', response_model=TorchEvalResponse)
def torch_evaluate(req: TorchEvalRequest):
    tc = ToyCircuit()
    output, commitment, randomness = tc.evaluate_and_commit(req.input_vector)
    return {"output": output, "commitment": commitment, "randomness": randomness}
