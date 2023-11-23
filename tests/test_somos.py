"""Somos tests"""

import unittest

from somos import Sequence


class TestSequence(unittest.TestCase):
    def test_sequence_generation(self):
        seq = Sequence(4, num_terms=10)
        expected_sequence = [1, 1, 1, 1, 2, 3, 7, 23, 59, 314]
        self.assertEqual(seq.sequence, expected_sequence)

    def test_sequence_with_k_2(self):
        seq = Sequence(2, num_terms=10)
        expected_sequence = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(seq.sequence, expected_sequence)

    def test_sequence_with_large_k(self):
        seq = Sequence(10, num_terms=10)
        # Check that the sequence starts with 10 ones
        self.assertEqual(seq.sequence[:10], [1] * 10)

    def test_invalid_k(self):
        with self.assertRaises(ValueError):
            Sequence(1)

    def text_negative_k(self):
        with self.assertRaises(ValueError):
            Sequence(-1)

    def test_k_not_int(self):
        with self.assertRaises(TypeError):
            Sequence("4")

    def test_invalid_num_terms(self):
        with self.assertRaises(ValueError):
            Sequence(4, num_terms=0)

    def test_negative_num_terms(self):
        with self.assertRaises(ValueError):
            Sequence(4, num_terms=-1)

    def test_num_terms_not_int(self):
        with self.assertRaises(TypeError):
            Sequence(4, num_terms="10")

    def test_invalid_num_non_triv_terms(self):
        with self.assertRaises(ValueError):
            Sequence(4, num_non_triv_terms=0)

    def test_negative_num_non_triv_terms(self):
        with self.assertRaises(ValueError):
            Sequence(4, num_non_triv_terms=-1)

    def test_num_non_triv_terms_not_int(self):
        with self.assertRaises(TypeError):
            Sequence(4, num_non_triv_terms="10")


if __name__ == "__main__":
    unittest.main()
