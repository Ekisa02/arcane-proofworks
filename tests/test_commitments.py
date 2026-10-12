from zkflow.protocols import commitments

def test_pedersen_commit_verify():
    p = 2 ** 61 - 1
    g, h = commitments.pedersen_generators(p)
    value = 12345
    c, r = commitments.pedersen_commit(p, g, h, value)
    assert commitments.pedersen_verify(p, g, h, value, r, c)
