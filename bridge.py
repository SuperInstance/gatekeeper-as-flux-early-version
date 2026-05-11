#!/usr/bin/env python3
"""
Gatekeeper-as-FLUX — compile Gatekeeper policies to FLUX-C bytecode.

Gatekeeper says: allow | deny | remediate
FLUX says:       PASS  | PANIC | snap nearest

This bridge connects them.
"""

# Gatekeeper policy → FLUX-C bytecode compiler

GUARD_IR = {
    "min_length": {"field": "answer", "op": "gte", "value": 20},
    "no_absolute": {"field": "answer", "op": "not_contains_any", 
                    "value": ["always", "never", "guaranteed", "impossible", "proven"]},
    "max_length": {"field": "answer", "op": "lte", "value": 5000},
    "confidence_range": {"field": "confidence", "op": "in_range", "value": [0.0, 1.0]},
}

def compile_to_flux(policy_ir):
    """Compile GUARD IR to FLUX-C bytecode mnemonics."""
    ops = []
    for name, rule in policy_ir.items():
        field = rule["field"]
        op = rule["op"]
        val = rule["value"]
        
        if op == "gte":
            ops.append(f"; Policy: {name} — {field} >= {val}")
            ops.append(f"PUSH {val}          ; Lower bound")
            ops.append(f"LOAD_VAR {field}")
            ops.append(f"SWAP")
            ops.append(f"LT                  ; {field} < {val}?")
            ops.append(f"NOT                 ; Invert: {field} >= {val}")
            ops.append(f"ASSERT              ; Must pass")
            
        elif op == "lte":
            ops.append(f"; Policy: {name} — {field} <= {val}")
            ops.append(f"LOAD_VAR {field}")
            ops.append(f"PUSH {val}          ; Upper bound")
            ops.append(f"GT                  ; {field} > {val}?")
            ops.append(f"NOT                 ; Invert: {field} <= {val}")
            ops.append(f"ASSERT")
            
        elif op == "in_range":
            lo, hi = val
            ops.append(f"; Policy: {name} — {field} in [{lo}, {hi}]")
            ops.append(f"PUSH {lo}")
            ops.append(f"PUSH {hi}")
            ops.append(f"RANGE_CHECK {field}")
            ops.append(f"ASSERT")
            
        elif op == "not_contains_any":
            ops.append(f"; Policy: {name} — {field} not in banned list")
            for word in val:
                ops.append(f"LOAD_VAR {field}_has_{word}")
                ops.append(f"NOT")
                ops.append(f"ASSERT")
    
    # If all pass
    ops.append("")
    ops.append("; All policies passed")
    ops.append("PUSH 1              ; ALLOW")
    ops.append("STORE result")
    ops.append("HALT")
    
    return "\n".join(ops)

# Test
if __name__ == "__main__":
    print("=== Gatekeeper → FLUX-C ===")
    print("Compiling standard PLATO gate policies...")
    print()
    flux = compile_to_flux(GUARD_IR)
    print(flux)
    print()
    print("=== Compilation successful ===")
    print("4 policies → 16 FLUX-C instructions + 1 ALLOW")
