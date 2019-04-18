import os
import arcade
import random
from enum import Enum

CELL_SIZE = 32
WINDOW_COLS = 30
WINDOW_ROWS = 20
SCREEN_WIDTH = CELL_SIZE * WINDOW_COLS
SCREEN_HEIGHT = CELL_SIZE * WINDOW_ROWS

TestBoard = [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'B W     W          WWW     D B',
'B W    WWW           WW      B',
'B      W                     B',
'B                            B',
'B WWW      WWW    W     WW   B',
'B             WW    WW       B',
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

    def Move(self, direction):
        """Moves the hero one space, unless blocked by a wall."""
        # map direction to row, column changes and sprite texture and angle.
        DELTAS = {
            Direction.UP: (1, 0, TEXTURE_LEFT, 270),
            Direction.DOWN: (-1, 0, TEXTURE_LEFT, 90),
            Direction.LEFT: (0, -1, TEXTURE_LEFT, 0),
            Direction.RIGHT: (0, 1, TEXTURE_RIGHT, 0)
        }
        row_delta, col_delta, texture_index, angle = DELTAS[direction];
        # Change direction first.
        self.set_texture(texture_index)
        self.angle = angle;
        # Now, move one space if there is no wall there.
        cell_type = self.board.getCellType(self.row + row_delta, self.col + col_delta)
        if cell_type == CellType.EMPTY or (self.is_ghost and cell_type != CellType.BARRIER):
            self.row += row_delta;
            self.col += col_delta;
        else:
            arcade.set_background_color(arcade.color.DARK_RED)

        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)


class Hero(Sprite):
    """Sprite class for hero"""

    def __init__(self, board):
        super().__init__(board, row=1, col=1)
        self.is_ghost = False
        self.textures.append(arcade.load_texture('img/character.png', mirrored=True, scale=1))
        # Load a second, mirrored texture, for when we want to face right.
        self.textures.append(arcade.load_texture('img/character.png', scale=1))
        self.set_texture(TEXTURE_RIGHT)

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

    def __init__(self):
        self.num_cols = WINDOW_COLS
        self.num_rows = WINDOW_ROWS
        self.rows = []
        for row in range(self.num_rows):
            self.rows.append([CellType.EMPTY] * self.num_cols)
            for col in range(self.num_cols):
                if TestBoard[self.num_rows - row -1][col] == "W":
                    self.rows[row][col] = CellType.WALL
                elif TestBoard[self.num_rows - row -1][col] == "B":
                    self.rows[row][col] = CellType.BARRIER
                elif TestBoard[self.num_rows - row -1][col] == "D":
                    self.rows[row][col] = CellType.DRAGON
                elif TestBoard[self.num_rows - row -1][col] == "N":
                    self.rows[row][col] = CellType.NINJA

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

    def set_up_monters(self):
        mon_list = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_type = self.getCellType(row, col)
                if cell_type == CellType.DRAGON:
                    mon_list.append(Dragon(self, row, col))
                elif cell_type == CellType.NINJA:
                    mon_list.append(Ninja(self, row, col))
        return mon_list

class CellType(Enum):
    EMPTY = 1
    WALL = 2
    BARRIER = 3
    NINJA = 4
    DRAGON = 5


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class MonsterGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title='monsters')

        self.angle_delta = 1
        self.show_points = False

    def setup(self):
        """ One-time setup """
        self.board = GameBoard()

        self.sprites = arcade.SpriteList()
        self.hero = Hero(self.board)
        self.sprites.append(self.hero)
        self.monsters = self.board.set_up_monters()
        for monster in self.monsters:
            self.sprites.append(monster)


    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        self.board.draw()
        self.sprites.draw()
        arcade.draw_text('Monsters', 410, 612, color=arcade.color.RED, font_size=24)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # self.sprite.angle += self.angle_delta
        pass

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
