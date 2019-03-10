import os
import arcade
import random
from enum import Enum

CELL_SIZE = 32
WINDOW_COLS = 30
WINDOW_ROWS = 20
SCREEN_WIDTH = CELL_SIZE * WINDOW_COLS
SCREEN_HEIGHT = CELL_SIZE * WINDOW_ROWS


class Hero(arcade.Sprite):
    """Sprite class for hero"""

    def __init__(self, board):
        super().__init__('img/character.png', scale=0.4)
        self.board = board
        self.col = 0
        self.row = 0
        self.center_x, self.center_y = self.board.getCoordinates(self.col, self.row)


    def Move(self, direction):
        if direction == Direction.UP:
            if self.board.getCellType(self.col, self.row + 1) == CellType.EMPTY:
                self.row += 1

        self.center_x, self.center_y = self.board.getCoordinates(self.col, self.row)
        # TODO: finish

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
        for r in range(self.num_rows):
            self.rows.append( [CellType.EMPTY] * self.num_cols )

    def getCellType(self, col, row):
        return self.rows[row][col]

    def getCoordinates(self, col, row):
        """Returns the center of the cell at col x row."""
        return ((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE)

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

        arcade.set_background_color(arcade.color.AMAZON)
        self.angle_delta = 1
        self.show_points = False

    def setup(self):
        """ One-time setup """
        self.board = GameBoard()
        print( self.board.getCellType(2,2))

        self.sprites = arcade.SpriteList()
        self.hero = Hero(self.board)
        self.sprites.append(self.hero)


    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_text('Monsters', 300, 500, arcade.color.BLACK, 24)
        self.sprites.draw()


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # self.sprite.angle += self.angle_delta
        pass

    def on_key_press(self, key, modifiers):
        """ Handles keyboard. Quits on 'q'. """
        if key == arcade.key.Q:
            self.quit()
        elif key == arcade.key.G:
            self.hero.alpha = 1.2 - self.hero.alpha
            print('Ghost!', self.hero.alpha)
        elif key == arcade.key.UP:
            self.hero.Move(Direction.UP)

    def on_key_release(self, key, modifiers):
        pass


def main():
    print('Starting up, directory "${0}"'.format(os.getcwd()))
    game = MonsterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
