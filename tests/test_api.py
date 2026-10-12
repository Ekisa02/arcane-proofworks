from fastapi.testclient import TestClient
from zkflow.app import app

client = TestClient(app)


def test_schnorr_keygen_and_prove_verify():
    r = client.post('/schnorr/keygen')
    assert r.status_code == 200
    data = r.json()
    assert 'p' in data and 'g' in data and 'public_key' in data

    # For testing, we do a local keygen/prove using the same params with the library to avoid transmitting secrets
    # But we'll call the API prove endpoint to ensure request parsing works
    from zkflow.protocols import schnorr
    params = schnorr.generate_group()
    sk, pk = schnorr.keygen(params)
    prove_payload = {"params": params, "secret": sk, "message": "api-test"}
    pr = client.post('/schnorr/prove', json=prove_payload)
    assert pr.status_code == 200
    proof = pr.json()
    verify_payload = {"params": params, "public_key": pk, "proof": proof, "message": "api-test"}
    vr = client.post('/schnorr/verify', json=verify_payload)
    assert vr.status_code == 200
    assert vr.json().get('valid') is True


def test_torch_eval():
    r = client.post('/torch/evaluate', json={"input_vector": [0.1, 0.2, 0.3, 0.4]})
    assert r.status_code == 200
    data = r.json()
    assert 'output' in data and 'commitment' in data and 'randomness' in data
