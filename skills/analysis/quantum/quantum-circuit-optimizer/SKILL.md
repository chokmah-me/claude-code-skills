---
name: quantum-circuit-optimizer
description: Optimize quantum circuits by reducing gate count, depth, and identifying optimization opportunities. Use when user says "optimize quantum circuit", "reduce circuit depth", or "analyze quantum gates".
---

# Quantum Circuit Optimizer Skill

## Purpose
Analyze and optimize quantum circuits to reduce gate count, circuit depth, and identify optimization opportunities without executing full simulation (~800 tokens).

## Instructions

When user requests quantum circuit optimization:

1. **Identify quantum circuit files** (`.qasm`, `.py` with Qiskit/Cirq, `.q`)
2. **Run analysis commands** to extract circuit metrics
3. **Present optimization summary** showing:
   - Current gate count and depth
   - Identified optimization opportunities
   - Recommended transformations
4. **Offer**: "Want me to apply optimizations or generate optimized circuit code?"

## Commands

### Qiskit Circuit Analysis
```bash
# Find Qiskit circuits
find . -name "*.py" -exec grep -l "QuantumCircuit\|qiskit" {} \; | head -10

# Extract circuit operations
grep -E "(\.cx\(|\.h\(|\.x\(|\.rz\(|\.measure\(|\.barrier\()" quantum_file.py | head -30

# Count gate types
grep -oE "\.(cx|h|x|y|z|rx|ry|rz|swap|ccx|measure)\(" quantum_file.py | sort | uniq -c
```

### Cirq Circuit Analysis
```bash
# Find Cirq circuits
find . -name "*.py" -exec grep -l "cirq\|Circuit" {} \; | head -10

# Extract operations
grep -E "(CNOT|H|X|Y|Z|Rx|Ry|Rz|SWAP|measure)" quantum_file.py | head -30
```

### QASM Analysis
```bash
# Find QASM files
find . -name "*.qasm" | head -10

# Count gates in QASM
grep -E "^(cx|h|x|y|z|rx|ry|rz|swap|measure)" circuit.qasm | wc -l

# Extract gate sequence
grep -vE "^(OPENQASM|include|qreg|creg|//))" circuit.qasm | grep -E "[a-z]"
```

## Output Format

```
Quantum Circuit Analysis:

📊 Circuit Metrics:
   - Total Gates: 47
   - Circuit Depth: 23
   - Qubit Count: 5
   - Two-Qubit Gates (CNOT/CX): 18
   - Single-Qubit Gates: 29

🔍 Optimization Opportunities:
   1. Consecutive H gates detected (lines 45-47) → Can be eliminated
   2. CNOT chains found → Candidate for gate synthesis
   3. Redundant rotations: Rz(θ)Rz(φ) → Rz(θ+φ)
   4. 3 barriers detected → Consider removing for optimization

✅ Recommended Actions:
   - Apply gate cancellation rules
   - Use transpiler optimization level 3
   - Consider ZX-calculus simplification
   - Estimated reduction: 35% gates, 40% depth
```

## Framework Detection

**Qiskit (Python)**:
- `from qiskit import QuantumCircuit`
- `.cx()`, `.h()`, `.measure()`
- `.transpile()`, `.optimize()`

**Cirq (Python)**:
- `import cirq`
- `cirq.Circuit()`, `cirq.CNOT`, `cirq.H`
- `cirq.optimize_for_target_gateset()`

**QASM (OpenQASM)**:
- `.qasm` files
- `cx q[0],q[1];`
- `h q[0];`

**PennyLane**:
- `@qml.qnode`
- `qml.CNOT`, `qml.Hadamard`

**Quil (Rigetti)**:
- `.quil` files
- `CNOT 0 1`, `H 0`

## Optimization Techniques Identified

### Gate Cancellation
- Consecutive H gates: H·H = I
- X·X = I, Y·Y = I, Z·Z = I
- CNOT·CNOT = I (same control/target)

### Gate Fusion
- Rz(θ)·Rz(φ) = Rz(θ+φ)
- Adjacent single-qubit rotations
- U3 gate synthesis

### Circuit Rewriting
- Commutation rules (move gates through circuit)
- ZX-calculus simplification
- Clifford+T optimization

### Topology Optimization
- Reduce SWAP gates for device topology
- Qubit mapping optimization
- Route optimization for connectivity constraints

## Use Cases

- Pre-compilation circuit optimization
- Reducing gate count for NISQ devices
- Identifying redundant operations
- Preparing circuits for hardware execution
- Estimating circuit fidelity improvements
- Comparing circuit implementations
- Educational: understanding circuit transformations

## Limitations

⚠️ **May miss**:
- Dynamic circuits (runtime-dependent gates)
- Parameterized circuits with symbolic parameters
- Circuit optimizations requiring matrix decomposition
- Hardware-specific compiler optimizations
- Noise-aware optimizations

For comprehensive optimization, suggest:
```python
# Qiskit
from qiskit import transpile
optimized = transpile(circuit, optimization_level=3)

# Cirq
import cirq
optimized = cirq.optimize_for_target_gateset(circuit)

# Analysis
print(f"Original: {len(circuit)} gates, depth {circuit.depth()}")
print(f"Optimized: {len(optimized)} gates, depth {optimized.depth()}")
```

## Follow-Up Actions

After circuit analysis, Claude can:
- Generate optimized circuit code
- Apply specific transformation rules
- Create visualization of optimization impact
- Suggest hardware-specific optimizations
- Estimate error reduction from optimization
- Compare multiple optimization strategies
- Generate decomposition for target gate set

## Integration with Other Skills

Works well with:
- **dependency-audit**: Check quantum library versions
- **dead-code-hunter**: Find unused quantum functions
- **quick-test-runner**: Run quantum circuit tests
- **repo-briefing**: Understand quantum project structure

## Token Efficiency

- ~800 tokens for circuit analysis and optimization suggestions
- Alternative: full circuit simulation (15k+ tokens)
- Alternative: reading all quantum files (10k+ tokens)
- 95% reduction in optimization analysis cost
- Enables quick feedback loop for circuit improvement

## Advanced Configuration

### Custom Gate Pattern Detection
```bash
# Find custom gate definitions
grep -E "def.*gate|@quantum_gate" *.py

# Detect parameterized circuits
grep -E "Parameter|ParameterVector" *.py
```

### Optimization Level Analysis
```python
# Compare optimization levels (Qiskit)
for level in [0, 1, 2, 3]:
    opt = transpile(circuit, optimization_level=level)
    print(f"Level {level}: {len(opt)} gates, depth {opt.depth()}")
```

### Hardware-Specific Metrics
```bash
# Check basis gate usage
grep -E "(basis_gates|coupling_map)" *.py

# SWAP gate analysis for topology
grep -E "\.swap\(|SWAP" *.py | wc -l
```

## Best Practices

1. **Run before hardware execution** - Optimization reduces error accumulation
2. **Check basis gate set** - Ensure optimized circuit uses target hardware gates
3. **Verify circuit equivalence** - Use statevector simulation to verify correctness
4. **Consider noise model** - Some optimizations may not help on noisy devices
5. **Iterate** - Apply multiple optimization passes for best results

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

## Important Notes

- **Framework-specific**: Optimization strategies vary by framework (Qiskit vs Cirq vs others)
- **Hardware constraints**: Real devices have limited gate sets and connectivity
- **Verification required**: Always verify optimized circuits maintain functional equivalence
- **Trade-offs**: Sometimes depth vs gate count requires balancing
- **Error mitigation**: Optimization can improve circuit fidelity on NISQ devices
- **Context matters**: VQE circuits optimize differently than QAOA or quantum simulation
