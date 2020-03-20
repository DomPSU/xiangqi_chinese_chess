# Author: Dominic Lupo
# Date: 03/12/2020
# Description: Unit tests for Board

import unittest
from Board import Board


class TestProduct(unittest.TestCase):
    """Contains unit tests for XiangqiGame.py"""

    def test_generate_point_array(self):
        """Tests for correct point_array generation."""

        a_board = Board()
        generated_point_array = []

        for point in a_board.get_point_array():
            generated_point_array.append(point.get_file() + point.get_rank())

        correct_point_array = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10',
                               'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10',
                               'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10',
                               'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10',
                               'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10',
                               'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
                               'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10',
                               'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10',
                               'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10']

        self.assertEqual(correct_point_array, generated_point_array)

    def test_generate_red_array(self):
        """Tests for correct red_array generation."""

        a_board = Board()
        generated_red_array = []

        for pos in a_board.get_red_side_array():
            generated_red_array.append(pos)

        correct_red_array = ['a1', 'a2', 'a3', 'a4', 'a5',
                             'b1', 'b2', 'b3', 'b4', 'b5',
                             'c1', 'c2', 'c3', 'c4', 'c5',
                             'd1', 'd2', 'd3', 'd4', 'd5',
                             'e1', 'e2', 'e3', 'e4', 'e5',
                             'f1', 'f2', 'f3', 'f4', 'f5',
                             'g1', 'g2', 'g3', 'g4', 'g5',
                             'h1', 'h2', 'h3', 'h4', 'h5',
                             'i1', 'i2', 'i3', 'i4', 'i5']

        self.assertEqual(correct_red_array, generated_red_array)

    def test_generate_black_array(self):
        """Tests for correct black_array generation."""

        a_board = Board()
        generated_black_array = []

        for pos in a_board.get_black_side_array():
            generated_black_array.append(pos)

        correct_black_array = ['a6', 'a7', 'a8', 'a9', 'a10',
                               'b6', 'b7', 'b8', 'b9', 'b10',
                               'c6', 'c7', 'c8', 'c9', 'c10',
                               'd6', 'd7', 'd8', 'd9', 'd10',
                               'e6', 'e7', 'e8', 'e9', 'e10',
                               'f6', 'f7', 'f8', 'f9', 'f10',
                               'g6', 'g7', 'g8', 'g9', 'g10',
                               'h6', 'h7', 'h8', 'h9', 'h10',
                               'i6', 'i7', 'i8', 'i9', 'i10']

        self.assertEqual(correct_black_array, generated_black_array)

    def test_get_point(self):
        """Tests get_point with both 1 and 2 length ranks."""

        a_board = Board()

        first_point = a_board.get_point_array()[0]
        last_point = a_board.get_point_array()[-1]

        first_point_file = first_point.get_file()
        first_point_rank = first_point.get_rank()

        last_point_file = last_point.get_file()
        last_point_rank = last_point.get_rank()

        self.assertEqual(first_point, a_board.get_point(first_point_file, first_point_rank))
        self.assertEqual(last_point, a_board.get_point(last_point_file, last_point_rank))

    def test_get_point_with_pos(self):
        """Tests get_point_with_pos with both 1 and 2 lengths ranks."""

        a_board = Board()

        first_point = a_board.get_point_array()[0]
        last_point = a_board.get_point_array()[-1]

        first_point_file = first_point.get_file()
        first_point_rank = first_point.get_rank()

        last_point_file = last_point.get_file()
        last_point_rank = last_point.get_rank()

        self.assertEqual(first_point, a_board.get_point_with_pos(first_point_file + first_point_rank))
        self.assertEqual(last_point, a_board.get_point_with_pos(last_point_file + last_point_rank))


if __name__ == '__main__':
    unittest.main()
