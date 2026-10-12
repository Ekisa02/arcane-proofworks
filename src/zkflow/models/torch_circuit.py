from typing import Tuple, List
import torch
from ..protocols.commitments import pedersen_generators, pedersen_commit

class ToyCircuit:
    """
    Toy PyTorch-backed "circuit" demonstrating batch witness processing and a simple commitment over outputs.

    This is a pedagogical component showing how tensors can be used to compute witnesses and fold them
    into a commitment-friendly representation. It is NOT a real zero-knowledge construction.
    """

    def __init__(self, hidden_dim: int = 8):
        # Simple one-hidden-layer MLP with fixed seeded weights for reproducibility
        torch.manual_seed(0)
        self.W1 = torch.randn((hidden_dim, hidden_dim)) * 0.1
        self.b1 = torch.randn((hidden_dim,)) * 0.1
        self.W2 = torch.randn((hidden_dim, 1)) * 0.1
        self.b2 = torch.randn((1,)) * 0.1

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.float()
        h = torch.relu(x @ self.W1.T + self.b1)
        out = (h @ self.W2) + self.b2
        return out.squeeze(-1)

    def evaluate_and_commit(self, input_vector: List[float]) -> Tuple[List[float], int, int]:
        # convert input to tensor
        x = torch.tensor(input_vector).unsqueeze(0)  # treat as batch of 1
        out = self.forward(x)
        # produce small integer output by hashing floating output
        out_bytes = str(out.tolist()).encode('utf-8')
        # simple folding into integer (pedagogical only)
        value = abs(hash(out_bytes)) % (2 ** 32)
        # use pedersen over a moderate prime to provide a commitment
        # choose a small prime for demonstration
        p = 2 ** 61 - 1
        g, h = pedersen_generators(p)
        commit, r = pedersen_commit(p, g, h, value)
        return out.tolist(), int(commit), int(r)
