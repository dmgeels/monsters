import os
import arcade
import random
from enum import Enum

CELL_SIZE = 32
WINDOW_COLS = 30
WINDOW_ROWS = 20
SCREEN_WIDTH = CELL_SIZE * WINDOW_COLS
SCREEN_HEIGHT = CELL_SIZE * WINDOW_ROWS

Boards = [
[
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'B W     W  H       WWW     D B',
'B W    WWW           WW      B',
'B      W                     B',
'B                            B',
'B WWW      WWW    W     WW   B',
'B   I         WW    WW       B',
'B                            B',
'B       WWW         W      WWB',
'B         WW        WW       B',
'B WWW                        B',
'B  W                       N B',
'B     WW         WW          B',
'B                            B',
'B                            B',
'B         WW         WW    W B',
'B WW         WWW           W B',
'BWW                        W B',
'B        WW        WW        B',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
]



TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Sprite(arcade.Sprite):
    """Base class for all game characters."""

    def __init__(self, board, row, col):
        super().__init__()
        self.col = col
        self.row = row
        self.board = board
        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)
        self.angle = 0
        self.frame_update = 0
        self.texture_index = 0
    def update(self):
        self.frame_update += 1
        if self.frame_update % 6 == 0:
            self.texture_index += 1
            if self.texture_index == len(self.textures):
                self.texture_index = 0
            self.set_texture(self.texture_index)

    def GetMoveDirection(self):
        """Each type of sprite should define this method. Default is silly."""
        return random.choice(list(Direction)) # Random Direction

    def GetMoveResult(self, cell_type):
        """Each type of sprite should define this method. Default is silly."""
        return MoveResult.MOVE

    def MoveOneSpace(self):
        """Moves the sprite one space."""
        direction = self.GetMoveDirection()
        self.last_direction = direction
        next_cell_type = self.board.getCellType(self.row + direction.row_delta,
            self.col + direction.col_delta)
        result = self.GetCollisionAction(next_cell_type)
        print( 'Moving ' + direction + ', next cell type=' + next_cell_type +
            'move result=' + result );
        if result == MoveResult.MOVE:
            self.row += direction.row_delta
            self.col += direction.col_delta
        elif result == MoveResult.DIE:
            pass # TODO: delete the sprite.
        elif result == MoveResult.STOP:
            pass # Wait here.


    def Move(self, direction):
        """Moves the hero one space, unless blocked by a wall."""
        # map direction to row, column changes and sprite texture and angle.
        DELTAS = {
            Direction.UP: (1, 0, TEXTURE_LEFT, 270),
            Direction.DOWN: (-1, 0, TEXTURE_LEFT, 90),
            Direction.LEFT: (0, -1, TEXTURE_LEFT, 0),
            Direction.RIGHT: (0, 1, TEXTURE_RIGHT, 0)
        }
        row_delta, col_delta, texture_index, angle = DELTAS[direction]
        # Change direction first.
        self.last_direction = direction

        #self.set_texture(texture_index)
        #self.angle = angle
        # Now, move one space if there is no wall there.
        cell_type = self.board.getCellType(self.row + row_delta, self.col + col_delta)
        if cell_type == CellType.EMPTY or (self.is_ghost and cell_type != CellType.BARRIER):
            self.row += row_delta
            self.col += col_delta
        elif cell_type == CellType.SOCK:
            self.health += 1
            self.row += row_delta
            self.col += col_delta
            self.board.remove(self.row, self.col)
        elif cell_type == CellType.SHOE:
            self.is_ghost == True
            self.row += row_delta
            self.col += col_delta
            self.board.remove(self.row, self.col)
        else:
            arcade.set_background_color(arcade.color.DARK_RED)

        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)

    def attack(self):
        DELTAS = {
            Direction.UP: (1, 0, TEXTURE_LEFT, 270),
            Direction.DOWN: (-1, 0, TEXTURE_LEFT, 90),
            Direction.LEFT: (0, -1, TEXTURE_LEFT, 0),
            Direction.RIGHT: (0, 1, TEXTURE_RIGHT, 0)
        }
        row_delta, col_delta, texture_index, angle = DELTAS[self.last_direction]
        cell_type = self.board.getCellType(self.row + row_delta, self.col + col_delta)
        if cell_type == CellType.NINJA or CellType.DRAGON:
            print ("Hiya")

class Hero(Sprite):
    """Sprite class for hero"""

    def __init__(self, board):
        super().__init__(board, row=1, col=1)
        self.health = 2
        self.textures.extend(arcade.load_textures('img/Hero.png',
            [
                [0, 0, 32, 32],
                [32, 0, 32, 32],
                [64, 0, 32, 32],
                [0, 32, 32, 32],
                [32, 32, 32, 32],
                [64, 32, 32, 32],
                [0, 64, 32, 32],
            ]
        ))
        self.set_texture(2)
        self.is_ghost = False

    def ghost(self, is_ghost):
        self.is_ghost = is_ghost
        if is_ghost:
            self.alpha = 0.2
        else:
            self.alpha = 1

class Monster(Sprite):
    """Sprite class for all monsters"""

    def __init__(self, board, row, col, filename, scale):
        super().__init__(board, row, col)
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.set_texture(0)


class Item(Sprite):
    """Sprite class for all items"""

    def __init__(self, board, row, col, filename, scale):
        super().__init__(board, row, col)
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.set_texture(0)

class Shoe(Item):
    """Sprite class for Invisibility shoe"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/Haunted shoe.png', 1)

class Sock(Item):
    """Sprite class for Health sock"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/health sock.png', 1)

class Dragon(Monster):
    """Sprite class for Dragon"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/dragon.png', 1)

class Ninja(Monster):
    """Sprite class for Ninja"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/ninja.png', 1)


class GameBoard():
    """Stores board state as a 2-d grid."""

    def __init__(self, board_number):
        self.num_cols = WINDOW_COLS
        self.num_rows = WINDOW_ROWS
        self.rows = []
        for row in range(self.num_rows):
            self.rows.append([CellType.EMPTY] * self.num_cols)
            for col in range(self.num_cols):
                cell_code = Boards[board_number][self.num_rows - row -1][col]
                if cell_code == "W":
                    self.rows[row][col] = CellType.WALL
                elif cell_code == "B":
                    self.rows[row][col] = CellType.BARRIER
                elif cell_code == "D":
                    self.rows[row][col] = CellType.DRAGON
                elif cell_code == "N":
                    self.rows[row][col] = CellType.NINJA
                elif cell_code == "I":
                    self.rows[row][col] = CellType.SHOE
                elif cell_code == "H":
                    self.rows[row][col] = CellType.SOCK
                    print (row, col)

    def remove(self, row, col):

        self.rows[row][col] = CellType.EMPTY
        for i in range(len(self.mon_list)):
            monster = self.mon_list[i]
            if monster.row == row and monster.row == col:
                del self.mon_list[i]
                return

        print (row, col)

    def getCellType(self, row, col):
        return self.rows[row][col]

    def getCoordinates(self, row, col):
        """Returns the center of the cell at col, row."""
        return ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE)

    def draw(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                center_x, center_y = self.getCoordinates(row, col)
                cell_type = self.getCellType(row, col)
                if cell_type == CellType.WALL:
                    arcade.draw_rectangle_filled(center_x, center_y,
                        CELL_SIZE, CELL_SIZE, arcade.color.GRAY)
                elif cell_type == CellType.BARRIER:
                    arcade.draw_rectangle_filled(center_x, center_y,
                        CELL_SIZE, CELL_SIZE, arcade.color.BLACK)

    def set_up(self):
        self.mon_list = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_type = self.getCellType(row, col)
                if cell_type == CellType.DRAGON:
                    self.mon_list.append(Dragon(self, row, col))
                elif cell_type == CellType.NINJA:
                    self.mon_list.append(Ninja(self, row, col))
                elif cell_type == CellType.SOCK:
                    self.mon_list.append(Sock(self, row, col))
                elif cell_type == CellType.SHOE:
                    self.mon_list.append(Shoe(self, row, col))
        return self.mon_list

class CellType(Enum):
    EMPTY = 1
    WALL = 2
    BARRIER = 3
    NINJA = 4
    DRAGON = 5
    SHOE = 6
    SOCK = 7

class Direction(Enum):
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    def __init__(self, row_delta, col_delta):
        self.row_delta = row_delta
        self.col_delta = col_delta

class MoveResult(Enum):
    """What happens when two sprites collide."""
    MOVE = 1
    STOP = 2
    DELETE = 3

class MonsterGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title='monsters')

        self.angle_delta = 1
        self.show_points = False

    def setup(self):
        """ One-time setup """
        self.board = GameBoard(0)

        self.sprites = arcade.SpriteList()
        self.hero = Hero(self.board)
        self.sprites.append(self.hero)
        self.monsters = self.board.set_up()
        for monster in self.monsters:
            self.sprites.append(monster)


    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        self.board.draw()
        self.sprites.draw()
        arcade.draw_text('Monsters', 410, 612, color=arcade.color.RED, font_size=24)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # self.sprite.angle += self.angle_delta
        self.hero.update()

    def on_key_press(self, key, modifiers):
        """ Handles keyboard. Quits on 'q'. """
        KEYS_TO_DIRECTIONS = {
            arcade.key.UP: Direction.UP,
            arcade.key.DOWN: Direction.DOWN,
            arcade.key.LEFT: Direction.LEFT,
            arcade.key.RIGHT: Direction.RIGHT
        }

        if key == arcade.key.Q:
            self.quit()
        elif key == arcade.key.G:
            if self.hero.is_ghost:
                self.hero.ghost(False)
            else:
                self.hero.ghost(True)
        elif key in KEYS_TO_DIRECTIONS:
            self.hero.Move(KEYS_TO_DIRECTIONS[key])

    def on_key_release(self, key, modifiers):
        pass


def main():
    print('Starting up, directory "${0}"'.format(os.getcwd()))
    game = MonsterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
