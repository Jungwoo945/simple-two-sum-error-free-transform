import math
import unittest

from simple_two_sum_error_free_transform import TwoSumResult, two_sum


class TestTwoSum(unittest.TestCase):
    def test_exact_small_integers(self):
        result = two_sum(2.0, 3.0)
        self.assertIsInstance(result, TwoSumResult)
        self.assertEqual(result.sum, 5.0)
        self.assertEqual(result.error, 0.0)

    def test_classic_rounding_error(self):
        result = two_sum(0.1, 0.2)
        self.assertAlmostEqual(result.sum, 0.30000000000000004, places=17)
        self.assertAlmostEqual(result.error, -2.7755575615628914e-17, places=35)
        # The defining property: sum + error is the exact real sum.
        self.assertEqual(result.sum + result.error, 0.1 + 0.2)

    def test_error_is_exact_residual(self):
        a = 1.0e16
        b = 1.0
        result = two_sum(a, b)
        # 1e16 + 1 is not representable; the residual is 1.0.
        self.assertEqual(result.sum, 1.0e16)
        self.assertEqual(result.error, 1.0)
        self.assertEqual(result.sum + result.error, a + b)

    def test_negative_values(self):
        result = two_sum(-1.5, -2.25)
        self.assertEqual(result.sum, -3.75)
        self.assertEqual(result.error, 0.0)

    def test_cancellation(self):
        a = 1.0e16
        b = -1.0e16
        result = two_sum(a, b)
        self.assertEqual(result.sum, 0.0)
        self.assertEqual(result.error, 0.0)

    def test_subnormal_residual(self):
        a = 1.0
        b = 2.0**-53
        result = two_sum(a, b)
        self.assertEqual(result.sum, 1.0)
        self.assertEqual(result.error, 2.0**-53)
        self.assertEqual(result.sum + result.error, a + b)

    def test_infinity(self):
        result = two_sum(math.inf, 1.0)
        self.assertEqual(result.sum, math.inf)
        self.assertTrue(math.isnan(result.error))

    def test_nan(self):
        result = two_sum(math.nan, 1.0)
        self.assertTrue(math.isnan(result.sum))
        self.assertTrue(math.isnan(result.error))

    def test_zero_signs(self):
        result = two_sum(0.0, -0.0)
        self.assertEqual(result.sum, 0.0)
        self.assertEqual(result.error, 0.0)

    def test_identity_with_compensated_sum(self):
        values = [1.0e100, 1.0, -1.0e100]
        total = 0.0
        compensation = 0.0
        for value in values:
            r = two_sum(total, value)
            total = r.sum
            compensation += r.error
        self.assertEqual(total + compensation, 1.0)

    def test_returns_namedtuple_fields(self):
        result = two_sum(1.0, 2.0)
        self.assertEqual(result.sum, 3.0)
        self.assertEqual(result.error, 0.0)
        self.assertEqual(result[0], 3.0)
        self.assertEqual(result[1], 0.0)

    def test_commutative(self):
        a = 0.1
        b = 0.2
        r1 = two_sum(a, b)
        r2 = two_sum(b, a)
        self.assertEqual(r1.sum, r2.sum)
        self.assertEqual(r1.error, r2.error)


if __name__ == "__main__":
    unittest.main()
