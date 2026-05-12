##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import transpile
from qiskit.circuit.random import random_circuit
from qiskit.transpiler import Target
from qiskit.circuit import Instruction, InstructionSet, QuantumCircuit
from qiskit.circuit.quantumcircuit import ClbitSpecifier, QubitSpecifier
from qiskit.circuit import IfElseOp
from qiskit.circuit import Barrier
from qiskit.circuit.library import Initialize
from typing import Optional

from qiskit_qir.visitor import SUPPORTED_INSTRUCTIONS
class MeasureX(Instruction):
    """Quantum measurement in the X basis."""

    def __init__(self, label: Optional[str] = None):
        """Create a new X-measurement instruction."""
        super().__init__("measure_x", 1, 1, [], label=label)
        self._definition = QuantumCircuit(1, 1, name="measure_x")
        self._definition.h(0)
        self._definition.measure(0, 0)
        self._definition.h(0)

def _measure_x(
    self: QuantumCircuit, qubit: QubitSpecifier, cbit: ClbitSpecifier
) -> InstructionSet:
    return self.append(MeasureX(), [qubit], [cbit])


# Patching the QuantumCircuit class to add a `measure_x` method.
QuantumCircuit.measure_x = _measure_x



def _random_target(num_qubits):
    # Instructions that are supported in the target but not to be specified as basis gates
    non_gate_instructions = ["if_else", "barrier", "initialize", "delay"] # Why is barrier in SUPPORTED_GATES but not if_else?
    abbreviated_gates = ["m"]
    custom_gates = ["measure_x"]
    basis_gates = [gate for gate in SUPPORTED_INSTRUCTIONS if gate not in non_gate_instructions and gate not in custom_gates and gate not in abbreviated_gates]
    target = Target.from_configuration(
        basis_gates=basis_gates, num_qubits=num_qubits
    )
    target.add_instruction(MeasureX, name="measure_x")
    target.add_instruction(IfElseOp, name="if_else")
    target.add_instruction(Barrier, name="barrier")
    target.add_instruction(Initialize, name="initialize")
    return target


def _generate_random_fixture(num_qubits, depth):
    @pytest.fixture()
    def random():
        circuit = random_circuit(num_qubits, depth, measure=True)
        return transpile(circuit, target=_random_target(num_qubits))

    return random


# Generate random fixtures
random_fixtures = []
for num_qubits, depth in [(i + 2, j + 2) for i in range(9) for j in range(9)]:
    name = f"random_{num_qubits}x{depth}"
    locals()[name] = _generate_random_fixture(num_qubits, depth)
    random_fixtures.append(name)
