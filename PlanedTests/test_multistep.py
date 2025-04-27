




import builtins
import math
import pytest
from functions.calc_class import Calculator


@pytest.fixture
def calc():
    return Calculator()

# ---------------------------------------------------------------------------
# 1. Smoke / constructor
# ---------------------------------------------------------------------------

def test_defaults(calc):
    assert calc.last_answer == 0.0

# ---------------------------------------------------------------------------
# 2. Parameterised happy-path arithmetic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "method, a, b, expected",
    [
        ("add",       2,        3,        5),
        ("add",      -4,        4,        0),
        ("add",     3.5,      2.1,      5.6),
        ("subtract",  7,        5,        2),
        ("subtract", -2,       -5,        3),
        ("multiply",  4,        2,        8),
        ("multiply",  0,       42,        0),
        ("divide",    9,        4,      2.25),
        ("maximum",  10,        3,       10),
        ("minimum",  10,        3,        3),
    ],
)
def test_arithmetic_methods(calc, method, a, b, expected):
    result = getattr(calc, method)(a, b)
    assert result == pytest.approx(expected)
    # side effect
    assert calc.last_answer == pytest.approx(expected)

# ---------------------------------------------------------------------------
# 3. Equal-operand branches for max/min
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("method", ["maximum", "minimum"])
def test_equal_operands_return_first_operand(calc, method):
    obj = getattr(calc, method)(-7, -7)
    assert obj == -7
    assert calc.last_answer == -7

# ---------------------------------------------------------------------------
# 4. Division by zero
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("zero", [0, 0.0])
def test_divide_by_zero_raises(calc, zero):
    start = calc.last_answer
    with pytest.raises(ZeroDivisionError):
        calc.divide(5, zero)
    assert calc.last_answer == start  # unchanged on failure

# ---------------------------------------------------------------------------
# 5. Chaining via last_answer
# ---------------------------------------------------------------------------

def test_chaining(calc):
    assert calc.add(1, 2) == 3
    assert calc.multiply(calc.last_answer, 3) == 9
    assert calc.subtract(calc.last_answer, 4) == 5

# ---------------------------------------------------------------------------
# 6. Read-only property guard
# ---------------------------------------------------------------------------

def test_last_answer_is_read_only(calc):
    with pytest.raises(AttributeError):
        calc.last_answer = 999

# ---------------------------------------------------------------------------
# 7. Type robustness (these should bubble up as TypeError)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "method, a, b",
    [
        ("add",       "1",  2),
        ("subtract",  None, 3),
        ("multiply",  2+3j, 1),
        ("divide",    [],   1),
    ],
)
def test_bad_types_raise(calc, method, a, b):
    with pytest.raises(TypeError):
        getattr(calc, method)(a, b)

# ---------------------------------------------------------------------------
# 8. Float guarantee for divide
# ---------------------------------------------------------------------------

def test_divide_returns_float(calc):
    assert isinstance(calc.divide(7, 2), builtins.float)
