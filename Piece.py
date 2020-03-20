# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a general piece in the game Xiangqi.


class Piece:
    """Represents a general piece in the game Xiangqi."""

    def __init__(self, color, symbol, possible_moves, possible_jumps=None):
        """Initializes the piece with the passed color, symbol, possible_moves and possible_jumps."""

        self.__color = color
        self.__symbol = symbol
        self.__possible_moves = possible_moves
        self.__possible_jumps = possible_jumps

    def get_color(self):
        """Getter for color"""

        return self.__color

    def get_symbol(self):
        """Getter for symbol"""

        return self.__symbol

    def get_possible_moves(self):
        """Returns an array of indices of the moves possible with the piece and no restrictions."""

        return self.__possible_moves

    def get_possible_jumps(self):
        """Returns a nested array of arrays for the jumps possible with the piece and no restrictions"""

        return self.__possible_jumps


