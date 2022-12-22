import pygame
pygame.init()


class Interface(object):
    """
    """

    def __init__(self):
        """
        Set-up the display and the images & fonts required.
        """
        self.screen = pygame.display.set_mode((616, 616))

        self.BLOCK_SIZE = 28
        self.green = pygame.image.load("images/green.png").convert()
        self.pink = pygame.image.load("images/pink.png").convert()
        self.orange = pygame.image.load("images/orange.png").convert()
        self.yellow = pygame.image.load("images/yellow.png").convert()
        self.blue = pygame.image.load("images/blue.png").convert()
        self.darkblue = pygame.image.load("images/darkblue.png").convert()
        self.red = pygame.image.load("images/red.png").convert()
        self.blank = pygame.image.load("images/blank.png").convert()
        self.IMAGES = {'green': self.green,
                       'pink': self.pink,
                       'orange': self.orange,
                       'yellow': self.yellow,
                       'blue': self.blue,
                       'darkblue': self.darkblue,
                       'red': self.red,
                       'blank': self.blank}

        self.font_large = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 25)

        self.setup_ui()

    def setup_ui(self):
        """
        Display the non-changing parts of the user interface.
        """
        labels = []

        def next_label():
            """
            Display label for next tetromino.
            """
            position = [12 * self.BLOCK_SIZE, 1 * self.BLOCK_SIZE]
            label = self.font_large.render("NEXT:", True, (240, 240, 240))
            return {'label': label, 'position': position}

        def score_label():
            """
            Display label for player score.
            """
            position = [12 * self.BLOCK_SIZE, 7 * self.BLOCK_SIZE]
            label = self.font_large.render("SCORE:", True, (240, 240, 240))
            return {'label': label, 'position': position}

        def lines_label():
            """
            Display the number of completed lines achieved.
            """
            position = [12 * self.BLOCK_SIZE, 12 * self.BLOCK_SIZE]
            label = self.font_large.render("LINES:", True, (240, 240, 240))
            return {'label': label, 'position': position}

        def control_labels():
            """
            Display the controls.
            """
            labels = []
            position = [12 * self.BLOCK_SIZE, 18 * self.BLOCK_SIZE]
            controls = ["ROTATE: UP     DOWN: DOWN",
                        "LEFT: LEFT     RIGHT: RIGHT",
                        "PAUSE: SPACE     QUIT: ESC"]

            for control in controls:
                label = self.font_small.render(control, True, (240, 240, 240))
                labels.append({'label': label, 'position': list(position)})
                position[1] += self.BLOCK_SIZE
            return labels

        labels.append(next_label())
        labels.append(score_label())
        labels.append(lines_label())
        labels.extend(control_labels())

        for label in labels:
            self.screen.blit(label['label'],
                             (label['position'][0], label['position'][1]))

    def update_display(self, gameboard,
                       tetro_current, tetro_next, player, lines):
        """
        Display the changing parts of the user interface.
        """

        def clear_display(area):
            """
            Turns an area of the screen black
            """
            self.screen.fill((0, 0, 0), area)

        def display_board(gameboard, tetro):
            """
            Refresh display of the gameboard.
            """
            position = (1 * self.BLOCK_SIZE, 1 * self.BLOCK_SIZE)
            dimensions = (gameboard.WIDTH * self.BLOCK_SIZE,
                          gameboard.HEIGHT * self.BLOCK_SIZE)
            board_area = pygame.Rect(position[0], position[1],
                                     dimensions[0], dimensions[1])

            def display_tetro_current():
                """
                Display the in-play tetromino.
                """
                offset_hori = position[0]
                offset_vert = position[1]
                for block in tetro.absolute_position():
                    block[0] -= gameboard.HIDDEN_ROWS
                    if not block[0] < 0:
                        self.screen.blit(self.IMAGES[tetro.image],
                                         (block[1] * self.BLOCK_SIZE
                                          + offset_hori,
                                          block[0] * self.BLOCK_SIZE
                                          + offset_vert))

            clear_display(board_area)

            offset_vert = position[1]
            for row in gameboard.board[gameboard.HIDDEN_ROWS:gameboard.HEIGHT]:
                offset_hori = position[0]
                for image in row:
                    if image is None:
                        image = 'blank'
                    if image != 'bottom':
                        self.screen.blit(self.IMAGES[image],
                                         (offset_hori, offset_vert))
                    offset_hori += self.BLOCK_SIZE
                offset_vert += self.BLOCK_SIZE

            display_tetro_current()

        def display_tetro_next(tetro):
            """
            Display the next tetromino.
            """
            position = (15 * self.BLOCK_SIZE, 4 * self.BLOCK_SIZE)
            dimensions = (4 * self.BLOCK_SIZE, 2 * self.BLOCK_SIZE)
            tetro_area = pygame.Rect(position[0], position[1],
                                     dimensions[0], dimensions[1])

            clear_display(tetro_area)
            offset_hori = position[0]
            offset_vert = position[1]
            for block in tetro.shape:
                self.screen.blit(self.IMAGES[tetro.image],
                                 (offset_hori + block[1]*self.BLOCK_SIZE,
                                  offset_vert + block[0]*self.BLOCK_SIZE))

        def display_scores(player, lines):
            """
            Display current player scores.
            """
            def display_value(position, value):
                """
                Display value passed at position passed.
                """
                dimensions = (6 * self.BLOCK_SIZE, 2 * self.BLOCK_SIZE)
                area = pygame.Rect(position[0], position[1],
                                   dimensions[0], dimensions[1])

                clear_display(area)
                display = self.font_large.render(str(value),
                                                 True, (240, 240, 240))
                self.screen.blit(display, (position[0], position[1]))

            score_position = [16 * self.BLOCK_SIZE, 9 * self.BLOCK_SIZE]
            lines_position = [16 * self.BLOCK_SIZE, 14 * self.BLOCK_SIZE]

            display_value(score_position, player.score)
            display_value(lines_position, lines)

        display_board(gameboard, tetro_current)
        display_tetro_next(tetro_next)
        display_scores(player, lines)
        pygame.display.update()

    def display_game_over(self):
        """
        Informs the player the current game has ended.
        """
        position = [2 * self.BLOCK_SIZE, 10 * self.BLOCK_SIZE]
        label = self.font_large.render("GAME  OVER", True, (240, 240, 240))
        self.screen.blit(label, (position[0], position[1]))
        pygame.display.update()
