# Quantum Circuit Optimizer

A Claude Code skill for analyzing and optimizing quantum circuits across multiple frameworks (Qiskit, Cirq, QASM, PennyLane, Quil).

## Overview

This skill helps you quickly analyze quantum circuits to identify optimization opportunities without running full simulations. It provides gate count analysis, depth metrics, and specific recommendations for reducing circuit complexity.

## Supported Frameworks

- **Qiskit** (Python) - IBM's quantum computing framework
- **Cirq** (Python) - Google's quantum computing framework
- **OpenQASM** - Open Quantum Assembly Language
- **PennyLane** - Quantum machine learning framework
- **Quil** - Rigetti's quantum instruction language

## What It Does

1. **Finds quantum circuit files** in your codebase
2. **Extracts gate operations** and circuit structure
3. **Counts gates by type** (CNOT, Hadamard, rotations, etc.)
4. **Identifies optimization opportunities**:
   - Gate cancellations (H·H = I, X·X = I, etc.)
   - Gate fusions (Rz(θ)·Rz(φ) = Rz(θ+φ))
   - Redundant barriers
   - CNOT chains for synthesis
5. **Estimates optimization impact** on gate count and depth

## Quick Start

### Example 1: Analyze a Qiskit Circuit

```python
# Your quantum_algorithm.py
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.h(0)  # Redundant - cancels with previous H
qc.cx(0, 1)
qc.cx(0, 1)  # Redundant - cancels with previous CNOT
qc.rz(0.5, 2)
qc.rz(0.3, 2)  # Can be fused into single Rz(0.8)
```

**Usage**: "Analyze quantum_algorithm.py for optimization opportunities"

**Output**:
```
Quantum Circuit Analysis:

📊 Circuit Metrics:
   - Total Gates: 6
   - Two-Qubit Gates: 2
   - Single-Qubit Gates: 4

🔍 Optimization Opportunities:
   1. Consecutive H gates (lines 4-5) → Can be eliminated
   2. Consecutive CNOT gates (lines 6-7) → Can be eliminated
   3. Consecutive Rz gates (lines 8-9) → Can be fused to Rz(0.8)

✅ Recommended Actions:
   - Apply gate cancellation rules
   - Estimated reduction: 67% gates (6 → 2)
```

### Example 2: Compare Optimization Levels

"Show me the effect of different Qiskit optimization levels on my circuit"

The skill will help you run:
```python
from qiskit import transpile

for level in [0, 1, 2, 3]:
    opt = transpile(circuit, optimization_level=level)
    print(f"Level {level}: {len(opt)} gates, depth {opt.depth()}")
```

### Example 3: Analyze QASM File

```bash
# Given a circuit.qasm file
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
cx q[0],q[1];
cx q[1],q[2];
measure q -> c;
```

**Usage**: "Analyze circuit.qasm"

**Output**: Gate count, depth analysis, and CNOT chain optimization suggestions

## Optimization Techniques Covered

### Gate Cancellation
- **Pauli gates**: X·X = I, Y·Y = I, Z·Z = I
- **Hadamard**: H·H = I
- **CNOT**: CNOT(a,b)·CNOT(a,b) = I
- **Inverse gates**: U·U† = I

### Gate Fusion
- **Rotation merging**: Rz(θ)·Rz(φ) = Rz(θ+φ)
- **Single-qubit optimization**: Multiple rotations → U3 gate
- **Clifford simplification**: Reduce Clifford circuits

### Circuit Rewriting
- **Commutation rules**: Reorder gates using commutativity
- **ZX-calculus**: Graphical circuit simplification
- **Clifford+T decomposition**: Optimize for fault-tolerant gates

### Topology Optimization
- **SWAP reduction**: Minimize SWAP gates for device topology
- **Qubit mapping**: Optimize qubit allocation for hardware
- **Route optimization**: Minimize overhead from limited connectivity

## Token Efficiency

- **~800 tokens** for complete analysis
- **Alternative approach**: Full circuit simulation uses 15k+ tokens
- **Savings**: 95% reduction in analysis cost

This enables rapid iteration on quantum algorithm design without expensive simulation runs.

## Integration with Other Skills

Works well with:
- `dependency-audit` - Check quantum library versions and compatibility
- `dead-code-hunter` - Find unused quantum functions
- `quick-test-runner` - Run quantum circuit unit tests
- `repo-briefing` - Understand quantum project structure

## Use Cases

### Algorithm Development
- Optimize VQE ansätze for molecular simulation
- Reduce QAOA circuit depth for combinatorial optimization
- Minimize error accumulation in NISQ algorithms

### Hardware Preparation
- Prepare circuits for specific device topologies
- Reduce gate count to fit within coherence time
- Optimize for native gate sets

### Research & Education
- Compare circuit implementations
- Understand circuit transformation effects
- Learn optimization techniques

### Performance Analysis
- Estimate fidelity improvements from optimization
- Compare optimization strategies
- Identify algorithmic bottlenecks

## Best Practices

1. **Run before hardware execution** - Optimization reduces error accumulation on NISQ devices
2. **Verify equivalence** - Use statevector simulation to confirm optimized circuits are functionally equivalent
3. **Consider noise models** - Some optimizations may not help on noisy devices
4. **Check basis gates** - Ensure optimized circuits use target hardware gate set
5. **Iterate** - Apply multiple optimization passes for best results

## Limitations

This skill performs **static analysis** and may miss:

- **Dynamic circuits** - Gates added at runtime based on measurements
- **Parameterized circuits** - Symbolic parameters prevent gate fusion analysis
- **Matrix-based optimizations** - Requires numerical decomposition
- **Hardware-specific compiler optimizations** - Device-specific tricks
- **Noise-aware optimizations** - Requires noise model simulation

For comprehensive optimization, the skill will suggest using framework-specific tools:
- Qiskit: `transpile(circuit, optimization_level=3)`
- Cirq: `cirq.optimize_for_target_gateset(circuit)`

## Framework-Specific Notes

### Qiskit
- Best support via `.transpile()` with optimization levels 0-3
- Native support for IBM Quantum hardware constraints
- Excellent basis gate decomposition

### Cirq
- Optimizer: `cirq.optimize_for_target_gateset()`
- Good for Google Quantum AI hardware
- Strong circuit transformation library

### OpenQASM
- Static analysis works well
- Limited optimization without additional tools
- Great for educational purposes

### PennyLane
- Optimizes via `qml.optimize()`
- Strong differentiable programming support
- Good for quantum machine learning

### Quil
- Quilc compiler handles optimization
- Optimized for Rigetti hardware
- Good native gate support

## Advanced Usage

### Custom Gate Pattern Detection
Find custom gate definitions in your code:
```bash
grep -E "def.*gate|@quantum_gate" *.py
```

### Parameterized Circuit Analysis
Detect parameter usage:
```bash
grep -E "Parameter|ParameterVector" *.py
```

### Hardware Metrics
Check device-specific considerations:
```bash
grep -E "(basis_gates|coupling_map|backend)" *.py
```

## Contributing

Found a bug or want to add support for a new quantum framework? Contributions welcome!

See [CONTRIBUTING.md](../../../../CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](../../../../LICENSE) for details
