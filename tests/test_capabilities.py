##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import List

import pytest
from qiskit_qir.elements import QiskitModule

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_qir.capability import (
    Capability,
    ConditionalBranchingOnResultError,
    QubitUseAfterMeasurementError,
)
from qiskit_qir.visitor import BasicQisVisitor

# test circuits


def teleport() -> QuantumCircuit:
    qq = QuantumRegister(3, name="qq")
    cr = ClassicalRegister(2, name="cr")
    circuit = QuantumCircuit(qq, cr, name="Teleport")
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    with circuit.if_test((cr, int("10", 2))):
        circuit.x(2)
    with circuit.if_test((cr, int("01", 2))):
        circuit.z(2)
    return circuit


def use_after_measure():
    qq = QuantumRegister(2, name="qq")
    cr = ClassicalRegister(2, name="cr")
    circuit = QuantumCircuit(qq, cr)

    circuit.h(1)
    circuit.measure(1, 1)
    circuit.h(1)

    return circuit


def use_another_after_measure():
    circuit = QuantumCircuit(3, 2)

    circuit.h(0)
    circuit.measure(0, 0)
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.measure(1, 1)

    return circuit


def use_another_after_measure_and_condition():
    qq = QuantumRegister(3, name="qq")
    cr = ClassicalRegister(2, name="cr")
    circuit = QuantumCircuit(qq, cr)

    circuit.h(0)
    circuit.measure(0, 0)
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.measure(1, 1)
    with circuit.if_test((cr, int("10", 2))):
        circuit.x(2)

    return circuit


def use_conditional_branch_on_single_register_true_value():
    circuit = QuantumCircuit(name="Conditional")
    qr = QuantumRegister(2, "qreg")
    cr = ClassicalRegister(3, "creg")
    circuit.add_register(qr)
    circuit.add_register(cr)
    circuit.x(0)
    circuit.measure(0, 0)
    with circuit.if_test((cr[2], 1)):
        circuit.x(1)
    circuit.measure(0, 1)

    return circuit


def use_conditional_branch_on_single_register_false_value():
    circuit = QuantumCircuit(name="Conditional")
    qr = QuantumRegister(2, "qreg")
    cr = ClassicalRegister(3, "creg")
    circuit.add_register(qr)
    circuit.add_register(cr)
    circuit.x(0)
    circuit.measure(0, 0)
    with circuit.if_test((cr[2], 0)):
        circuit.x(1)
    circuit.measure(0, 1)

    return circuit


def conditional_branch_on_bit():
    qr = QuantumRegister(2, "qreg")
    cr = ClassicalRegister(2, "creg")
    circuit = QuantumCircuit(qr, cr, name="conditional_branch_on_bit")
    circuit.x(0)
    circuit.measure(0, 0)
    with circuit.if_test((cr[0], 1)):
        circuit.x(1)
    circuit.measure(1, 1)
    return circuit


# Utility using new visitor
def circuit_to_qir(circuit, profile: str = "AdaptiveExecution"):
    module = QiskitModule.from_quantum_circuit(circuit=circuit)
    visitor = BasicQisVisitor(profile)
    module.accept(visitor)
    return visitor.ir()


def test_branching_on_measurement_fails_without_required_capability_one():
    circuit = teleport()
    with pytest.raises(ConditionalBranchingOnResultError) as exc_info:
        _ = circuit_to_qir(circuit, "BasicExecution")

    exception_raised = exc_info.value
    assert exception_raised.instruction.name == "if_else"
    assert exception_raised.instruction.num_clbits == 2
    assert exception_raised.instruction.num_qubits == 1
    # check that the instruction that caused the error is the correct one (the x gate in the if statement)
    assert exception_raised.instruction.params[0].data[0].name == "x"
    assert (
        str(exception_raised.instruction.condition) == "(ClassicalRegister(2, 'cr'), 2)"
    )
    assert str(exception_raised.qargs) == "[<Qubit register=(3, \"qq\"), index=2>]"
    assert str(exception_raised.cargs) == "[<Clbit register=(2, \"cr\"), index=0>, <Clbit register=(2, \"cr\"), index=1>]"
    assert str(exception_raised.profile) == "BasicExecution"
    assert exception_raised.instruction_string == "if(cr == 2) if_else(param(cr[0]),param(cr[1])) qq[2]"


def test_branching_on_measurement_fails_without_required_capability_two():
    circuit = use_conditional_branch_on_single_register_true_value()
    with pytest.raises(ConditionalBranchingOnResultError) as exc_info:
        _ = circuit_to_qir(circuit, "BasicExecution")

    exception_raised = exc_info.value
    assert exception_raised.instruction.name == "if_else"
    assert exception_raised.instruction.num_clbits == 1
    assert exception_raised.instruction.num_qubits == 1
    # check that the instruction that caused the error is the correct one (the x gate in the if statement)
    assert exception_raised.instruction.params[0].data[0].name == "x"
    assert (
        str(exception_raised.instruction.condition)
        == "(<Clbit register=(3, \"creg\"), index=2>, 1)"
    )
    assert str(exception_raised.qargs) == "[<Qubit register=(2, \"qreg\"), index=1>]"
    assert str(exception_raised.cargs) == "[<Clbit register=(3, \"creg\"), index=2>]"
    assert str(exception_raised.profile) == "BasicExecution"
    assert exception_raised.instruction_string == "if(creg[2] == 1) if_else(param(creg[2])) qreg[1]"


def test_branching_on_measurement_fails_without_required_capability_three():
    circuit = use_conditional_branch_on_single_register_false_value()
    with pytest.raises(ConditionalBranchingOnResultError) as exc_info:
        _ = circuit_to_qir(circuit, "BasicExecution")

    exception_raised = exc_info.value
    assert str(exception_raised.instruction).startswith(
        "Instruction(name='if_else', num_qubits=1, num_clbits=1, params=["
    )
    assert (
        str(exception_raised.instruction.condition)
        == '(<Clbit register=(3, "creg"), index=2>, 0)'
    )
    assert str(exception_raised.qargs) == '[<Qubit register=(2, "qreg"), index=1>]'
    assert str(exception_raised.cargs) == '[<Clbit register=(3, "creg"), index=2>]'
    assert str(exception_raised.profile) == "BasicExecution"
    assert (
        exception_raised.instruction_string
        == "if(creg[2] == 0) if_else(param(creg[2])) qreg[1]"
    )


def test_branching_on_measurement_register_passses_with_required_capability():
    circuit = teleport()
    _ = circuit_to_qir(circuit)


def test_branching_on_measurement_bit_passses_with_required_capability():
    circuit = conditional_branch_on_bit()
    _ = circuit_to_qir(circuit)


def test_reuse_after_measurement_fails_without_required_capability():
    circuit = use_after_measure()
    with pytest.raises(QubitUseAfterMeasurementError) as exc_info:
        _ = circuit_to_qir(circuit, "BasicExecution")

    exception_raised = exc_info.value
    assert (
        str(exception_raised.instruction)
        == "Instruction(name='h', num_qubits=1, num_clbits=0, params=[])"
    )
    assert getattr(exception_raised.instruction, "condition", None) is None
    assert str(exception_raised.qargs) == '[<Qubit register=(2, "qq"), index=1>]'
    assert str(exception_raised.cargs) == "[]"
    assert str(exception_raised.profile) == "BasicExecution"
    assert exception_raised.instruction_string == "h qq[1]"


def test_reuse_after_measurement_passes_with_required_capability():
    circuit = use_after_measure()
    _ = circuit_to_qir(circuit)


def test_using_an_unread_qubit_after_measuring_passes_without_required_capability():
    circuit = use_another_after_measure()
    _ = circuit_to_qir(circuit, "BasicExecution")


def test_use_another_after_measure_and_condition_passes_with_required_capability():
    circuit = use_another_after_measure_and_condition()
    _ = circuit_to_qir(circuit)
