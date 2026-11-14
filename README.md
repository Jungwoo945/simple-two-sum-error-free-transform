# simple-two-sum-error-free-transform

Split a floating point sum into its rounded result and the exact residual
using Knuth's error-free transformation.

## Usage

```python
from simple_two_sum_error_free_transform import two_sum, TwoSumResult

result: TwoSumResult = two_sum(0.1, 0.2)
print(result.sum)    # 0.30000000000000004
print(result.error)  # -2.7755575615628914e-17

# The defining property: sum + error is the exact real sum.
assert result.sum + result.error == 0.1 + 0.2
```

The module exports exactly two names:

- `two_sum(a: float, b: float) -> TwoSumResult`
- `TwoSumResult`, a `NamedTuple` with fields `sum` and `error`.

## Why this exists

Floating point addition rounds.  When you add many numbers, or add a tiny
number to a huge one, the rounding error accumulates and the final result
drifts away from the true sum.  Knuth's two-sum algorithm recovers the
exact rounding error of a single addition using only standard floating
point operations, with no extra precision and no branches.  You can feed
the residual into a compensated accumulator (Kahan, Neumaier) or use it
to compute residuals in iterative refinement.

The trade-off is cost: each addition now takes six floating point
operations instead of one.  The algorithm also assumes round-to-nearest
mode; under directed rounding the intermediate subtraction is not exact
and the recovered error is wrong.

## The awkward edge

`two_sum` is defined for finite inputs.  If either argument is an
infinity or a NaN the rounded sum is still computed, but the residual is
not meaningful: `two_sum(inf, 1.0)` returns `error = nan`.  This is
intentional — the transformation cannot recover a finite error from an
infinite sum — and the tests assert that behaviour rather than pretending
it does not happen.

## Testing

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

