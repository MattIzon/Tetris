import pygame.event
import pygame.key


class Player(object):
    """
    Represents the players interaction with tetris_game.
    """

    def __init__(self):
        """
        Ensure correct pygame key events are logged.
        """
        self.score = 0

        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.key.set_repeat(1, 160)

    def get_input(self):
        """
        Gather player inputs into a list.
        """
        inputs = []

        for event in pygame.event.get():
            if event.key == pygame.K_ESCAPE:
                inputs.append("quit")
            if event.key == pygame.K_SPACE:
                inputs.append("pause")
            if event.key == pygame.K_UP:
                inputs.append("rotate")
            if event.key == pygame.K_LEFT:
                inputs.append("move_l")
            if event.key == pygame.K_RIGHT:
                inputs.append("move_r")
            if event.key == pygame.K_DOWN:
                inputs.append("move_d")
        return inputs

    def update_score(self, lines, level):
        """
        Updates the player score based on the gameboy version scoring system.
        """
        points = {1: 40,
                  2: 100,
                  3: 300,
                  4: 1200}

        self.score += (points[lines] * (level))
