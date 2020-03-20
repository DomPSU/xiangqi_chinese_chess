# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a horse piece in the game Xiangqi. Inherits from Piece.


from Piece import Piece


class Horse(Piece):
    """Represents a horse piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color.."""

        possible_moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
        possible_jumps = [[[1, 0]], [[0, 1]], [[0, 1]], [[-1, 0]], [[-1, 0]], [[0, -1]], [[0, -1]], [[1, 0]]]

        Piece.__init__(self, color, "H", possible_moves, possible_jumps)
