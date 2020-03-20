# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines an elephant piece in the game Xiangqi. Inherits from Piece.


from Piece import Piece


class Elephant(Piece):
    """Represents an elephant piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
        possible_jumps = [[[1, 1]], [[1, -1]], [[-1, 1]], [[-1, -1]]]

        Piece.__init__(self, color, "E", possible_moves, possible_jumps)
