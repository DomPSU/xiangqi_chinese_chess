# Author: Dominic Lupo
# Date: 03/12/20
# Description: Represents a game of Xiangqi. Contains logic for determining if a move is valid. A move is valid based on
#              general piece restrictions and specific piece restrictions. If a move is called and is valid the move is
#              processed. The game state is automatically updated to determine the winner.""


from Board import Board
from Player import Player


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
