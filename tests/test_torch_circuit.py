from zkflow.models.torch_circuit import ToyCircuit


def test_toy_circuit_evaluate_and_commit():
    tc = ToyCircuit(hidden_dim=4)
    out, commit, r = tc.evaluate_and_commit([0.1, 0.2, 0.3, 0.4])
    assert isinstance(out, list)
    assert isinstance(commit, int)
    assert isinstance(r, int)
