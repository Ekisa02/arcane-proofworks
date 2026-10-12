# Arcane Proofworks

Arcane Proofworks is a modular Python project providing educational implementations of zero-knowledge primitives (Schnorr sigma-protocol and Pedersen commitments) and a small PyTorch-backed toy "circuit" evaluator to demonstrate how a ZK-enabled service can be structured. The project exposes a FastAPI HTTP API for interactive experimentation, includes tests, and follows best-practices for a multi-module Python repository.

This repository is intended for learning, prototyping, and research. The cryptographic primitives are implemented in an approachable style for clarity and teaching; do not use this repository as-is for production or sensitive secrets without appropriate review and hardened cryptographic libraries.

Highlights

- Schnorr proof-of-knowledge (discrete-log) primitive with keygen/prove/verify flows
- Pedersen commitments (commit and verify)
- PyTorch toy "circuit" evaluator (vectorized witness/commit operations using torch tensors)
- FastAPI service exposing endpoints to interact with primitives
- Well-structured Python package layout with unit tests and API examples

Repository architecture

- src/zkflow/: main python package
  - api/: FastAPI routes and schemas
  - protocols/: implementations of Schnorr and Pedersen primitives
  - models/: PyTorch-backed toy circuit model and helpers
  - services/: higher-level prover/verification orchestration
  - utils/: helper crypto utilities
- tests/: pytest-based unit tests and API tests

Installation

Prerequisites

- Python 3.9+
- pip

Install from source (recommended to use a virtual environment):

1) Create and activate a virtualenv

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the FastAPI service (development)

```bash
uvicorn zkflow.app:app --reload
```

By default the server will be available at http://127.0.0.1:8000. Open http://127.0.0.1:8000/docs for the interactive OpenAPI UI.

Usage examples

Schnorr keygen (curl):

```bash
curl -s -X POST "http://127.0.0.1:8000/schnorr/keygen" -H "Content-Type: application/json" | jq
```

Prove knowledge of the private key (example):

```bash
# Keygen response contains: p, q, g, public_key
# For demonstration only: you can POST the secret back to the API to create a proof
# In practice, proving happens client-side and the secret is never sent to a server.
curl -s -X POST "http://127.0.0.1:8000/schnorr/prove" -H "Content-Type: application/json" \
  -d '{"params": {"p": <p>, "q": <q>, "g": <g>, "public_key": <y>}, "secret": <x>, "message": "demo"}'
```

See the API Swagger UI for request/response schemas and examples.

Testing

Run the test suite with pytest:

```bash
pytest -q
```

Notes and Safety

- Implementations are for educational/prototyping use. For production, use vetted libraries (e.g., libsecp256k1, pyca/cryptography, zk frameworks such as zkSync/halo2, bellman, etc.).
- The PyTorch module demonstrates vectorized witness computation and commitment-style interactions — it is not a complete ZK proof system.

Contributing

Contributions that add more primitives, stronger tests, integration with real curve libraries, or clearer pedagogical docs are welcome. Please open issues or PRs with design rationale.
