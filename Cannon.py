# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a cannon piece in the game Xiangqi. Inherits from Piece.


from Piece import Piece


class Cannon(Piece):
    """"Represents a cannon piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = []
        possible_jumps = []

        for num in range(9):
            possible_moves.append([num + 1, 0])
            possible_jumps.append(self.find_jumps(num + 1, 0))

        for num in range(9):
            possible_moves.append([-1 - num, 0])
            possible_jumps.append(self.find_jumps(-1 - num, 0))

        for num in range(9):
            possible_moves.append([0, num + 1])
            possible_jumps.append(self.find_jumps(0, num + 1))

        for num in range(9):
            possible_moves.append([0, -1 - num])
            possible_jumps.append(self.find_jumps(0, -1 - num))

        Piece.__init__(self, color, "C", possible_moves, possible_jumps)

    @staticmethod
    def find_jumps(file_index, rank_index):
        """Returns the jumps indexes required to react the passed file_index and rank_index."""

        jumps = []

        if file_index == 0 and rank_index < 0:
            rank_index += 1

            while rank_index != 0:
                jumps.insert(0, [0, rank_index])
                rank_index += 1

            return jumps

        elif file_index == 0 and rank_index > 0:
            rank_index -= 1

            while rank_index != 0:
                jumps.insert(0, [0, rank_index])
                rank_index -= 1

            return jumps

        elif file_index < 0 and rank_index == 0:
            file_index += 1

            while file_index != 0:
                jumps.insert(0, [file_index, 0])
                file_index += 1

            return jumps

        elif file_index > 0 and rank_index == 0:
            file_index -= 1

            while file_index != 0:
                jumps.insert(0, [file_index, 0])
                file_index -= 1

            return jumps

        return None
