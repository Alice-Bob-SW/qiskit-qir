##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import transpile
from qiskit.circuit.random import random_circuit
from qiskit.transpiler import Target
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit_qir.visitor import SUPPORTED_INSTRUCTIONS


def _generate_random_fixture(num_qubits, depth):
    @pytest.fixture()
    def random():
        # The target basis gates should include all gates supported by
        # the visitor that may be used by a random_circuit()
        gates_dict = get_standard_gate_name_mapping()
        standard_gates = list(gates_dict.keys())
        basis_gates = [gate for gate in standard_gates if gate in SUPPORTED_INSTRUCTIONS]
        target = Target.from_configuration(
            basis_gates=basis_gates, num_qubits=num_qubits
        )
        circuit = random_circuit(num_qubits, depth, measure=True)
        return transpile(circuit, target=target)

    return random


# Generate random fixtures
random_fixtures = []
for num_qubits, depth in [(i + 2, j + 2) for i in range(9) for j in range(9)]:
    name = f"random_{num_qubits}x{depth}"
    locals()[name] = _generate_random_fixture(num_qubits, depth)
    random_fixtures.append(name)
