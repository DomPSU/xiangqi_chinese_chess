# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a board for the game Xiangqi.


from Point import Point
from General import General
from Advisor import Advisor
from Horse import Horse
from Chariot import Chariot
from Elephant import Elephant
from Cannon import Cannon
from Soldier import Soldier


class Board:
    """Represents a board in the game Xiangqi."""

    def __init__(self):
        """
        Initializes the points on the board and sets up special board areas red_side, black_side and castles. Sets up
        the starting pieces on the board.
        """

        self.__file_array = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        self.__rank_array = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.__red_castle_array = ["d1", "e1", "f1", "d2", "e2", "f2", "d3", "e3", "f3"]
        self.__black_castle_array = ["d8", "e8", "f8", "d9", "e9", "f9", "d10", "e10", "f10"]
        self.__red_side_array = []
        self.__black_side_array = []
        self.__point_array = []

        # Append points to point array
        for file in self.__file_array:
            for rank in self.__rank_array:
                self.__point_array.append(Point(file, rank))

        # Append positions of red side points to red_side_array
        for file in self.__file_array:
            for rank in self.__rank_array[:5]:
                self.__red_side_array.append(file + rank)

        # Append positions of black side points to black_side_array
        for file in self.__file_array:
            for rank in self.__rank_array[5:]:
                self.__black_side_array.append(file + rank)

        self.reset_pieces()

    def clear_board(self):
        """Removes all pieces for the board."""

        # clear board
        for a_point in self.__point_array:
            a_point.set_piece(None)

        return None

    def reset_pieces(self):
        """Removes all pieces from the board and places all pieces in the starting positions."""

        self.clear_board()

        # place chariots in starting positions
        self.get_point("a", "10").set_piece(Chariot("black"))
        self.get_point("i", "10").set_piece(Chariot("black"))
        self.get_point("a", "1").set_piece(Chariot("red"))
        self.get_point("i", "1").set_piece(Chariot("red"))

        # place horses in starting positions
        self.get_point("b", "10").set_piece(Horse("black"))
        self.get_point("h", "10").set_piece(Horse("black"))
        self.get_point("b", "1").set_piece(Horse("red"))
        self.get_point("h", "1").set_piece(Horse("red"))

        # place elephants in starting positions
        self.get_point("c", "10").set_piece(Elephant("black"))
        self.get_point("g", "10").set_piece(Elephant("black"))
        self.get_point("c", "1").set_piece(Elephant("red"))
        self.get_point("g", "1").set_piece(Elephant("red"))

        # place advisors in starting positions
        self.get_point("d", "10").set_piece(Advisor("black"))
        self.get_point("f", "10").set_piece(Advisor("black"))
        self.get_point("d", "1").set_piece(Advisor("red"))
        self.get_point("f", "1").set_piece(Advisor("red"))

        # place generals in starting positions
        self.get_point("e", "10").set_piece(General("black"))
        self.get_point("e", "1").set_piece(General("red"))

        # place cannons in starting positions
        self.get_point("b", "8").set_piece(Cannon("black"))
        self.get_point("h", "8").set_piece(Cannon("black"))
        self.get_point("b", "3").set_piece(Cannon("red"))
        self.get_point("h", "3").set_piece(Cannon("red"))

        # place soldier in starting positions
        self.get_point("a", "7").set_piece(Soldier("black"))
        self.get_point("c", "7").set_piece(Soldier("black"))
        self.get_point("e", "7").set_piece(Soldier("black"))
        self.get_point("g", "7").set_piece(Soldier("black"))
        self.get_point("i", "7").set_piece(Soldier("black"))
        self.get_point("a", "4").set_piece(Soldier("red"))
        self.get_point("c", "4").set_piece(Soldier("red"))
        self.get_point("e", "4").set_piece(Soldier("red"))
        self.get_point("g", "4").set_piece(Soldier("red"))
        self.get_point("i", "4").set_piece(Soldier("red"))

    def get_file_array(self):
        """Getter for file_array."""

        return self.__file_array

    def get_rank_array(self):
        """Getter for rank_array."""

        return self.__rank_array

    def get_red_side_array(self):
        """Getter for red_side_array."""

        return self.__red_side_array

    def get_red_castle_array(self):
        """Getter for red_castle_array"""

        return self.__red_castle_array

    def get_black_side_array(self):
        """Getter for black-side_array."""

        return self.__black_side_array

    def get_black_castle_array(self):
        """Getter for black_castle_array"""

        return self.__black_castle_array

    def get_point_array(self):
        """Getter for point_array."""

        return self.__point_array

    def get_point(self, file, rank):
        """Return Point corresponding to passed file and rank. Returns None if point does not exist."""

        for a_point in self.__point_array:
            if (a_point.get_file() == file) and (a_point.get_rank() == rank):
                return a_point

        return None

    def get_point_with_pos(self, a_pos):
        """
        Returns the point with the file and rank indicated with the passed position. Returns None if point does not
        exist.
        """

        file = a_pos[0]

        if len(a_pos) == 2:
            rank = a_pos[1]
        else:
            rank = a_pos[1] + a_pos[2]

        return self.get_point(file, rank)

    def display(self):
        """Displays board with pieces and coordinates."""

        print(self.get_piece_row("10"))
        print("    | | | |\|/| | | |")
        print(self.get_piece_row("9"))
        print("    | | | |/|\| | | |")
        print(self.get_piece_row("8"))
        print("    | | | | | | | | |")
        print(self.get_piece_row("7"))
        print("    | | | | | | | | |")
        print(self.get_piece_row("6"))
        print("    |               |")
        print(self.get_piece_row("5"))
        print("    | | | | | | | | |")
        print(self.get_piece_row("4"))
        print("    | | | | | | | | |")
        print(self.get_piece_row("3"))
        print("    | | | |\|/| | | |")
        print(self.get_piece_row("2"))
        print("    | | | |/|\| | | |")
        print(self.get_piece_row("1"))
        print("                     ")
        print("    a b c d e f g h i")

    def get_piece_row(self, row_number):
        """Returns row with pieces and coordinates from the passed row_number."""

        row_string = " "

        # remove extra space in front on row number if row number is 10
        if row_number == "10":
            row_string = ""

        row_string = row_string + row_number + "  "

        # add respective row symbols to row_string
        for file in self.__file_array:
            a_point = self.get_point(file, row_number)
            symbol = a_point.get_symbol()

            row_string += symbol
            row_string += "-"

        row_string = row_string[:-1]

        return row_string

    def valid_file_index(self, file_index):
        """Returns True if the passed file_index exists within the file_array. Returns False otherwise."""

        max_file_index = len(self.get_file_array()) - 1
        min_file_index = 0

        if min_file_index <= file_index <= max_file_index:
            valid_file_index = True
        else:
            valid_file_index = False

        return valid_file_index

    def valid_rank_index(self, rank_index):
        """Returns True if the passed rank_index exists within the rank_array. Returns False otherwise."""

        max_rank_index = len(self.get_rank_array()) - 1
        min_rank_index = 0

        if min_rank_index <= rank_index <= max_rank_index:
            valid_rank_index = True
        else:
            valid_rank_index = False

        return valid_rank_index

    def get_file_index_from_pos(self, a_pos):
        """Returns the corresponding file_index from file_array for the passed a_pos."""

        file = self.get_file_from_pos(a_pos)

        file_array = self.get_file_array()

        file_index = file_array.index(file)

        return file_index

    def get_rank_index_from_pos(self, a_pos):
        """Returns the corresponding rank_index from rank_array for the passed a_pos."""

        rank = self.get_rank_from_pos(a_pos)

        rank_array = self.get_rank_array()

        rank_index = rank_array.index(rank)

        return rank_index

    @staticmethod
    def get_file_from_pos(a_pos):
        """Returns the file from the passed pos."""

        file = a_pos[0]

        return file

    @staticmethod
    def get_rank_from_pos(a_pos):
        """Returns the rank from the passed pos."""

        if len(a_pos) == 2:
            rank = a_pos[1]
        else:
            rank = a_pos[1] + a_pos[2]

        return rank
