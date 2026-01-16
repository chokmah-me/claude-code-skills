---
name: quantum-circuit-optimizer
description: Optimize quantum circuits by reducing gate count, depth, and identifying optimization opportunities. Use when user says "optimize quantum circuit", "reduce circuit depth", or "analyze quantum gates".
---

# Quantum Circuit Optimizer Skill


A concise description of what this skill does and its primary purpose.

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

When user requests this skill:

1. Perform the primary action
2. Report findings or results
3. Offer next steps or related actions

No additional parameters required.

## Examples

### Example 1: Quick Circuit Analysis
```bash
# User: "Analyze the quantum circuit in vqe_circuit.py"
grep -E "\.(cx|h|rz|ry)\(" vqe_circuit.py | wc -l
# Output: 127 gates found
```

### Example 2: Gate Count by Type
```bash
# User: "What gates are used most in this circuit?"
grep -oE "\.(cx|h|x|y|z|rx|ry|rz)\(" ansatz.py | sort | uniq -c | sort -rn
# Output:
#   45 .cx(
#   38 .ry(
#   22 .rz(
#   12 .h(
```

### Example 3: Optimization Opportunity Detection
```bash
# User: "Find optimization opportunities in quantum_algorithm.py"
grep -A 1 "\.h(" quantum_algorithm.py | grep "\.h("
# Output: Consecutive H gates on lines 89-90 (can be eliminated)
```

Results of the skill execution in a clear, actionable format.

## Important Notes

- **Framework-specific**: Optimization strategies vary by framework (Qiskit vs Cirq vs others)
- **Hardware constraints**: Real devices have limited gate sets and connectivity
- **Verification required**: Always verify optimized circuits maintain functional equivalence
- **Trade-offs**: Sometimes depth vs gate count requires balancing
- **Error mitigation**: Optimization can improve circuit fidelity on NISQ devices
- **Context matters**: VQE circuits optimize differently than QAOA or quantum simulation

## Best Practices

1. **Run before hardware execution** - Optimization reduces error accumulation
2. **Check basis gate set** - Ensure optimized circuit uses target hardware gates
3. **Verify circuit equivalence** - Use statevector simulation to verify correctness
4. **Consider noise model** - Some optimizations may not help on noisy devices
5. **Iterate** - Apply multiple optimization passes for best results
