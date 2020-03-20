# Author: Dominic Lupo
# Date: 03/12/20
# Description: Represents a game of Xiangqi. Contains logic for determining if a move is valid. A move is valid based on
#              general piece restrictions and specific piece restrictions. If a move is called and is valid the move is
#              processed. The game state is automatically updated to determine the winner.""


class XiangqiGame:
    """Represents a game of Xiangqi. Contains logic for determining if a move is valid. A move is valid based on general
    piece restrictions and specific piece restrictions. If a move is called and is valid the move is processed. The game
    state is automatically updated to determine the winner."""

    def __init__(self):
        """
        Initializes the XiangqiGame without a winner, a board with placed starting pieces, the red player starting and
        the black player going second.
        """

        self.__game_state = "UNFINISHED"
        self.__board = Board()
        self.__player_one = Player("red")
        self.__player_two = Player("black")
        self.__current_player = self.__player_one

    def get_current_player(self):
        """Getter for current_player."""

        return self.__current_player

    def get_board(self):
        """Getter for board."""

        return self.__board

    def get_game_state(self):
        """Getter for game_state."""

        return self.__game_state

    def switch_current_player(self):
        """Switches the current player."""

        if self.__current_player == self.__player_one:
            self.__current_player = self.__player_two
        else:
            self.__current_player = self.__player_one

        return None

    def all_pieces_pos_array(self, color):
        """Returns an array of all positions on the board with pieces of the passed color."""

        piece_pos_array = []
        point_array = self.__board.get_point_array()

        for point in point_array:
            if point.get_piece() is not None:
                if point.get_piece().get_color() == color:

                    piece_pos_array.append(point.get_file() + point.get_rank())

        return piece_pos_array

    def piece_move_change_array(self, a_pos):
        """
        Returns an array of arrays. The nested array contains the change in file and rank index possible with the piece
        located at the passed position.
        """

        point = self.__board.get_point_with_pos(a_pos)
        piece = point.get_piece()

        if piece is None:
            possible_moves = [[]]  # Return an empty nested array if the passed position has no piece located on it.
        else:
            possible_moves = piece.get_possible_moves()

        return possible_moves

    def piece_jump_change_array(self, a_pos):
        """
        Returns a nested array of arrays. The nested array contains an array of the change in file and rank index needed
        to perform the jump for the corresponding move.
        """

        point = self.__board.get_point_with_pos(a_pos)
        piece = point.get_piece()

        if piece is None:
            possible_jumps = None
        else:
            possible_jumps = piece.get_possible_jumps()

        return possible_jumps

    def convert_moves(self, start_pos, piece_move_array):
        """
        Returns converted_end_pos for the passed start_pos and piece_move_array. The conversion converts indices into
        positions.
        """

        if piece_move_array is []:
            return []

        converted_end_pos = []

        board = self.__board
        file_array = board.get_file_array()
        rank_array = board.get_rank_array()

        start_file_index = board.get_file_index_from_pos(start_pos)
        start_rank_index = board.get_rank_index_from_pos(start_pos)

        for move in piece_move_array:
            file_index_change = move[0]
            rank_index_change = move[1]

            end_file_index = start_file_index + file_index_change
            end_rank_index = start_rank_index + rank_index_change

            end_file = file_array[end_file_index]
            end_rank = rank_array[end_rank_index]

            end_pos = end_file + end_rank

            converted_end_pos.append(end_pos)

        return converted_end_pos

    def convert_jumps(self, start_pos, jumps_arrays):
        """
        Returns converted_end_pos for the passed start_pos and jumps_arrays. The conversion converts indices into
        positions.
        """

        if jumps_arrays is None:
            return None

        converted_end_pos = []

        board = self.__board
        file_array = board.get_file_array()
        rank_array = board.get_rank_array()

        start_file_index = board.get_file_index_from_pos(start_pos)
        start_rank_index = board.get_rank_index_from_pos(start_pos)

        for a_jump_array in jumps_arrays:

            converted_end_pos.append([])

            for move in a_jump_array:

                file_index_change = move[0]
                rank_index_change = move[1]

                end_file_index = start_file_index + file_index_change
                end_rank_index = start_rank_index + rank_index_change

                end_file = file_array[end_file_index]
                end_rank = rank_array[end_rank_index]

                end_pos = end_file + end_rank

                converted_end_pos[-1].append(end_pos)

        return converted_end_pos

    def board_restriction(self, start_pos, piece_move_array, jumps_arrays):
        """
        Returns a tuple containg restricted_moves and restricted jumps after the board boundary restriction has been
        applied.
        """

        if not piece_move_array:
            return [], None

        restricted_moves = []
        restricted_jumps = []

        board = self.__board

        start_file_index = board.get_file_index_from_pos(start_pos)
        start_rank_index = board.get_rank_index_from_pos(start_pos)

        move_index = 0

        # check if move file index and move rank index is outside file_array and rank_array index from Board class.
        for move in piece_move_array:
            file_index_change = move[0]
            rank_index_change = move[1]

            end_file_index = start_file_index + file_index_change
            end_rank_index = start_rank_index + rank_index_change

            if board.valid_file_index(end_file_index) and board.valid_rank_index(end_rank_index):
                restricted_moves.append(piece_move_array[move_index])

                if jumps_arrays is not None:
                    restricted_jumps.append(jumps_arrays[move_index])

            move_index += 1

        return restricted_moves, restricted_jumps

    def color_restriction(self, start_pos, end_pos_array, jumps_arrays=None):
        """
        Returns a tuple containing restricted_end_pos and restricted jumps for the passed start_pos, end_pos_array and
        jumps_array after the color restriction has been applied.
        """

        if not end_pos_array:
            return [], None

        restricted_end_pos = []
        restricted_jumps = []

        board = self.__board
        start_point = board.get_point_with_pos(start_pos)
        piece = start_point.get_piece()
        piece_color = piece.get_color()

        pos_index = 0

        # end_pos is not valid if start_pos and end_pos have same color pieces.
        for end_pos in end_pos_array:

            end_point = board.get_point_with_pos(end_pos)
            end_piece = end_point.get_piece()

            if end_piece is None:
                restricted_end_pos.append(end_pos_array[pos_index])

                if jumps_arrays != [] and jumps_arrays is not None:
                    restricted_jumps.append(jumps_arrays[pos_index])

            elif end_piece is not None:
                end_piece_color = end_piece.get_color()

                if piece_color is not end_piece_color:
                    restricted_end_pos.append(end_pos_array[pos_index])

                    if jumps_arrays != [] and jumps_arrays is not None:
                        restricted_jumps.append(jumps_arrays[pos_index])

            pos_index += 1

        return restricted_end_pos, restricted_jumps

    def jump_restriction(self, end_pos_array, jump_arrays=None):
        """
        Returns a tuple containing restricted_end_pos and restricted_jumps for the passed end_pos array and jumps_array
        once jump restriction has been applied.
        """

        if not end_pos_array:
            return [], None

        restricted_end_pos = []
        restricted_jumps = []

        board = self.__board

        jump_index = 0

        for a_jump_array in jump_arrays:
            piece_in_jump_array = False

            # check all position in jump array if a piece is located at the position
            for a_pos in a_jump_array:

                point = board.get_point_with_pos(a_pos)
                piece = point.get_piece()

                if piece is not None:
                    piece_in_jump_array = True

            # move is valid if all jump pos in a_jump_array do not contain pieces
            if not piece_in_jump_array:
                restricted_end_pos.append(end_pos_array[jump_index])

                if jump_arrays is not None:
                    restricted_jumps.append(jump_arrays[jump_index])

            jump_index += 1

        return restricted_end_pos, restricted_jumps

    def castle_restriction(self, start_pos, end_pos_array):
        """
        Returns restricted end_pos for the passed start_pos and end_pos_array after castle restriction has been applied.
        """

        restricted_end_pos = []

        board = self.__board
        red_castle_array = board.get_red_castle_array()
        black_castle_array = board.get_black_castle_array()

        # add move if piece is moving within on own castle
        for end_pos in end_pos_array:
            if start_pos in red_castle_array and end_pos in red_castle_array:
                restricted_end_pos.append(end_pos)
            elif start_pos in black_castle_array and end_pos in black_castle_array:
                restricted_end_pos.append(end_pos)

        return restricted_end_pos

    def elephant_restriction(self, start_pos, end_pos_array, jump_pos_array=None):
        """
        Returns restricted_end_pos for the passed start_pos, end_pos_array and jump_pos_array after elephant
        restrictions have been applied.
        """

        restricted_end_pos = []
        restricted_jumps = []

        board = self.__board
        red_side_array = board.get_red_side_array()
        black_side_array = board.get_black_side_array()

        index = 0

        # elephant move is valid if it is  moving within own side.
        for end_pos in end_pos_array:
            if start_pos in red_side_array and end_pos in red_side_array:
                restricted_end_pos.append(end_pos)
                restricted_jumps.append(jump_pos_array[index])
            elif start_pos in black_side_array and end_pos in black_side_array:
                restricted_end_pos.append(end_pos)
                restricted_jumps.append(jump_pos_array[index])

            index += 1

        return restricted_end_pos

    def soldier_restriction(self, start_pos, end_pos_array):
        """
        Returns restricted_end_pos for the passed start_pos, end_pos_array after soldier restrictions have been applied.
        """

        restricted_end_pos = []

        board = self.__board
        start_point = board.get_point_with_pos(start_pos)
        piece = start_point.get_piece()
        soldier_color = piece.get_color()
        start_rank = board.get_rank_from_pos(start_pos)

        for end_pos in end_pos_array:
            end_rank = board.get_rank_from_pos(end_pos)

            if soldier_color == "red":
                soldier_across_river = start_pos in board.get_black_side_array()

                if end_rank > start_rank:
                    restricted_end_pos.append(end_pos)  # soldier move is valid if moving towards black side
                elif end_rank == start_rank and soldier_across_river is True:
                    restricted_end_pos.append(end_pos)  # horizontal soldier move is valid if on black side

            elif soldier_color == "black":
                soldier_across_river = start_pos in board.get_red_side_array()

                if end_rank < start_rank:
                    restricted_end_pos.append(end_pos)  # soldier move is valid if moving towards red side
                elif end_rank == start_rank and soldier_across_river is True:
                    restricted_end_pos.append(end_pos)  # horizontal soldier move is valid if on red side

        return restricted_end_pos

    def cannon_restriction(self, start_pos, end_pos_array, jump_arrays=None):
        """
        Returns a tuple containing restricted_end_pos and restricted jumps for the passed start_pos, end_pos_array and
        jumps_arrays after cannon restrictions have been applied.
        """

        if not end_pos_array:
            return [], None

        restricted_end_pos = []
        restricted_jumps = []

        board = self.__board
        start_point = board.get_point_with_pos(start_pos)
        start_piece = start_point.get_piece()
        start_piece_color = start_piece.get_color()

        jump_index = 0

        for a_jump_array in jump_arrays:
            piece_in_jump_array_count = 0

            for a_pos in a_jump_array:

                point = board.get_point_with_pos(a_pos)
                piece = point.get_piece()

                if piece is not None:
                    piece_in_jump_array_count += 1

            end_pos = end_pos_array[jump_index]
            end_point = board.get_point_with_pos(end_pos)
            end_piece = end_point.get_piece()

            # cannon move is valid if it is only jumping one piece and is capturing opposing piece.
            if piece_in_jump_array_count == 1 and end_piece is not None:
                end_piece_color = end_piece.get_color()

                if start_piece_color != end_piece_color:
                    restricted_end_pos.append(end_pos_array[jump_index])

                    if jump_arrays is not None:
                        restricted_jumps.append(jump_arrays[jump_index])

            # cannon move is valid if it is not jumping any pieces and is not capturing any piece.
            elif piece_in_jump_array_count == 0 and end_piece is None:
                restricted_end_pos.append(end_pos_array[jump_index])

                if jump_arrays is not None:
                    restricted_jumps.append(jump_arrays[jump_index])

            jump_index += 1

        return restricted_end_pos, restricted_jumps

    def generals_facing(self):
        """Returns True if generals are facing, returns False otherwise."""

        board = self.__board
        red_pos_array = self.all_pieces_pos_array("red")
        red_general_pos = None

        # set reg_general_pos by checking all red position pieces
        for pos in red_pos_array:
            point = board.get_point_with_pos(pos)
            piece = point.get_piece()
            piece_symbol = piece.get_symbol()

            if piece_symbol == "G":
                red_general_pos = pos

        # special case where red king was captured with simulated move
        if red_general_pos is None:
            return False

        end_file = board.get_file_from_pos(red_general_pos)
        end_rank_index = board.get_rank_index_from_pos(red_general_pos)

        sight_index = 1

        current_sighted_pos = end_file + board.get_rank_array()[end_rank_index + sight_index]
        current_sighted_point = board.get_point_with_pos(current_sighted_pos)
        current_sighted_piece = current_sighted_point.get_piece()

        # check positions in front of red General for black General until a piece is sighted or end of board is reached.
        while current_sighted_piece is None:
            sight_index += 1

            if board.valid_rank_index(end_rank_index + sight_index) is False:
                return False

            current_sighted_pos = end_file + board.get_rank_array()[end_rank_index + sight_index]
            current_sighted_point = board.get_point_with_pos(current_sighted_pos)
            current_sighted_piece = current_sighted_point.get_piece()

        current_sighted_piece_symbol = current_sighted_piece.get_symbol()

        if current_sighted_piece_symbol == "G":
            return True
        else:
            return False

    def get_valid_end_pos_array(self, start_pos, piece_symbol):
        """
        Returns an array containing valid end positions from the passed start_pos and piece_symbol. All restrictions
        limits end positions except checkmate.
        """

        move_change_array = self.piece_move_change_array(start_pos)
        jump_change_array = self.piece_jump_change_array(start_pos)

        # perform restrictions for all pieces except checkmate restriction and generals looking restriction
        valid_moves_and_jumps = self.all_piece_restrictions(start_pos, move_change_array, jump_change_array)

        # perform piece specific restrictions
        if piece_symbol == "G":
            valid_moves = self.castle_restriction(start_pos, valid_moves_and_jumps[0])

        elif piece_symbol == "A":
            valid_moves = self.castle_restriction(start_pos, valid_moves_and_jumps[0])

        elif piece_symbol == "E":
            valid_moves_and_jumps = self.jump_restriction(valid_moves_and_jumps[0], valid_moves_and_jumps[1])
            valid_moves = self.elephant_restriction(start_pos, valid_moves_and_jumps[0], valid_moves_and_jumps[1])

        elif piece_symbol == "H":
            valid_moves = self.jump_restriction(valid_moves_and_jumps[0], valid_moves_and_jumps[1])[0]

        elif piece_symbol == "R":
            valid_moves = self.jump_restriction(valid_moves_and_jumps[0], valid_moves_and_jumps[1])[0]

        elif piece_symbol == "S":
            valid_moves = self.soldier_restriction(start_pos, valid_moves_and_jumps[0])

        elif piece_symbol == "C":
            valid_moves = self.cannon_restriction(start_pos, valid_moves_and_jumps[0], valid_moves_and_jumps[1])[0]
        else:
            valid_moves = None

        valid_moves = self.generals_facing_restriction(start_pos, valid_moves)

        return valid_moves

    def generals_facing_restriction(self, start_pos, end_pos_array):
        """
        Returns restricted_end_pos that removes end_pos from the passed start_pos and end_pos_array that cause
        Generals to face each other.
        """

        restricted_end_pos = []
        board = self.__board

        # save start_point and start_piece
        start_point = board.get_point_with_pos(start_pos)
        start_piece = start_point.get_piece()

        for end_pos in end_pos_array:

            # save end_point and end_piece
            end_point = board.get_point_with_pos(end_pos)
            end_piece = end_point.get_piece()

            # simulate move
            self.move_piece(start_pos, end_pos)

            if self.generals_facing() is False:
                restricted_end_pos.append(end_pos)

            self.reverse_move(start_point, start_piece, end_point, end_piece)

        return restricted_end_pos

    def all_piece_restrictions(self, start_pos, a_move_change_array, a_jump_change_array):
        """
        Returns a tuple of valid_move_pos and valid_jump_pos. These values are found by performing restrictions that
        affect all pieces in Xiangqi from the passed start_pos, a_move_change_array and a_jump_change_array.
        """

        # Remove move and jumps that are beyond board boundaries
        valid_move_changes, valid_jump_changes = self.board_restriction(start_pos, a_move_change_array,
                                                                        a_jump_change_array)

        # convert changes in position to end positions
        valid_move_pos = self.convert_moves(start_pos, valid_move_changes)
        valid_jump_pos = self.convert_jumps(start_pos, valid_jump_changes)

        # Remove move and jumps that land on same color as the start position piece color
        valid_move_pos, valid_jump_pos = self.color_restriction(start_pos, valid_move_pos, valid_jump_pos)

        return valid_move_pos, valid_jump_pos

    def valid_move(self, start_pos, end_pos, player_color):
        """
        Returns True if a piece located at the passed start_pos is the same color as the passed player_color and can
        move to the passed end_pos.
        """

        board = self.__board

        # if start position does not exist return no valid end positions.
        if board.get_point_with_pos(start_pos) is None:
            return False

        point = board.get_point_with_pos(start_pos)
        piece = point.get_piece()

        # if start position has no piece return no valid en positions.
        if piece is None:
            return False

        piece_color = piece.get_color()

        # if the piece at start_position does not have the same color as player color
        if piece_color != player_color:
            return False

        piece_symbol = piece.get_symbol()

        valid_end_pos_array = self.get_valid_end_pos_array(start_pos, piece_symbol)

        if end_pos not in valid_end_pos_array:
            return False

        return True

    @staticmethod
    def reverse_move(start_point, start_piece, end_point, end_piece):
        """Uses the passed start_point, start_piece, end_point and end_piece to reverse simulated moves."""

        start_point.set_piece(start_piece)
        end_point.set_piece(end_piece)

        return None

    def move_piece(self, start_pos, end_pos):
        """Moves the piece at the passed start_pos to the passed end_pos."""

        board = self.__board
        start_point = board.get_point_with_pos(start_pos)
        start_piece = start_point.get_piece()
        end_point = board.get_point_with_pos(end_pos)

        # make desired move and remove captured piece
        end_point.set_piece(start_piece)
        start_point.set_piece(None)

    def make_move(self, start_pos, end_pos):
        """Returns True if the passed start_pos and end_pos is valid for a piece. Returns False otherwise."""

        board = self.__board

        # if the game is over return False
        if self.game_over():
            return False

        # if the move is invalid return False
        if self.valid_move(start_pos, end_pos, self.__current_player.get_color()) is False:
            return False

        # simulate move
        start_point = board.get_point_with_pos(start_pos)
        start_piece = start_point.get_piece()
        end_point = board.get_point_with_pos(end_pos)
        end_piece = end_point.get_piece()

        self.move_piece(start_pos, end_pos)

        # if the move causes check return False
        if self.is_in_check(self.__current_player.get_color()):
            self.reverse_move(start_point, start_piece, end_point, end_piece)
            return False

        # move is valid, complete move
        self.switch_current_player()
        self.update_game_state()

        return True

    def update_game_state(self):
        """Sets game_state when current_player is either checkmated or stalemated."""

        current_player_color = self.__current_player.get_color()

        # check for checkmate
        if self.is_in_check(current_player_color) and self.checkmate_preventable() is False:
            self.current_player_lost()

        if self.stalemate() is True:
            self.current_player_lost()

        return None

    def current_player_lost(self):
        """Determines game_state when current_player loses."""

        current_player_color = self.__current_player.get_color()

        if current_player_color is "red":
            self.__game_state = "BLACK_WON"
        else:
            self.__game_state = "RED_WON"

        return None

    def stalemate(self):
        """Returns True if the current_player is in stalemate. Returns False otherwise."""

        current_player_color = self.__current_player.get_color()

        board = self.__board
        player_color_piece_pos_array = self.all_pieces_pos_array(current_player_color)
        move_available = False

        # check all pieces
        for start_pos in player_color_piece_pos_array:
            start_point = board.get_point_with_pos(start_pos)
            start_piece = start_point.get_piece()
            start_piece_symbol = start_piece.get_symbol()

            valid_end_pos_array = self.get_valid_end_pos_array(start_pos, start_piece_symbol)

            # simulate move to check if move would cause check
            start_point = board.get_point_with_pos(start_pos)
            start_piece = start_point.get_piece()

            # check all end positions for piece
            for end_pos in valid_end_pos_array:

                end_point = board.get_point_with_pos(end_pos)
                end_piece = end_point.get_piece()

                self.move_piece(start_pos, end_pos)

                if not self.is_in_check(current_player_color):
                    move_available = True

                self.reverse_move(start_point, start_piece, end_point, end_piece)

        if move_available is False:
            stalemate = True
        else:
            stalemate = False

        return stalemate

    def checkmate_preventable(self):
        """TODO"""

        current_player_color = self.__current_player.get_color()

        board = self.__board
        player_color_piece_pos_array = self.all_pieces_pos_array(current_player_color)

        for start_pos in player_color_piece_pos_array:
            start_point = board.get_point_with_pos(start_pos)
            start_piece = start_point.get_piece()
            start_piece_symbol = start_piece.get_symbol()

            valid_end_pos_array = self.get_valid_end_pos_array(start_pos, start_piece_symbol)

            for end_pos in valid_end_pos_array:

                # simulate move
                start_point = board.get_point_with_pos(start_pos)
                start_piece = start_point.get_piece()
                end_point = board.get_point_with_pos(end_pos)
                end_piece = end_point.get_piece()

                self.move_piece(start_pos, end_pos)

                if self.is_in_check(current_player_color) is False:
                    self.reverse_move(start_point, start_piece, end_point, end_piece)
                    return True

                self.reverse_move(start_point, start_piece, end_point, end_piece)

        return False

    def game_over(self):
        """Returns True if red or black has won. Return False otherwise."""

        if self.__game_state == "RED_WON" or self.__game_state == "BLACK_WON":
            game_over = True
        else:
            game_over = False

        return game_over

    def is_in_check(self, player_color):
        """Returns True if the passed player_color is in check. Returns False otherwise."""

        board = self.__board
        opposing_player_color = self.opposing_player_color(player_color)
        opposing_player_color_piece_pos_array = self.all_pieces_pos_array(opposing_player_color)

        # if any move from opposing player can capture passed player_color general return True

        # check all pieces
        for start_pos in opposing_player_color_piece_pos_array:
            start_point = board.get_point_with_pos(start_pos)
            start_piece = start_point.get_piece()
            start_piece_symbol = start_piece.get_symbol()

            valid_end_pos_array = self.get_valid_end_pos_array(start_pos, start_piece_symbol)

            # check all end positions for piece
            for end_pos in valid_end_pos_array:
                end_point = board.get_point_with_pos(end_pos)
                end_piece = end_point.get_piece()

                if end_piece is not None:
                    end_piece_color = end_piece.get_color()
                    end_piece_symbol = end_piece.get_symbol()

                    if end_piece_symbol == "G" and end_piece_color == player_color:
                        return True
        return False

    @staticmethod
    def opposing_player_color(player_color):
        """Returns the color of the opposing player for the passed player_color."""

        if player_color == "red":
            opposing_player_color = "black"
        else:
            opposing_player_color = "red"

        return opposing_player_color


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a board for the game Xiangqi.


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


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a general piece in the game Xiangqi. Inherits from Piece.


class General(Piece):
    """Represents a general piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        Piece.__init__(self, color, "G", possible_moves)


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines an advisor piece in the game Xiangqi. Inherits from Piece.


class Advisor(Piece):
    """Represents an advisor piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[1, 1], [-1, 1], [-1, -1], [1, -1]]

        Piece.__init__(self, color, "A", possible_moves)


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines an elephant piece in the game Xiangqi. Inherits from Piece.


class Elephant(Piece):
    """Represents an elephant piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
        possible_jumps = [[[1, 1]], [[1, -1]], [[-1, 1]], [[-1, -1]]]

        Piece.__init__(self, color, "E", possible_moves, possible_jumps)


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a horse piece in the game Xiangqi. Inherits from Piece.


class Horse(Piece):
    """Represents a horse piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color.."""

        possible_moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
        possible_jumps = [[[1, 0]], [[0, 1]], [[0, 1]], [[-1, 0]], [[-1, 0]], [[0, -1]], [[0, -1]], [[1, 0]]]

        Piece.__init__(self, color, "H", possible_moves, possible_jumps)

# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a chariot piece in the game Xiangqi. Inherits from Piece.


class Chariot(Piece):
    """Represents a chariot piece in the game Xiangqi."""

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

        Piece.__init__(self, color, "R", possible_moves, possible_jumps)

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


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a soldier piece in the game Xiangqi. Inherits from Piece.


class Soldier(Piece):
    """Represents a soldier piece in the game Xiangqi."""

    def __init__(self, color):
        """Initializes the piece with the passed color."""

        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        Piece.__init__(self, color, "S", possible_moves)


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a chariot piece in the game Xiangqi. Inherits from Piece.


class Chariot(Piece):
    """Represents a chariot piece in the game Xiangqi."""

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

        Piece.__init__(self, color, "R", possible_moves, possible_jumps)

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


# Author: Dominic Lupo
# Date: 03/12/20
# Description: Defines a cannon piece in the game Xiangqi. Inherits from Piece.


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

