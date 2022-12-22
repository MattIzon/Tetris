SHAPES = ["Tetro_Line",
          "Tetro_T",
          "Tetro_J",
          "Tetro_L",
          "Tetro_S",
          "Tetro_Z",
          "Tetro_O"]


class _Tetromino(object):
    '''
    The base class for a Tetromino object
    This is a base class and should never be instantiated.
    '''

    def __init__(self):
        '''
        Initialise starting position.
        '''
        self.position = [0, 3]
        self.temp_position = list(self.position)

    def absolute_position(self, temp=True):
        """
        Calculate the squares occupied by temp_shape and temp_position by
        default.
        If temp is False use shape and position.
        """
        if temp:
            position = self.temp_position
            shape = self.temp_shape
        else:
            position = self.position
            shape = self.shape
        abs_pos = [[block_vector[index] + position[index]
                    for index in [0, 1]]
                   for block_vector in shape]
        return abs_pos

    def rows_occupied(self):
        """
        Get non-repeating X co-ordinates of absolute_position in
        descending order.
        """
        rows = {block[0] for block in self.absolute_position()}
        rows = list(rows)
        rows.sort(reverse=True)
        return rows

    def rotate(self, rotation_matrix=[(0, 1), (-1, 0)]):
        """
        Calculate temp_shape by rotating shape clockwise around pivot_vector.
        """
        def dot_product(rotation_matrix, relative_vector):
            """
            Calculates the matrix product between rotation_matrix and
            relative_vector.
            """
            return tuple([sum(row[index]*relative_vector[index]
                              for index in [0, 1]) for row in rotation_matrix])

        new_shape = []
        for block_vector in self.shape:

            # Vector relative to pivot_vector origin
            relative_vector = (block_vector[0] - self.pivot_vector[0],
                               block_vector[1] - self.pivot_vector[1])

            # rotate 90 degrees
            transition_vector = dot_product(rotation_matrix, relative_vector)

            # Vector back to (0,0) origin
            new_block_vector = (
                transition_vector[0] + self.pivot_vector[0],
                transition_vector[1] + self.pivot_vector[1])
            new_shape.append(new_block_vector)
        self.temp_shape = new_shape

    def move_l(self):
        """
        Calculate temp_position when moving left one square.
        """
        self.temp_position[1] -= 1

    def move_r(self):
        """
        Calculate temp_position when moving right one square.
        """
        self.temp_position[1] += 1

    def move_d(self):
        """
        Calculate temp_position when moving down one square.
        """
        self.temp_position[0] += 1

    def keep_temp_position_shape(self):
        """
        Make temp_position the new position.
        """
        self.position = list(self.temp_position)
        self.shape = list(self.temp_shape)

    def clear_temp_position_shape(self):
        """
        Forget temp_position, make equal to position.
        """
        self.temp_position = list(self.position)
        self.temp_shape = list(self.shape)


class Tetro_Line(_Tetromino):
    '''
    Line shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_Line, self).__init__()
        self.shape = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (0, 1)
        self.image = 'blue'

    def rotate(self):
        super(Tetro_Line, self).rotate()


class Tetro_T(_Tetromino):
    '''
    T shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_T, self).__init__()
        self.shape = [(0, 1), (1, 0), (1, 1), (1, 2)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (1, 1)
        self.image = 'pink'

    def rotate(self):
        super(Tetro_T, self).rotate()


class Tetro_J(_Tetromino):
    '''
    J shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_J, self).__init__()
        self.shape = [(0, 0), (1, 0), (1, 1), (1, 2)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (1, 1)
        self.image = 'orange'

    def rotate(self):
        super(Tetro_J, self).rotate()


class Tetro_L(_Tetromino):
    '''
    L shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_L, self).__init__()
        self.shape = [(0, 2), (1, 0), (1, 1), (1, 2)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (1, 1)
        self.image = 'red'

    def rotate(self):
        super(Tetro_L, self).rotate()


class Tetro_S(_Tetromino):
    '''
    S shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_S, self).__init__()
        self.shape = [(0, 1), (0, 2), (1, 0), (1, 1)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (1, 1)
        self.image = 'green'

    def rotate(self):
        super(Tetro_S, self).rotate()


class Tetro_Z(_Tetromino):
    '''
    Z shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_Z, self).__init__()
        self.shape = [(0, 0), (0, 1), (1, 1), (1, 2)]
        self.temp_shape = list(self.shape)
        self.pivot_vector = (1, 1)
        self.image = 'darkblue'

    def rotate(self):
        super(Tetro_Z, self).rotate()


class Tetro_O(_Tetromino):
    '''
    O shaped Tetromino object.
    '''

    def __init__(self):
        super(Tetro_O, self).__init__()
        self.shape = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.temp_shape = list(self.shape)
        self.image = 'yellow'

    def rotate(self):
        """
        Overwrite superclass method to effectively do nothing.
        """
        return self.shape
