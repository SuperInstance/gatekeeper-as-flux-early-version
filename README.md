# Gatekeeper-as-FLUX

> Bridge between Oracle1's Gatekeeper policies and FM's FLUX-C bytecode.

Compiles PLATO gate policies to FLUX-C directly. 4 standard policies → 16 instructions + ALLOW.

## Usage
```python
python3 bridge.py
```

## How it works
- Gatekeeper: `allow | deny | remediate`
- FLUX-C: `PASS | PANIC | snap nearest`
- Bridge: Policy IR → FLUX-C opcodes

See research/GATEKEEPER-AS-FLUX-MESH.md for the full architecture.
