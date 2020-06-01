# Author: Ryan Jensen
# Date: May 18th, 2020
# Description: Implementation of Gess, a GO/Chess hybrid game. The game is played on an 18x18 grid of squares, with each
# player owning 43 stones, represented with "B" for the black stones and "W" for the white stones. "E" represents empty
# spots but a method in the GessGame class be used to alter that to user's preference. Moves are made by declaring the
# center of a 3x3 stone grid on the board and the center of the desired destination of that 3x3 grid, which is referred
# to as a footprint. Players take turns declaring moves, starting with the Black player first.
#
# Once the center piece of a footprint is declared, the class has access to the coordinates of all 9 squares that make
# up the footprint. Each time a move is made, the move is checked for validity in terms of spaces moved, direction,
# valid footprint, etc. Invalid moves return False, and print a message declaring the issue, while valid moves simply
# return True. Once a move is confirmed valid, it is executed and the game checks if a player has won. A player
# wins when the opposing player has no 'rings' or 'circles' of 8 stones all owned by the player, with an empty center.
# Detailed rules can be found at {{https://www.chessvariants.com/crossover.dir/gess.html}}.

from termcolor import colored


class Footprint:
    """Represents a footprint object, which is a 3x3 square section of the board that makes up a piece. Contains data
    attributes that consist of the locations of the center square and the locations of the 9 squares that
    make up the footprint.
    """

    def to_grid_coordinate(self):
        """Takes in user inputted string coordinates and returns coordinates in (row, column) format, in
        order to make them usable for the logic of the other class methods and make_move function of GessGame.
        """

        # Assigns numerical values to the letter values which represents columns.
        column_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10,
                       "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19}

        # Grabs first letter of coordinate and gets the column number from the above dictionary.
        column = column_dict[self._center_coordinates[0]]
        # Row coordinate looks at the rest of the characters of the entered location to locate the row.
        row = 20 - int(self._center_coordinates[1:])

        coordinates = [row, column]

        return coordinates

    def to_full_footprint(self):
        """Returns a list of the coordinates of the 9 squares that compose the footprint."""

        foot_print_coordinates = []
        center = self._center_grid_coordinates
        northwest = [center[0] - 1, center[1] - 1]
        west = [center[0], center[1] - 1]
        southwest = [center[0] + 1, center[1] - 1]
        south = [center[0] + 1, center[1]]
        north = [center[0] - 1, center[1]]
        northeast = [center[0] - 1, center[1] + 1]
        east = [center[0], center[1] + 1]
        southeast = [center[0] + 1, center[1] + 1]

        directions = [center, northwest, west, southwest, south, north, northeast, east, southeast]

        for direction in directions:
            foot_print_coordinates.append(direction)

        return foot_print_coordinates

    def __init__(self, center_coordinates):
        """Initialized using user-entered coordinates, defines the entire footprint and area surrounding the center
        using the above functions after converting the user input to grid format in order to be used in the logic of the
        make_move function in GessGame.
        """
        self._center_coordinates = center_coordinates
        self._center_grid_coordinates = self.to_grid_coordinate()
        self._footprint_coordinates = self.to_full_footprint()

    def get_center_coordinates(self):
        return self._center_grid_coordinates

    def get_footprint_coordinates(self):
        return self._footprint_coordinates

    def set_center_coordinates(self, center_coordinates):
        """Takes in coordinates in [4,5] format to create Footprints using non-user input. Not to be used by players."""
        self._center_grid_coordinates = center_coordinates

    def __repr__(self):
        """Represent footprints using player friendly coordinate notation. ex. ('b6')"""
        return self._center_coordinates


class GessGame:
    """Handle the playing of Gess. Has attributes to track the current player and player who is waiting for their turn,
    the current game state, which is updated as moves are made, the empty placeholder, which is a cosmetic attribute
    that can be altered in order to make the board look different to the players, and a game board set up with "B"
    representing black stones, "W" representing white stones, and "E" representing empty spaces. Resign game can be
     called to forfeit the game, and make_move handles the logic of the turn by turn playing of Gess.
     """

    def __init__(self):
        """Initializes a GessGame starting board with empty spaces represented with "E", white pieces with "W", black
        pieces with "B", the current player's to the black player, and sets the current game state to UNFINISHED.
        """
        # Cosmetics
        self._empty_placeholder = "E"
        self._labels_color = 'yellow'
        self._info_text_color = 'blue'
        self._warning_text_color = 'red'
        self._instruction_text_color = 'green'

        # Game logic
        self._game_state = "UNFINISHED"
        self._current_player = "BLACK"
        self._waiting_player = "WHITE"
        self._board = [
           #  a    b    c    d    e    f    g    h    i    j    k    l    m    n    o    p    q    r    s    t
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 20
            ["E", "E", "W", "E", "W", "E", "W", "W", "W", "W", "W", "W", "W", "W", "E", "W", "E", "W", "E", "E"],  # 19
            ["E", "W", "W", "W", "E", "W", "E", "W", "W", "W", "W", "E", "W", "E", "W", "E", "W", "W", "W", "E"],  # 18
            ["E", "E", "W", "E", "W", "E", "W", "W", "W", "W", "W", "W", "W", "W", "E", "W", "E", "W", "E", "E"],  # 17
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 16
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 15
            ["E", "E", "W", "E", "E", "W", "E", "E", "W", "E", "E", "W", "E", "E", "W", "E", "E", "W", "E", "E"],  # 14
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 13
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 12
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 11
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 10
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 9
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 8
            ["E", "E", "B", "E", "E", "B", "E", "E", "B", "E", "E", "B", "E", "E", "B", "E", "E", "B", "E", "E"],  # 7
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 6
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 5
            ["E", "E", "B", "E", "B", "E", "B", "B", "B", "B", "B", "B", "B", "B", "E", "B", "E", "B", "E", "E"],  # 4
            ["E", "B", "B", "B", "E", "B", "E", "B", "B", "B", "B", "E", "B", "E", "B", "E", "B", "B", "B", "E"],  # 3
            ["E", "E", "B", "E", "B", "E", "B", "B", "B", "B", "B", "B", "B", "B", "E", "B", "E", "B", "E", "E"],  # 2
            ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],  # 1
        ]

    def get_game_state(self):
        return self._game_state

    def set_game_state(self, state):
        self._game_state = state

    def set_current_player(self, player):
        self._current_player = player

    def set_waiting_player(self, player):
        self._waiting_player = player

    def get_current_player(self):
        return self._current_player

    def get_waiting_player(self):
        return self._waiting_player

    def resign_game(self):
        """Allows the current player to resign the game, altering the game state accordingly. Returns the game_over
        function with updated game state.
        """

        if self._current_player == "BLACK":
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "BLACK_WON"
        self.game_over()

    def game_over(self):
        """Prints farewell message once game has ended, according to game state."""
        if self._game_state == "WHITE_WON":
            return print("Congratulations white player! You won!")
        elif self._game_state == "BLACK_WON":
            return print("Congratulations black player! You won!")
        elif self._game_state == "UNFINISHED":
            raise ValueError

    def get_current_board(self):
        """Prints current Gess board."""
        for row in self._board:
            print(row)

    def get_playable_board(self):
        """Prints board in user friendly format, including coordinate labels and colors.
        """
        lower_case_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']

        # Color column labels.
        print('   ' + colored(lower_case_letters, self._labels_color))

        # Color row numbers.
        for n, row in enumerate(self._board):
            n = 20 - n
            if n < 10:
                print(colored('0' + str(n), self._labels_color), row)
            else:
                print(colored(n, self._labels_color), row)

    def alter_board_display(self, placeholder):
        """Takes in a character/string to represent the empty spaces and alters the Gess board so the inputted
        character/string is the placeholder for empty spaces when the board is printed. Allows board to be read
        more easily according to user's preference. Returns nothing.
        """

        # Handles if the user attempts to set empty spots to the black or white piece characters.
        if placeholder == "W" or "B":
            placeholder = " "

        for row in self._board:
            for n, i in enumerate(row):
                if i == "E":
                    row[n] = placeholder

        # Resets empty placeholder attribute to user entered placeholder value.
        self._empty_placeholder = placeholder

    def make_move(self, start_footprint, destination_footprint):
        """Takes in the coordinates of the center space of a piece and the desired location for that center space to
        be moved to, in format ('b3', 'c6') if the player wanted to move a piece with a center stone currently located
        at column b, row 3, to column c, row 6. Will create Footprint objects for the start and destination locations.
        Will return true if input is valid, piece is valid, and move is valid. Returns False otherwise.
        """

        # Creates Footprint objects based on user enter coordinates. Raises error and stops move for bad input.
        try:
            start_footprint = Footprint(start_footprint)
            destination_footprint = Footprint(destination_footprint)
        except KeyError:
            print(colored("Bad input! Enter valid coordinates for pieces!", self._warning_text_color))
            return False

        def is_valid_piece():
            """Checks if the current middle location is a valid piece, meaning the 8 squares surrounding it are
            either empty or contain stones owned by the player who is attempting to make the move. If the piece is
            valid, True is returned, otherwise returns False.
            """

            piece_coordinates = start_footprint.to_full_footprint()
            current_player_stones = 0

            for adjacent_space in piece_coordinates:
                adjacent_space_x = adjacent_space[0]
                adjacent_space_y = adjacent_space[1]

                # Checks how many stones the player has within the 9 space piece.
                if self._board[adjacent_space_x][adjacent_space_y] == self._current_player[0]:
                    current_player_stones += 1

                # Check that the piece spaces do not contain the opponent's stones.
                if self._board[adjacent_space_x][adjacent_space_y] == self._waiting_player[0]:
                    print(colored("Contains opponents stones, you can't move this footprint!",
                                  self._warning_text_color))
                    return False

            # Checks if player has no stones within the piece and therefor is unable to move it.
            if current_player_stones == 0:
                print(colored("None of your stones are present in this footprint. You can't move this footprint!",
                              self._warning_text_color))
                return False
            return True

        def is_valid_move():
            """Checks for move validity. (User has entered start and destination points that make a valid move.)
            Returns True if move is valid, False if not.
            """

            def spaces_allowed():
                """Checks Footprint for player stone in center space, dictating how many spaces are allowed to move.
                Determines if the player's desired movement is greater than allowed movement.
                """

                # Determines max spaces the piece is allowed to move. (17 if center space is occupied, otherwise 3.)
                if self._board[start_footprint.get_center_coordinates()[0]]\
                    [start_footprint.get_center_coordinates()[1]] == self._current_player[0]:
                    allowed_movement = 17
                else:
                    allowed_movement = 3

                # Compares the start and destination location coordinates to determine if their distance is greater
                # than the allowed movement by that footprint.
                if abs(start_footprint.get_center_coordinates()[0] - destination_footprint.get_center_coordinates()[0])\
                    > allowed_movement or abs(start_footprint.get_center_coordinates()[1] -\
                                              destination_footprint.get_center_coordinates()[1]) > allowed_movement:
                    print(colored("You are trying to move too many spaces!", self._warning_text_color))
                    return False
                else:
                    return True

            def direction_allowed():
                """Checks stones within Footprint to determine which directions the Footprint is allowed to move and
                determines if the user desired direction is allowed. Also checks if the destination is in the path of
                the desired direction. Returns False if the desired direction is invalid. If the desired direction is
                valid, the desired direction is returned.
                """

                start_center = start_footprint.get_center_coordinates()
                dest_center = destination_footprint.get_center_coordinates()

                # Determines desired desired_direction by comparing start and destination center coordinates.
                if start_center[0] == dest_center[0] and start_center[1] > dest_center[1]:
                    desired_direction = "west"
                elif start_center[0] == dest_center[0] and start_center[1] < dest_center[1]:
                    desired_direction = "east"
                elif start_center[0] < dest_center[0] and start_center[1] == dest_center[1]:
                    desired_direction = "south"
                elif start_center[0] > dest_center[0] and start_center[1] == dest_center[1]:
                    desired_direction = "north"
                elif start_center[0] > dest_center[0] and start_center[1] > dest_center[1]:
                    desired_direction = "northwest"
                elif start_center[0] < dest_center[0] and start_center[1] > dest_center[1]:
                    desired_direction = "southwest"
                elif start_center[0] > dest_center[0] and start_center[1] < dest_center[1]:
                    desired_direction = "northeast"
                elif start_center[0] < dest_center[0] and start_center[1] < dest_center[1]:
                    desired_direction = "southeast"
                else:
                    desired_direction = "invalid"

                # Determines the directions a piece is allowed to move, according to which squares are occupied.
                allowed_directions = []

                for index, space in enumerate(start_footprint.get_footprint_coordinates()):
                    if self._board[space[0]][space[1]] == self._current_player[0]:
                        if index == 1:
                            allowed_directions.append("northwest")
                        elif index == 2:
                            allowed_directions.append("west")
                        elif index == 3:
                            allowed_directions.append("southwest")
                        elif index == 4:
                            allowed_directions.append("south")
                        elif index == 5:
                            allowed_directions.append("north")
                        elif index == 6:
                            allowed_directions.append("northeast")
                        elif index == 7:
                            allowed_directions.append("east")
                        elif index == 8:
                            allowed_directions.append("southeast")

                # Checks if desired direction is allowed.
                if desired_direction not in allowed_directions:
                    print(colored("Mismatch of directions! Can't move that way!", self._warning_text_color))
                    return False
                else:
                    return desired_direction

            def obstruction_check(direction):
                """Checks desired path from start-finish of Footprint to see if it is impeded by any stones. Will
                return False if path is obstructed and True if the path is valid."""

                # Uses start and destination coordinates to determine if the path is obstructed.
                start_center = start_footprint.get_center_coordinates()
                dest_center = destination_footprint.get_center_coordinates()

                def from_grid_coordinate(index_format):
                    """Takes in python coordinates (grid/index format) and returns coordinates in 'i3' format, in
                    order to create new instances of the Footprint class.
                    """

                    # Assigns letter values to the numerical values that represent columns.
                    column_dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j",
                                   10: "k", 11: "l", 12: "m", 13: "n", 14: "o", 15: "p", 16: "q", 17: "r", 18: "s",
                                   19: "t"}

                    column = column_dict[index_format[1]]
                    row = 20 - index_format[0]
                    coordinates_readable = str(column) + str(row)

                    return coordinates_readable

                def create_new_center(alter_row, alter_column, input_foot):
                    """Takes in values to alter row/column of center based on desired direction in the directional check
                    function. Produces coordinates for the next footprint center in tracking the movement of a footprint.
                    Returns those coordinates.
                    """

                    row = input_foot.get_center_coordinates()[0] + alter_row
                    column = input_foot.get_center_coordinates()[1] + alter_column

                    return [row, column]

                def directional_check(temp_footprint_input, indices_of_interest, alt_row, alt_column):
                    """Takes in a temporary footprint which represents the first step in the direction the piece
                    is attempting to move, the indices which move to new spaces when a piece moves in the desired
                    direction, and the logic to create a new center in the desired direction in order to move along
                    the board in the desired direction, checking for obstructions. Returns True if no obstructions and
                    False if the path is obstructed or there are invalid directions.
                    """

                    # Create a list of locations to check relevant to movement for specific direction. (The spaces to
                    # check for obstructions in path of the specific direction.)
                    all_location_list = temp_footprint_input.get_footprint_coordinates()
                    key_locations = []
                    for i in indices_of_interest:
                        key_locations.append(all_location_list[i])
                    while True:
                        try:
                            # If arrived at the destination unobstructed, obstruction check passed, returns True.
                            if temp_footprint_input.get_center_coordinates() == dest_center:
                                return True
                            else:
                                # Check squares of temporary footprint that are new with regards to the last footprint.
                                for space in key_locations:
                                    # If space is occupied, movement is obstructed, bad move, returns False.
                                    if self._board[space[0]][space[1]] != self._empty_placeholder:
                                        print(colored("Obstructed path!", self._warning_text_color))
                                        return False
                                # Update temporary center one space in desired direction, create new Footprint, loop.
                                new_center_temp = create_new_center(alt_row, alt_column, temp_footprint_input)
                                new_center_temp = from_grid_coordinate(new_center_temp)
                                temp_footprint_input = Footprint(new_center_temp)
                        # IndexError will catch if the player has entered movement that 'uses multiple directions' such
                        # as a move from n6 to o8, wherein the player is trying to move northeast then north.
                        except IndexError:
                            print(colored("Invalid movement!", self._warning_text_color))
                            return False

                if direction == "southeast":
                    # Defines temporary center and creates Footprint utilizing it, one space to the southeast.
                    temp_center = from_grid_coordinate([start_center[0] + 1, start_center[1] + 1])
                    temp_footprint = Footprint(temp_center)
                    southeast_indices = [3, 4, 6, 7, 8]  # SW(3), S(4), NE(6), E(7) SE(8).

                    return directional_check(temp_footprint, southeast_indices, 1, 1)

                elif direction == "southwest":
                    # Defines temporary center and creates Footprint utilizing it, one space to the southwest.
                    temp_center = from_grid_coordinate([start_center[0] + 1, start_center[1] - 1])
                    temp_footprint = Footprint(temp_center)
                    southwest_indices = [1, 2, 3, 4, 8]  # NW(1), W(2), SW(3), S(4), SE(8).

                    return directional_check(temp_footprint, southwest_indices, 1, -1)

                elif direction == "northwest":
                    # Defines temporary center and creates Footprint utilizing it, one space to the northwest.
                    temp_center = from_grid_coordinate([start_center[0] - 1, start_center[1] - 1])
                    temp_footprint = Footprint(temp_center)
                    northwest_indices = [1, 2, 3, 5, 6]  # NW(1), W(2), SW(3), 5(N), NE(6).

                    return directional_check(temp_footprint, northwest_indices, -1, -1)

                elif direction == "north":
                    # Defines temporary center and creates Footprint utilizing it, one space to the north.
                    temp_center = from_grid_coordinate([start_center[0] - 1, start_center[1]])
                    temp_footprint = Footprint(temp_center)
                    north_indices = [1, 5, 6]  # NW(1), N(5), NE(6).

                    return directional_check(temp_footprint, north_indices, -1, 0)

                elif direction == "northeast":
                    # Defines temporary center and creates Footprint utilizing it, one space to the northeast.
                    temp_center = from_grid_coordinate([start_center[0] - 1, start_center[1] + 1])
                    temp_footprint = Footprint(temp_center)
                    northeast_indices = [1, 5, 6, 7, 8]  # NW(1), N(5), NE(6), E(7), SE(8).

                    return directional_check(temp_footprint, northeast_indices, -1, 1)

                elif direction == "west":
                    # Defines temporary center and creates Footprint utilizing it, one space to the west.
                    temp_center = from_grid_coordinate([start_center[0], start_center[1] - 1])
                    temp_footprint = Footprint(temp_center)
                    west_indices = [1, 2, 3]  # NW(1), W(2), SW(3).

                    return directional_check(temp_footprint, west_indices, 0, -1)

                elif direction == "south":
                    # Defines temporary center and creates Footprint utilizing it, one space to the south.
                    temp_center = from_grid_coordinate([start_center[0] + 1, start_center[1]])
                    temp_footprint = Footprint(temp_center)
                    south_indices = [3, 4, 8]  # SW(3), S(4), SE(8)

                    return directional_check(temp_footprint, south_indices, 1, 0)

                elif direction == "east":
                    # Defines temporary center and creates Footprint utilizing it, one space to the east.
                    temp_center = from_grid_coordinate([start_center[0], start_center[1] + 1])
                    temp_footprint = Footprint(temp_center)
                    east_indices = [6, 7, 8]  # NE(6), E(7), SE(8)

                    return directional_check(temp_footprint, east_indices, 0, 1)

            # Checks if spaces allowed is False, is_valid_move return False if so.
            if not spaces_allowed():
                return False
            # Checks if direction allowed is False, is_valid_move return False if so.
            elif not direction_allowed():
                return False
            else:
                # Uses direction to determine potential path of piece.
                check = obstruction_check(direction_allowed())
                # If path is obstructed, check equals False, and is_valid_move returns False.
                if not check:
                    return False
                # All checks successful, is_valid_move returns True.
                else:
                    return True

        def execute_move():
            """Validated move is executed, altering the pieces on the Gess board accordingly. Returns nothing."""

            # Fill list with 'contents' of the spots in the start space/footprint.
            start_contents = []
            for i in start_footprint.get_footprint_coordinates():
                x = self._board[i[0]][i[1]]
                start_contents.append(x)

            # Set all spots in starting spot to "empty".
            for i in start_footprint.get_footprint_coordinates():
                self._board[i[0]][i[1]] = self._empty_placeholder

            # Place the original 'contents' of start footprint in the same order into the destination space/footprint.
            for n, i in enumerate(destination_footprint.get_footprint_coordinates()):
                self._board[i[0]][i[1]] = start_contents[n]

        def check_for_win():
            """Checks the Gess board for player winning. (Player's last ring being destroyed.) Updates the game status
            accordingly, potentially ending the game. Returns nothing.
            """

            def from_grid_coordinate(index_format):
                """Takes in python coordinates and returns coordinates in 'i3' format, in order to create new instances
                of the Footprint class.
                """

                # Assigns letter values to the numerical values that represent columns.
                column_dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j",
                               10: "k", 11: "l", 12: "m", 13: "n", 14: "o", 15: "p", 16: "q", 17: "r", 18: "s",
                               19: "t"}

                c = column_dict[index_format[1]]
                r = 20 - index_format[0]
                coordinates_readable = str(c) + str(r)

                return coordinates_readable

            opponent_has_ring = "no"

            # Find all spaces that are empty on the board.
            for row_number, row in enumerate(self._board):
                for column_number, space in enumerate(row):
                    # Get coordinates of empty space, then convert to format needed to make a Footprint. (ex: 'b6')
                    if space == self._empty_placeholder:
                        # Create a Footprint using coordinates of empty space.
                        potential_ring = from_grid_coordinate([row_number, column_number])
                        potential_ring_footprint = Footprint(potential_ring)

                        # Check for a footprint where there are 8 stones owned by the opposing player. (A ring.)
                        stones_in_ring = 0
                        try:
                            for i in potential_ring_footprint.get_footprint_coordinates():
                                if self._board[i[0]][i[1]] == self._waiting_player[0]:
                                    stones_in_ring += 1
                        # Will skip index errors when attempting to iterate over spaces not on the board.
                        except IndexError:
                            continue

                        # If opponent has a ring, game is not over.
                        if stones_in_ring == 8:
                            opponent_has_ring = "yes"

            if opponent_has_ring == "yes":
                return
            else:
                self.set_game_state(f"{self._current_player}_WON")

        def update_game():
            """Checks game state for player winning, in which case game is ended game_over is called,  otherwise,
            changes current player and waiting player in preparation for next turn. Returns nothing.
            """

            if self._game_state != "UNFINISHED":
                self.game_over()
            else:
                current = self._current_player
                waiting = self._waiting_player
                self.set_waiting_player(current)
                self.set_current_player(waiting)

        # Checks if the piece is valid to be moved by the current player.
        if is_valid_piece():
            # Checks that the desired move is valid.
            if is_valid_move():
                # Executes the move once the piece and move are deemed valid.
                execute_move()
                # After move is executed, checks for player winning and thus ending the game, updates game status if so.
                check_for_win()
                # Checks game status, changes current player and waiting player.
                update_game()
                return True
            else:
                return False
        else:
            return False

    def play_game(self):
        """Handles the playing of the Gess game, provides way for players to play the game from the terminal by
        entering keys based on their desired actions.
        """

        # Set empty placeholders to empty characters to improve readability. (Users can change according to preference.)
        self.alter_board_display(' ')

        # Welcome info and starting board displayed.
        print("\n")
        print(colored("Welcome to Gess! Let's get started!\n", self._info_text_color))
        self.get_playable_board()

        while True:
            print(colored(f"It is the {self._current_player} player's turn.\n", self._info_text_color))
            user_input = input(colored("Enter one of the following keys....\n"
                                       "v - View Current Board.\n"
                                       "m - Make Move.\n"
                                       "q - Quit/Resign.\n",
                                       self._instruction_text_color))
            if user_input == 'v':
                self.get_playable_board()
            elif user_input == 'm':
                start_coordinates = input(colored("Please enter the start coordinates in 'c3' format...",
                                                  self._instruction_text_color))
                end_coordinates = input(colored("Please enter the destination coordinates in 'b6' format...",
                                                self._instruction_text_color))
                self.make_move(start_coordinates, end_coordinates)
                self.get_playable_board()
            elif user_input == 'q':
                check = input(colored("Are you sure you would like to forfeit the game? Enter 'y' if so.",
                                      self._warning_text_color))
                if check == 'y':
                    self.resign_game()
                    break
            elif self._game_state != "UNFINISHED":
                break
            else:
                print(colored("Invalid input! Please enter a key for a valid action!", self._warning_text_color))


game = GessGame()
game.play_game()
