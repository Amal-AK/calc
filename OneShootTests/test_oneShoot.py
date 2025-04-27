# Prompt , o3 model
# ---------------------------------------------------------------------------
# here is a code for some functions for calculation, generate necessary pytest unit 
# tests for all the methods including class methods for the given code,
# and consider all typical cases and edge cases : code... "
# ---------------------------------------------------------------------------



# test_calc.py
import math
import pytest

import functions.calc_func as cf 
from functions.calc_class import Calculator

# ---------------------------------------------------------------------------
# calc_func –– pure function unit tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (-1, -2, -3),
        (1.5, 2.5, 4.0),
        (0, 0, 0),
        (1e308, 1e308, math.inf),          # float-overflow edge case
    ],
)
def test_add(a, b, expected):
    assert cf.add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 2, 3),
        (-5, -2, -3),
        (2.5, 5.5, -3.0),
        (0, 7, -7),
        (-1e308, 1e308, -math.inf),        # overflow toward -∞
    ],
)
def test_subtract(a, b, expected):
    assert cf.subtract(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 12),
        (-3, 4, -12),
        (1.5, 2, 3.0),
        (0, 123, 0),
        (1e200, 1e200, math.inf),          # overflow
    ],
)
def test_multiply(a, b, expected):
    assert cf.multiply(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 2, 2.5),
        (-6, -3, 2.0),
        (0, 5, 0.0),
        (7.5, 2.5, 3.0),
    ],
)
def test_divide(a, b, expected):
    # use approx so  floating rounding differences on various platforms pass
    assert cf.divide(a, b) == pytest.approx(expected)


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        cf.divide(1, 0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 4),
        (4, 3, 4),
        (4, 4, 4),         # equality tie chooses first argument
        (-1, -5, -1),
    ],
)
def test_maximum(a, b, expected):
    assert cf.maximum(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 4, 3),
        (4, 3, 3),
        (4, 4, 4),         # equality tie chooses first argument
        (-1, -5, -5),
    ],
)
def test_minimum(a, b, expected):
    assert cf.minimum(a, b) == expected


# ---------------------------------------------------------------------------
# Calculator class –– behavioural tests (stateful)
# ---------------------------------------------------------------------------

@pytest.fixture
def calc():
    return Calculator()


def test_initial_last_answer(calc):
    assert calc.last_answer == 0.0


@pytest.mark.parametrize(
    "method, a, b, expected",
    [
        ("add", 1, 2, 3),
        ("subtract", 5, 3, 2),
        ("multiply", 3, 4, 12),
        ("divide", 9, 3, 3.0),
        ("maximum", 5, 7, 7),
        ("minimum", 5, 7, 5),
    ],
)
def test_operations_return_correct_value_and_update_state(calc, method, a, b, expected):
    """
    • Result is correct
    • last_answer is updated to that result
    • return value and last_answer are identical objects (same float)
    """
    result = getattr(calc, method)(a, b)
    assert result == expected
    assert calc.last_answer == expected
    assert result is calc.last_answer  # identity check on small floats still valid


def test_successive_operations_overwrite_last_answer(calc):
    first = calc.add(2, 2)       # 4
    second = calc.multiply(3, 3) # 9
    assert first == 4
    assert second == 9
    assert calc.last_answer == 9  # only most-recent stored


def test__do_math_internal_method(calc):
    # Directly exercise the “private” helper
    out = calc._do_math(7, 2, cf.subtract)
    assert out == 5
    assert calc.last_answer == 5


def test__do_math_preserves_state_if_function_raises(calc):
    # Seed with a known good value
    calc.add(1, 1)
    assert calc.last_answer == 2

    with pytest.raises(ZeroDivisionError):
        calc._do_math(1, 0, cf.divide)

    # Should still be the previous good value because assignment
    # happens *after* the call to func succeeds.
    assert calc.last_answer == 2


# ---------------------------------------------------------------------------
# Type/identity and special-value edge-cases
# ---------------------------------------------------------------------------

def test_division_result_is_float_even_for_int_inputs(calc):
    res = calc.divide(4, 2)
    assert isinstance(res, float)
    assert res == 2.0


def test_add_large_numbers_overflow_to_inf(calc):
    res = calc.add(1e308, 1e308)
    assert math.isinf(res) and res > 0
    assert calc.last_answer == res
