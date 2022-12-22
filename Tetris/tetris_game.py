import pygame
import random
import tetris_tetrominos as tetro
import tetris_player as player
import tetris_gameboard as gameboard
import tetris_interface as interface

pygame.init()
random.seed()


class Tetris_Game(object):
    """
    Manages all tetris objects and their interactions to produce a playable
    game of Tetris.
    """

    def __init__(self):

        self.tetro_set = self.new_tetro_set()
        self.tetro_current = getattr(tetro, self.tetro_set.pop())()
        self.tetro_next = getattr(tetro, self.tetro_set.pop())()

        self.board = gameboard.Gameboard()

        self.player = player.Player()

        self.interface = interface.Interface()

        self.level = 1
        self.lines = 0

        self.DROP_RATE = 60
        self.drop_counter = 0
        self.clock = pygame.time.Clock()
        self.play = True

    def new_tetro_set(self):
        """
        Create a randomised list with one of every tetromino.
        """
        tetro_set = list(tetro.SHAPES)
        random.shuffle(tetro_set)
        return tetro_set

    def new_tetros(self):
        """
        Move tetro_next into tetro_current and update tetro_next.
        """

        def game_over():
            """
            Determine whether player has quit.
            """
            quit = False
            self.interface.display_game_over()
            while not quit:
                inputs = self.player.get_input()
                for input in inputs:
                    if input == 'quit':
                        self.play = False
                        quit = True

        if not self.tetro_set:
            self.tetro_set = self.new_tetro_set()
        self.tetro_current = self.tetro_next
        self.tetro_next = getattr(tetro, self.tetro_set.pop())()
        if self.board.collision_occured(self.tetro_current):
            game_over()

    def drop_tetro(self):
        """
        Determine if enough clock ticks have passed to drop the tetromino.
        """
        if self.drop_counter == 0:
            self.drop_counter = self.DROP_RATE // self.level
            return True
        else:
            self.drop_counter -= 1
            return False

    def pause_game(self):
        """
        Freeze the game state until unpaused.
        """
        paused = True
        while paused:
            inputs = self.player.get_input()
            for input in inputs:
                if input == 'quit':
                    self.play = False
                    paused = not paused
                if input == 'pause':
                    paused = not paused

    def calculate_move(self, input):
        """
        Update temp_position of tetromino based on input.
        """
        getattr(self.tetro_current, input)()

    def move_valid(self):
        """
        Checks to ensure tetro stays on board and doesn't overlap any
        existing tetros.
        """
        def move_possible():
            """
            Checks move doesn't send tetromino off the gameboard.
            """
            for block_vector in self.tetro_current.absolute_position():
                if block_vector[1] < 0 or block_vector[1] > 9:
                    return False
            return True

        if move_possible():
            if not self.board.collision_occured(self.tetro_current):
                return True
        return False

    def fix_tetro_position(self):
        """
        Fix tetro_current to the board.
        Remove complete lines.
        Update scores.
        """
        self.board.update_section(self.tetro_current)

        # Remove complete lines
        rows_occupied = self.tetro_current.rows_occupied()
        lines_complete = 0
        for row in rows_occupied:
            if self.board.row_complete(row):
                lines_complete += 1
                self.board.remove_row(row)

        # update scores
        if lines_complete > 0:
            self.board.resize_board()
            self.lines += lines_complete
            if self.lines % 10 == 0:
                self.level += 1
            self.player.update_score(lines_complete, self.level)

    def game_start(self):
        """
        Game Loop.
        """
        while self.play:
            moves = self.player.get_input()
            if self.drop_tetro():
                moves.append('move_d')

            # Handle inputs
            for move in moves:
                if move == 'quit':
                    self.play = False
                elif move == 'pause':
                    self.pause_game()
                else:
                    self.calculate_move(move)

                    # Validate move
                    if self.move_valid():
                        self.tetro_current.keep_temp_position_shape()
                    else:
                        self.tetro_current.clear_temp_position_shape()

                        # Update game state
                        if move == "move_d":
                            self.fix_tetro_position()
                            self.new_tetros()
                            break

            self.interface.update_display(self.board,
                                          self.tetro_current,
                                          self.tetro_next,
                                          self.player,
                                          self.lines)
            self.clock.tick(60)


if __name__ == "__main__":
    game = Tetris_Game()
    game.game_start()
    pygame.quit()
