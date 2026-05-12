##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import transpile
from qiskit.circuit.random import random_circuit

# Standard Qiskit basis gates that overlap with supported instructions.
# Non-standard gates (m, measure_x, initialize, barrier, delay) are excluded
# because Qiskit 2.0 transpile() does not accept non-standard basis_gates.
_TRANSPILE_BASIS_GATES = [
    "measure", "cx", "cz", "h", "reset",
    "rx", "ry", "rz", "s", "sdg", "t", "tdg",
    "x", "y", "z", "id",
]


def _generate_random_fixture(num_qubits, depth):
    @pytest.fixture()
    def random():
        circuit = random_circuit(num_qubits, depth, measure=True)
        return transpile(circuit, basis_gates=_TRANSPILE_BASIS_GATES)

    return random


# Generate random fixtures
random_fixtures = []
for num_qubits, depth in [(i + 2, j + 2) for i in range(9) for j in range(9)]:
    name = f"random_{num_qubits}x{depth}"
    locals()[name] = _generate_random_fixture(num_qubits, depth)
    random_fixtures.append(name)
