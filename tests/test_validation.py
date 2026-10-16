import unittest

from src.validation.validate_dataset import (
    check,
    results,
)


class TestValidation(unittest.TestCase):

    def setUp(self):
        results.clear()

    def tearDown(self):
        results.clear()

    def test_valid_condition(self):
        check("prueba", "condicion valida", True, "OK")
        self.assertEqual(results[-1]["status"], "PASS")

    def test_invalid_condition(self):
        check("prueba", "condicion invalida", False, "Error")
        self.assertEqual(results[-1]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
