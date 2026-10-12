from zkflow.protocols import schnorr

def test_schnorr_roundtrip():
    params = schnorr.generate_group()
    sk, pk = schnorr.keygen(params)
    proof = schnorr.prove(params, sk, "test")
    assert schnorr.verify(params, pk, proof, "test") is True

    # tamper with proof
    bad = dict(proof)
    bad['s'] = (bad['s'] + 1) % params['q']
    assert schnorr.verify(params, pk, bad, "test") is False
