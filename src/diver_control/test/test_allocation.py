"""Verify the allocation matrix keeps full 6-DOF control, even with a dead thruster."""
import numpy as np
from diver_control.thruster_allocation import allocation_matrix, mixer, THRUSTERS


def test_full_rank():
    A = allocation_matrix()
    assert np.linalg.matrix_rank(A) == 6


def test_mixer_reproduces_commanded_wrench():
    A = allocation_matrix()
    Ainv = mixer(A)
    for i in range(6):
        w = np.zeros(6); w[i] = 1.0
        assert np.allclose(A @ (Ainv @ w), w, atol=1e-9)


def test_over_actuated_survives_one_fault():
    faulted = [t for j, t in enumerate(THRUSTERS) if j != 2]
    assert np.linalg.matrix_rank(allocation_matrix(faulted)) == 6


def test_depth_hold_converges():
    from diver_control.depth_hold import simulate
    log = simulate(setpoint=5.0, T=40.0)
    final = log[-1, 1]
    assert abs(final - 5.0) < 0.10, f"depth-hold did not settle, final={final:.3f}"


def test_positive_buoyancy_is_safe():
    from diver_control.depth_hold import net_buoyancy
    assert net_buoyancy() > 0, "vehicle must float up when unpowered"


def test_terminal_velocity_balances_drag():
    from diver_control.hydrodynamics import drag, terminal_velocity, B, W
    vt = terminal_velocity()
    assert abs(drag(vt) - abs(B - W)) < 1e-6


def test_drag_is_quadratic():
    from diver_control.hydrodynamics import drag
    assert abs(drag(2.0) / drag(1.0) - 4.0) < 1e-9


def test_depth_pressure_roundtrip():
    from diver_control.hydrodynamics import pressure_at_depth, depth_from_pressure
    assert abs(depth_from_pressure(pressure_at_depth(42.0)) - 42.0) < 1e-6
