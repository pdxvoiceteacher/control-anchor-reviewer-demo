"""Exact supplied-field arithmetic, not model, source-truth or approval proof."""
from decimal import localcontext, ROUND_DOWN, ROUND_UP, ROUND_HALF_EVEN
from fractions import Fraction

import unittest
from itertools import product

from triadicbrain.assurance.ucc_plan import execute_plan


def comparison(left, right, tolerance):
    plan = {'schema_id': 'control-anchor.ucc-plan.v1', 'plan_id': 'EXACT-AMOUNT',
            'version': 1, 'steps': [{'id': 'AMOUNT', 'title': 'Compare supplied amounts',
            'kind': 'executable', 'phase': 'result', 'operation': 'compare_amounts',
            'arguments': {'left': '/source/left', 'right': '/source/right',
                          'tolerance': tolerance}}]}
    return execute_plan(plan, {'source': {'left': left, 'right': right}}, phase='result')[0]


CASES = [
    ('10000000000000000000000000000.1', '0', '10000000000000000000000000000'),
    ('0', '10000000000000000000000000000.1', '10000000000000000000000000000'),
    ('99999999999999999999999999999.9', '0', '99999999999999999999999999999.9'),
    ('999999999999999999999999999999.999999999999',
     '-999999999999999999999999999999.999999999999', '999999999999999999999999999999'),
    ('1.000000000001', '1', '0.000000000001'),
    ('1.000000000002', '1', '0.000000000001'),
    ('-0.000000000001', '0', '0'),
    ('1', '1', '0'),
]


class AmountPrecisionTests(unittest.TestCase):
    def test_exact_rational_oracle(self):
        for precision, rounding, values in product((6, 28, 96), (ROUND_DOWN, ROUND_UP, ROUND_HALF_EVEN), CASES):
            left, right, tolerance = values
            with self.subTest(precision=precision, rounding=rounding, values=values):
                # Fraction arithmetic is independent of Decimal context and implementation.
                expected = 'PASS' if abs(Fraction(left) - Fraction(right)) <= Fraction(tolerance) else 'FAIL'
                with localcontext() as ambient:
                    ambient.prec = precision
                    ambient.rounding = rounding
                    before_flags = dict(ambient.flags)
                    row = comparison(left, right, tolerance)
                    assert row['result'] == expected
                    assert ambient.prec == precision and ambient.rounding == rounding
                    assert ambient.flags == before_flags
                assert row['human_procedure'] == 'NOT_EXECUTED'
                assert row['observation'] == ('DETERMINISTIC_CHECK_SATISFIED' if expected == 'PASS'
                                              else 'DETERMINISTIC_CHECK_NOT_SATISFIED')



    def test_invalid_input_failure(self):
        for value in (True, "NaN", "Infinity", "1e2", "0.0000000000001"):
            with self.subTest(value=value):
                self.assertEqual(comparison(value, "0", "0")["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
