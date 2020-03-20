# Author: Dominic Lupo
# Date: 03/12/2020
# Description: Unit tests for XiangqiGame

import unittest
from XiangqiGame import XiangqiGame
from General import General
from Advisor import Advisor
from Horse import Horse
from Chariot import Chariot
from Elephant import Elephant
from Cannon import Cannon
from Soldier import Soldier


class TestProduct(unittest.TestCase):
    """Contains unit tests for XiangqiGame.py"""

    def test_general_moves(self):
        """Tests all types of General moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        # test flying general and cannot leave castle
        red_general_moves = game.get_valid_end_pos_array("e1", "G")
        black_general_moves = game.get_valid_end_pos_array("d10", "G")
        self.assertEqual(["f1", "e2"], red_general_moves)
        self.assertEqual(["d9"], black_general_moves)

        game.make_move("e1", "e2")
        game.make_move("d10", "d9")

        red_general_moves = game.get_valid_end_pos_array("e2", "G")
        black_general_moves = game.get_valid_end_pos_array("d9", "G")
        self.assertEqual(["f2", "e3", "e1"], red_general_moves)
        self.assertEqual(["d10", "d8"], black_general_moves)

        game.make_move("e2", "e3")
        game.make_move("d9", "d8")

        red_general_moves = game.get_valid_end_pos_array("e3", "G")
        black_general_moves = game.get_valid_end_pos_array("d8", "G")
        self.assertEqual(["f3", "e2"], red_general_moves)
        self.assertEqual(["d9"], black_general_moves)

        # test can only capture opposing color pieces
        board.get_point_with_pos("f3").set_piece(Advisor("red"))
        board.get_point_with_pos("e2").set_piece(Soldier("black"))

        red_general_moves = game.get_valid_end_pos_array("e3", "G")
        self.assertEqual(["e2"], red_general_moves)

        # test can have no moves
        board.get_point_with_pos("e2").set_piece(Soldier("red"))

        red_general_moves = game.get_valid_end_pos_array("e3", "G")
        self.assertEqual([], red_general_moves)

    def test_advisor_moves(self):
        """Tests all types of Advisor moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d9").set_piece(General("black"))

        board.get_point_with_pos("d1").set_piece(Advisor("red"))
        board.get_point_with_pos("f1").set_piece(Advisor("red"))
        board.get_point_with_pos("d10").set_piece(Advisor("black"))
        board.get_point_with_pos("f10").set_piece(Advisor("black"))

        # cannot leave castle
        red_advisor_moves = game.get_valid_end_pos_array("d1", "A")
        black_advisor_moves = game.get_valid_end_pos_array("d10", "A")
        self.assertEqual(["e2"], red_advisor_moves)
        self.assertEqual(["e9"], black_advisor_moves)

        red_advisor_moves = game.get_valid_end_pos_array("d1", "A")
        black_advisor_moves = game.get_valid_end_pos_array("d10", "A")
        self.assertEqual(["e2"], red_advisor_moves)
        self.assertEqual(["e9"], black_advisor_moves)

        game.make_move("d1", "e2")
        game.make_move("d10", "e9")

        # test can only capture opposing color pieces
        board.get_point_with_pos("d1").set_piece(Soldier("black"))
        board.get_point_with_pos("d10").set_piece(Soldier("red"))

        red_advisor_moves = game.get_valid_end_pos_array("e2", "A")
        black_advisor_moves = game.get_valid_end_pos_array("e9", "A")
        self.assertEqual(["f3", "d3", "d1"], red_advisor_moves)
        self.assertEqual(["d10", "d8", "f8"], black_advisor_moves)

        # test can have no moves
        red_advisor_moves = game.get_valid_end_pos_array("f1", "A")
        black_advisor_moves = game.get_valid_end_pos_array("f10", "A")
        self.assertEqual([], red_advisor_moves)
        self.assertEqual([], black_advisor_moves)

    def test_elephant_moves(self):
        """Tests all types of Elephant moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        board.get_point_with_pos("c1").set_piece(Elephant("red"))
        board.get_point_with_pos("g1").set_piece(Elephant("red"))
        board.get_point_with_pos("c10").set_piece(Elephant("black"))
        board.get_point_with_pos("g10").set_piece(Elephant("black"))

        # test can only capture opposing color pieces
        red_elephant_moves = game.get_valid_end_pos_array("c1", "E")
        black_elephant_moves = game.get_valid_end_pos_array("c10", "E")
        self.assertEqual(["e3", "a3"], red_elephant_moves)
        self.assertEqual(["e8", "a8"], black_elephant_moves)

        red_elephant_moves = game.get_valid_end_pos_array("g1", "E")
        black_elephant_moves = game.get_valid_end_pos_array("g10", "E")
        self.assertEqual(["i3", "e3"], red_elephant_moves)
        self.assertEqual(["i8", "e8"], black_elephant_moves)

        game.make_move("c1", "e3")
        game.make_move("c10", "e8")

        board.get_point_with_pos("c1").set_piece(Soldier("black"))
        board.get_point_with_pos("c10").set_piece(Soldier("red"))

        red_elephant_moves = game.get_valid_end_pos_array("e3", "E")
        black_elephant_moves = game.get_valid_end_pos_array("e8", "E")
        self.assertEqual(["g5", "c5", "c1"], red_elephant_moves)
        self.assertEqual(["g6", "c10", "c6"], black_elephant_moves)

        # test cannot jump over pieces and test can have no moves
        board.get_point_with_pos("h2").set_piece(Soldier("red"))
        board.get_point_with_pos("h9").set_piece(Soldier("red"))

        red_elephant_moves = game.get_valid_end_pos_array("g1", "E")
        black_elephant_moves = game.get_valid_end_pos_array("g10", "E")
        self.assertEqual([], red_elephant_moves)
        self.assertEqual([], black_elephant_moves)

        # test cannot cross river
        board.get_point_with_pos("c1").set_piece(None)
        board.get_point_with_pos("c10").set_piece(None)

        game.make_move("e3", "c5")
        game.make_move("e8", "c6")

        red_elephant_moves = game.get_valid_end_pos_array("c5", "E")
        black_elephant_moves = game.get_valid_end_pos_array("c6", "E")
        self.assertEqual(["e3", "a3"], red_elephant_moves)
        self.assertEqual(["e8", "a8"], black_elephant_moves)

    def test_horse_moves(self):
        """Tests all types of Horse moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        board.get_point_with_pos("b1").set_piece(Horse("red"))
        board.get_point_with_pos("b10").set_piece(Horse("black"))

        # test can only capture opposing color pieces
        board.get_point_with_pos("c3").set_piece(Soldier("red"))
        board.get_point_with_pos("c8").set_piece(Soldier("red"))

        red_horse_moves = game.get_valid_end_pos_array("b1", "H")
        black_horse_moves = game.get_valid_end_pos_array("b10", "H")
        self.assertEqual(["d2", "a3"], red_horse_moves)
        self.assertEqual(["a8", "c8", "d9"], black_horse_moves)

        # test can be blocked
        board.get_point_with_pos("c1").set_piece(Soldier("red"))
        board.get_point_with_pos("c10").set_piece(Soldier("red"))

        red_horse_moves = game.get_valid_end_pos_array("b1", "H")
        black_horse_moves = game.get_valid_end_pos_array("b10", "H")
        self.assertEqual(["a3"], red_horse_moves)
        self.assertEqual(["a8", "c8"], black_horse_moves)

        # test can have no moves
        board.get_point_with_pos("b2").set_piece(Soldier("red"))
        board.get_point_with_pos("b9").set_piece(Soldier("red"))

        red_horse_moves = game.get_valid_end_pos_array("b1", "H")
        black_horse_moves = game.get_valid_end_pos_array("b10", "H")
        self.assertEqual([], red_horse_moves)
        self.assertEqual([], black_horse_moves)

    def test_chariot_moves(self):
        """Tests all types of Chariot moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        board.get_point_with_pos("a1").set_piece(Chariot("red"))
        board.get_point_with_pos("a10").set_piece(Chariot("black"))

        # test can only capture opposing color and cannot jump
        board.get_point_with_pos("a3").set_piece(Soldier("red"))
        board.get_point_with_pos("a8").set_piece(Soldier("red"))

        red_chariot_moves = game.get_valid_end_pos_array("a1", "R")
        black_chariot_moves = game.get_valid_end_pos_array("a10", "R")
        self.assertEqual(["b1", "c1", "d1", "a2"], red_chariot_moves)
        self.assertEqual(["b10", "c10", "a9", "a8"], black_chariot_moves)

    def test_soldier_moves(self):
        """Tests all types of Soldier moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        board.get_point_with_pos("a4").set_piece(Soldier("red"))
        board.get_point_with_pos("i7").set_piece(Soldier("black"))

        # test can only move forward on own side
        red_soldier_moves = game.get_valid_end_pos_array("a4", "S")
        black_soldier_moves = game.get_valid_end_pos_array("i7", "S")
        self.assertEqual(["a5"], red_soldier_moves)
        self.assertEqual(["i6"], black_soldier_moves)

        game.make_move("a4", "a5")
        game.make_move("i7", "i6")

        red_soldier_moves = game.get_valid_end_pos_array("a5", "S")
        black_soldier_moves = game.get_valid_end_pos_array("i6", "S")
        self.assertEqual(["a6"], red_soldier_moves)
        self.assertEqual(["i5"], black_soldier_moves)

        # test can move forward and sideways on opposing side
        game.make_move("a5", "a6")
        game.make_move("i6", "i5")

        red_soldier_moves = game.get_valid_end_pos_array("a6", "S")
        black_soldier_moves = game.get_valid_end_pos_array("i5", "S")
        self.assertEqual(["b6", "a7"], red_soldier_moves)
        self.assertEqual(["h5", "i4"], black_soldier_moves)

        game.make_move("a6", "b6")
        game.make_move("i5", "h5")

        red_soldier_moves = game.get_valid_end_pos_array("b6", "S")
        black_soldier_moves = game.get_valid_end_pos_array("h5", "S")
        self.assertEqual(["c6", "a6", "b7"], red_soldier_moves)
        self.assertEqual(["i5", "g5", "h4"], black_soldier_moves)

        # test can only capture opposing color
        board.get_point_with_pos("c6").set_piece(Soldier("red"))
        board.get_point_with_pos("a6").set_piece(Soldier("black"))

        board.get_point_with_pos("i5").set_piece(Soldier("red"))
        board.get_point_with_pos("g5").set_piece(Soldier("black"))

        red_soldier_moves = game.get_valid_end_pos_array("b6", "S")
        black_soldier_moves = game.get_valid_end_pos_array("h5", "S")
        self.assertEqual(["a6", "b7"], red_soldier_moves)
        self.assertEqual(["i5", "h4"], black_soldier_moves)

    def test_cannon_moves(self):
        """Tests all types of Cannon moves that are valid."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        board.get_point_with_pos("b4").set_piece(Cannon("red"))
        board.get_point_with_pos("b7").set_piece(Cannon("black"))

        # test cannot capture own piece and must jump to capture
        board.get_point_with_pos("b2").set_piece(Soldier("black"))
        board.get_point_with_pos("b9").set_piece(Soldier("red"))

        red_cannon_moves = game.get_valid_end_pos_array("b4", "C")
        black_cannon_moves = game.get_valid_end_pos_array("b7", "C")
        self.assertEqual(['c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4', 'a4', 'b5', 'b6', 'b3'], red_cannon_moves)

        self.assertEqual(['c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7', 'a7', 'b8', 'b6', 'b5'], black_cannon_moves)

        # test can capture opposing piece if jumping one piece of different color
        board.get_point_with_pos("b2").set_piece(Soldier("red"))
        board.get_point_with_pos("b9").set_piece(Soldier("black"))

        red_cannon_moves = game.get_valid_end_pos_array("b4", "C")
        black_cannon_moves = game.get_valid_end_pos_array("b7", "C")
        self.assertEqual(['c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4', 'a4', 'b5', 'b6', 'b9', 'b3'], red_cannon_moves)

        self.assertEqual(['c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7', 'a7', 'b8', 'b6', 'b5', 'b2'], black_cannon_moves)

        # test cannot capture opposing piece if jumping more than two pieces
        board.get_point_with_pos("b2").set_piece(Soldier("red"))
        board.get_point_with_pos("b9").set_piece(Soldier("black"))
        board.get_point_with_pos("b3").set_piece(Soldier("black"))
        board.get_point_with_pos("b8").set_piece(Soldier("red"))

        red_cannon_moves = game.get_valid_end_pos_array("b4", "C")
        black_cannon_moves = game.get_valid_end_pos_array("b7", "C")
        self.assertEqual(['c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4', 'a4', 'b5', 'b6'], red_cannon_moves)

        self.assertEqual(['c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7', 'a7', 'b6', 'b5'], black_cannon_moves)

        # test can capture opposing piece if jumping one piece of same color
        board.get_point_with_pos("b3").set_piece(None)
        board.get_point_with_pos("b8").set_piece(None)

        board.get_point_with_pos("b4").set_piece(Cannon("black"))

        black_cannon_moves = game.get_valid_end_pos_array("b7", "C")
        self.assertEqual(['c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7', 'a7', 'b8', 'b6', 'b5', 'b2'], black_cannon_moves)

        board.get_point_with_pos("b4").set_piece(Cannon("red"))
        board.get_point_with_pos("b7").set_piece(Cannon("red"))

        red_cannon_moves = game.get_valid_end_pos_array("b4", "C")
        self.assertEqual(['c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4', 'a4', 'b5', 'b6', 'b9', 'b3'], red_cannon_moves)

        board.get_point_with_pos("b7").set_piece(Cannon("black"))

    def test_oppposing_player_color(self):
        """Tests opposing_player_color returns correct color."""

        game = XiangqiGame()

        self.assertEqual("black", game.opposing_player_color("red"))
        self.assertEqual("red", game.opposing_player_color("black"))

    def test_is_in_check(self):
        """Tests is_in_check correctly returns if the current player is in check for both red and black."""

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        # test where red and black are not in check
        self.assertEqual(False, game.is_in_check("red"))
        self.assertEqual(False, game.is_in_check("black"))

        board.get_point_with_pos("e3").set_piece(Chariot("red"))
        board.get_point_with_pos("d8").set_piece(Chariot("black"))

        self.assertEqual(False, game.is_in_check("red"))
        self.assertEqual(False, game.is_in_check("black"))

        # test where black is in check
        board.get_point_with_pos("d8").set_piece(Chariot("red"))

        self.assertEqual(False, game.is_in_check("red"))
        self.assertEqual(True, game.is_in_check("black"))

        # test where red is in check
        board.get_point_with_pos("d8").set_piece(None)
        board.get_point_with_pos("e3").set_piece(Chariot("black"))

        self.assertEqual(True, game.is_in_check("red"))
        self.assertEqual(False, game.is_in_check("black"))

    def test_checkmate_preventable(self):
        """
        Tests that checkmate_preventable returns True if a move is possible that removes check from the player in check.
        """

        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        # test red can prevent checkmate
        self.assertEqual(True, game.checkmate_preventable())

        game.make_move("e1", "e2")

        # test black can prevent checkmate
        self.assertEqual(True, game.checkmate_preventable())

        game.make_move("d10", "d9")

        # test black cant prevent checkmate
        self.assertEqual(True, game.checkmate_preventable())

        board.get_point_with_pos("d1").set_piece(Chariot("red"))
        game.make_move("d1", "d2")

        self.assertEqual(False, game.checkmate_preventable())

        # test red cant prevent checkmate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("e10").set_piece(Chariot("black"))
        board.get_point_with_pos("f10").set_piece(Chariot("black"))

        self.assertEqual(False, game.checkmate_preventable())

    def test_stalemate(self):
        """Tests stalemate correctly determines if red and black are put into stalemate."""

        # test red in stalemate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("f10").set_piece(Chariot("black"))

        self.assertEqual(False, game.stalemate())

        board.get_point_with_pos("a2").set_piece(Chariot("black"))

        self.assertEqual(True, game.stalemate())

        # test black in stalemate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        game.make_move("e1", "f1")

        self.assertEqual(False, game.stalemate())

        board.get_point_with_pos("e9").set_piece(Chariot("red"))
        board.get_point_with_pos("c9").set_piece(Chariot("red"))

        self.assertEqual(True, game.stalemate())

    def test_update_game_state_with_stalemate(self):
        """Test when stalemate happens game_state is correctly updated."""

        # test red won with stalemate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("f1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("e9").set_piece(Chariot("red"))

        self.assertEqual("UNFINISHED", game.get_game_state())

        game.make_move("f1", "e1")
        self.assertEqual("RED_WON", game.get_game_state())

        # test black won with stalemate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("f1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        game.make_move("f1", "e1")
        self.assertEqual("UNFINISHED", game.get_game_state())

        board.get_point_with_pos("d2").set_piece(Chariot("black"))
        board.get_point_with_pos("g2").set_piece(Chariot("black"))

        self.assertEqual("UNFINISHED", game.get_game_state())

        game.make_move("g2", "f2")
        self.assertEqual("BLACK_WON", game.get_game_state())

    def test_update_game_state_with_checkmate(self):
        """tests when checkmate happens game_state is correctly updated."""

        # test red won with checkmate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("a1").set_piece(Chariot("red"))

        self.assertEqual("UNFINISHED", game.get_game_state())

        game.make_move("a1", "d1")
        self.assertEqual("RED_WON", game.get_game_state())

        # test black won with checkmate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("e1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))

        game.make_move("e1", "f1")

        board.get_point_with_pos("e10").set_piece(Chariot("black"))
        board.get_point_with_pos("g10").set_piece(Chariot("black"))

        self.assertEqual("UNFINISHED", game.get_game_state())

        game.make_move("g10", "f10")
        self.assertEqual("BLACK_WON", game.get_game_state())

    def test_move_must_prevent_checkmate_if_in_check(self):
        """Tests that if player is in check, only moves that prevent checck are allowed."""

        # test red must prevent checkmate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("f1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("e10").set_piece(Chariot("black"))
        board.get_point_with_pos("i10").set_piece(Chariot("black"))
        board.get_point_with_pos("a1").set_piece(Chariot("red"))

        game.make_move("a1", "a2")
        game.make_move("i10", "f10")

        self.assertEqual(False, game.make_move("a2", "b2"))
        self.assertEqual(False, game.make_move("f1", "e1"))
        self.assertEqual(True, game.make_move("a2", "f2"))

        # test black must prevent checkmate
        game = XiangqiGame()
        board = game.get_board()
        board.clear_board()

        board.get_point_with_pos("f1").set_piece(General("red"))
        board.get_point_with_pos("d10").set_piece(General("black"))
        board.get_point_with_pos("a9").set_piece(Chariot("black"))
        board.get_point_with_pos("e4").set_piece(Chariot("red"))
        board.get_point_with_pos("a2").set_piece(Chariot("red"))

        game.make_move("a2", "d2")

        self.assertEqual(False, game.make_move("d10", "d9"))
        self.assertEqual(False, game.make_move("a9", "b9"))
        self.assertEqual(True, game.make_move("a9", "d9"))


if __name__ == '__main__':
    unittest.main()
