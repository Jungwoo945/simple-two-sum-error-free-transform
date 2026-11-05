"""Core implementation of Knuth's two-sum error-free transformation.

Given floating point numbers a and b, ``two_sum(a, b)`` returns a pair
``(s, e)`` such that ``s == a + b`` (the rounded sum) and ``s + e == a + b``
exactly in real arithmetic, with ``e`` being the rounding error of the
addition.  The algorithm is the branch-free form published by Knuth
(TAOCP Vol. 2, 4.2.2) and popularised by Ogita, Rump and Oishi.

Why this module exists: floating point addition is not associative and the
rounded sum loses information.  Recovering the exact error term lets you
sum many numbers with a compensated (Kahan-style) accumulator or compute
residuals in iterative refinement without extra precision.  The trade-off
is that the transformation costs a handful of extra floating point
operations per addition and assumes round-to-nearest mode; it does not
work under directed rounding.
"""

from __future__ import annotations

from typing import NamedTuple


class TwoSumResult(NamedTuple):
    """Result of a two-sum transformation.

    Attributes:
        sum: The rounded sum ``a + b``.
        error: The exact residual such that ``sum + error == a + b`` in
            exact arithmetic.
    """

    sum: float
    error: float


def two_sum(a: float, b: float) -> TwoSumResult:
    """Return the rounded sum and its exact rounding error.

    This is Knuth's branch-free error-free transformation.  It requires
    round-to-nearest arithmetic and no overflow in the intermediate
    subtraction ``b - (s - a)``; for normal magnitudes this always holds.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        A :class:`TwoSumResult` whose ``sum`` is ``a + b`` and whose
        ``error`` satisfies ``sum + error == a + b`` exactly.

    Examples:
        >>> r = two_sum(0.1, 0.2)
        >>> r.sum
        0.30000000000000004
        >>> r.error
        -2.7755575615628914e-17
    """
    s = a + b
    # The naive error term ``(a - (s - b)) + (b - (s - a))`` is correct
    # only when the magnitudes of a and b are comparable.  Knuth's form
    # below is exact for all inputs (given round-to-nearest) because the
    # subtraction ``s - a`` is exact by Sterbenz' lemma whenever ``s`` and
    # ``a`` are close, which they are by construction.
    bb = s - a
    err = (a - (s - bb)) + (b - bb)
    return TwoSumResult(sum=s, error=err)
