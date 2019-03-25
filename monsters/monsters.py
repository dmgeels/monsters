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
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2 ],
[2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2 ],
[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ]]


TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Hero(arcade.Sprite):
    """Sprite class for hero"""

    def __init__(self, board):
        super().__init__()
        self.col = 1
        self.row = 1
        self.is_ghost = False
        self.textures.append(arcade.load_texture('img/character.png', scale=0.4))
        # Load a second, mirrored texture, for when we want to face right.
        self.textures.append(arcade.load_texture('img/character.png', mirrored=True, scale=0.4))
        self.set_texture(TEXTURE_RIGHT)
        self.board = board
        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)

    def ghost(self, is_ghost):
        self.is_ghost = is_ghost

        if is_ghost:
            self.alpha = 0.2
        else:
            self.alpha = 1




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
        if self.board.getCellType(self.row + row_delta, self.col + col_delta) == CellType.EMPTY:
            self.row += row_delta;
            self.col += col_delta;
        else:
            arcade.set_background_color(arcade.color.DARK_RED)

        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)

class Monster(arcade.Sprite):
    """Sprite class for all monsters"""

    def __init__(self, filename, scale, x, y):
        super().__init__(filename, scale=scale, center_x=x, center_y=y)

class Ogre(Monster):
    """Sprite class for Ogre"""

    def __init__(self, x, y):
        super().__init__('img/Ogre.png', 3, x, y)

class GameBoard():
    """Stores board state as a 2-d grid."""

    def __init__(self):
        self.num_cols = WINDOW_COLS
        self.num_rows = WINDOW_ROWS
        self.rows = []
        for row in range(self.num_rows):
            self.rows.append([CellType.EMPTY] * self.num_cols)
            for col in range(self.num_cols):
                if TestBoard[self.num_rows - row -1][col] == 2:
                    self.rows[row][col] = CellType.WALL

    def getCellType(self, row, col):
        return self.rows[row][col]

    def getCoordinates(self, row, col):
        """Returns the center of the cell at col, row."""
        return ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE)

    def draw(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                center_x, center_y = self.getCoordinates(row, col)
                if self.getCellType(row, col) == CellType.WALL:
                    arcade.draw_rectangle_filled(center_x, center_y,
                        CELL_SIZE, CELL_SIZE, arcade.color.GRAY)

class CellType(Enum):
    EMPTY = 1
    WALL = 2

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


    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_text('Monsters', 300, 500, arcade.color.BLACK, 24)
        self.board.draw()
        self.sprites.draw()


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
