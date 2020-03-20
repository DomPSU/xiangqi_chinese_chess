# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a soldier piece in the game Xiangqi. Inherits from Piece.


from Piece import Piece


class Soldier(Piece):
    """Represents a soldier piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        Piece.__init__(self, color, "S", possible_moves)
