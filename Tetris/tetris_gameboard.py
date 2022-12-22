class Gameboard(object):
    '''
    Holds info on the current board state

    Rows:
        HIDDEN_ROWS
        IN_PLAY = HEIGHT - 1 - HIDDEN_ROWS
        BOTTOM
    '''

    def __init__(self):
        """
        Initialises the board to be a WIDTH x HEIGHT matrix.
        The first HEIGHT - 1 rows contain None values.
        The final row contains "bottom" for each value.
        """
        self.HEIGHT = 23
        self.HIDDEN_ROWS = 2
        self.WIDTH = 10

        self.board = [[None for col in range(self.WIDTH)]
                      for row in range(self.HEIGHT - 1)]
        self.board.append(['bottom'] * self.WIDTH)

    def collision_occured(self, tetro):
        """
        Checks if co-ordinate is already occupied.
        """
        def get_section():
            '''
            Returns values found on board at each block co-ordinate.
            '''
            return [self.board[block[0]][block[1]]
                    for block in tetro.absolute_position()]

        for block in get_section():
            if block is not None:
                return True
        return False

    def update_section(self, tetro):
        '''
        Sets the values of a section of the game board
        with the data held in tetro
        '''
        for block in tetro.absolute_position():
            self.board[block[0]][block[1]] = tetro.image

    def row_complete(self, row):
        """
        Checks row on board for free space to see if its complete.
        """
        for column in range(self.WIDTH):
            if self.board[row][column] is None:
                return False
        return True

    def remove_row(self, row):
        """
        Remove row from the board.
        """
        self.board.pop(row)

    def create_row(self):
        """
        Creates a new row at the top of the board
        """
        self.board.insert(0, [None]*10)

    def resize_board(self):
        """
        Return board to full dimension.
        """
        current_height = len(self.board)
        for missing_row in range(self.HEIGHT - current_height):
            self.create_row()
