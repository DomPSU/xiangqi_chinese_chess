# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a point in the game Xiangqi.


class Point:
    """Represents a point in the game Xiangqi."""

    def __init__(self, file, rank):
        """Initializes the point with the passed file and rank. Set the piece at point to None."""

        self.__file = file
        self.__rank = rank
        self.__piece = None

    def get_file(self):
        """Getter for file."""

        return self.__file

    def get_rank(self):
        """Getter for rank."""

        return self.__rank

    def get_pos(self):
        """Returns file and rank together."""

        return self.__file + self.__rank

    def get_piece(self):
        """Getter for piece."""

        return self.__piece

    def set_piece(self, piece):
        """Setter for piece."""

        self.__piece = piece

    def get_symbol(self):
        """Returns default point symbol + unless a piece is located at point."""

        if self.__piece is None:
            return "+"
        else:
            return self.__piece.get_symbol()
