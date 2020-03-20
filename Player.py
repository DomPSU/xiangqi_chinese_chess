# Author: Dominic Lupo
# Date: 03/12/2020
# Description: Defines a Player in the game Xiangqi.


class Player:
    """Represents a player in the game Xiangqi."""

    def __init__(self, color):
        """Initialize the Player with the passed color."""

        self.__color = color

    def get_color(self):
        """Getter for color."""

        return self.__color
