import pytest

# from metrics import Metrics
from pr2_controller.metrics import Metrics


def test_no_baseline():
    assert Metrics().compute_degradation("DONE", 30.0, None) == (None, None)

def test_no_zero_division():
    assert Metrics().compute_degradation("DONE", 30.0, 0) == (None, None)
    assert Metrics().compute_degradation("DONE", 30.0, 0.0) == (None, None)

def test_faster_than_baseline_clamps_to_zero():
    degradation , slowdown = Metrics().compute_degradation("DONE", 7.2, 23.3)
    assert slowdown == pytest.approx(-16.1) # Neg slowdown check
    assert degradation == 0.0 # clamped but never negative


def test_halted_early_return():
    degradation, slowdown = Metrics().compute_degradation("HALTED", 7.2, 23.3)
    assert degradation is None
    assert slowdown is None


@pytest.mark.parametrize("elapsed", [0.0, 0.1, 5.0, 23.0, -3.0])
def test_yield_neg_degradation(elapsed):
    # elapsed < baseline= 23.3
    degradation, slowdown = Metrics().compute_degradation("DONE", elapsed, 23.3)
    assert degradation >= 0.0
    assert slowdown < 0.0

# elapsed == baseline
def test_exactly_baseline_zero_degradation():
    degradation, slowdown = Metrics().compute_degradation("DONE", 23.3, 23.3)
    assert degradation == 0.0
    assert slowdown == pytest.approx(0.0)

# elapsed > baseline, pos degredation
def test_slower_baseline_pos_degredation():
    degradation, slowdown = Metrics().compute_degradation("DONE", 47.5, 23.3)
    assert slowdown == pytest.approx(24.2)
    assert degradation == pytest.approx(24.2 / 23.3) # 103.9%

def test_real_run():
    degradation, slowdown = Metrics().compute_degradation("DONE", 33.3, 23.3)
    assert slowdown == pytest.approx(10.0)
    assert degradation * 100 == pytest.approx(42.918, abs = 0.1)

# HALTED situations
def test_halted_with_baseline():
    assert Metrics().compute_degradation("HALTED", 50.0, 23.3) == (None, None)

@pytest.mark.parametrize("result", ["HALTED", "Done", "done", "", "FAILED", None])
def test_only_DONE_as_completed(result):
    assert Metrics().compute_degradation(result, 47.5, 23.3) == (None, None)


