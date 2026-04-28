##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import math
import numpy as np
import pytest

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


@pytest.fixture()
def while_loop():
    circuit = QuantumCircuit(1, 1)
    circuit.name = "Simple while-loop circuit"
    with circuit.while_loop((circuit.clbits[0], 0)):
        circuit.h(0)
        circuit.measure(0, 0)
    return circuit


@pytest.fixture()
def for_loop():
    qc = QuantumCircuit(2, 1)

    with qc.for_loop(range(5)) as i:
        qc.rx(i * math.pi / 4, 0)
        qc.cx(0, 1)
        qc.measure(0, 0)
        with qc.if_test((0, True)):
            qc.break_loop()
        qc.measure(0, 0)
    return qc


@pytest.fixture()
def if_else():
    circuit = QuantumCircuit(3, 2)

    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure(0, 0)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure(0, 1)

    with circuit.if_test((circuit.clbits[0], 0)) as else_:
        circuit.x(2)
    with else_:
        circuit.h(2)
        circuit.z(2)
    return circuit

@pytest.fixture()
def switch_case():
    qreg = QuantumRegister(3)
    creg = ClassicalRegister(3)
    qc = QuantumCircuit(qreg, creg)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    with qc.switch(creg) as case:
        with case(0):
            qc.x(0)
        with case(1, 2):
            qc.z(1)
        with case(case.DEFAULT):
            qc.cx(0, 1)

    return qc


cf_fixtures = ["while_loop", "for_loop", "if_else", "switch_case"]
