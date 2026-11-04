# qiskit-qir

> **Deprecated.** This fork is no longer maintained and the repository is
> archived. `qiskit-alice-bob-provider` 3.0 and later converts circuits to QIR
> itself and no longer depends on this package:
>
> ```python
> from qiskit_alice_bob_provider.qir import circuit_to_qir
>
> qir = circuit_to_qir(circuit)  # LLVM text of the QIR module
> ```
>
> The package stays on PyPI so that older provider versions still install.

Qiskit to QIR translator.

This is a temporary fork until the upstream qiskit-qir supports user-defined
instructions.

## Example

```python
from qiskit import QuantumCircuit
from qiskit_qir import to_qir_module

circuit = QuantumCircuit(3, 3, name="my-circuit")
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

module, entry_points = to_qir_module(circuit)
bitcode = module.bitcode
ir = str(module)
```

## Installation

Install `qiskit-qir` with `pip`:

```bash
pip install qiskit-qir
```
> Note: this will automatically install PyQIR if needed.

## Development

### Install from source

To install the package from source, clone the repo onto your machine, browse to the root directory and run

```bash
pip install -e .
```

### Tests

First, install the development dependencies using

```bash
pip install -r requirements_dev.txt
```

To run the tests in your local environment, run

```bash
make test
```

To run the tests in virtual environments on supported Python versions, run

```bash
make test-all
```

### Docs

To build the docs using Sphinx, run

```bash
make docs
```
