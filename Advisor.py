# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines an advisor piece in the game Xiangqi. Inherits from Piece.


from Piece import Piece


class Advisor(Piece):
    """Represents an advisor piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

        Piece.__init__(self, color, "A", possible_moves)
