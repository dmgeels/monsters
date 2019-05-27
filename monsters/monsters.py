import os
import arcade
import random
from enum import Enum
from collections import Counter

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
'BWW                      E W B',
'B        WW        WW        B',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
]



TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Sprite(arcade.Sprite):
    """Base class for all game characters."""
    instance_count_by_class = Counter()

    def __init__(self, board, row, col):
        super().__init__()
        self.col = col
        self.row = row
        self.board = board
        self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)
        self.angle = 0
        self.frame_update = 0
        self.texture_index = 0
        classname = str(self.__class__)
        self.debug_name = f'{classname}-{Sprite.instance_count_by_class[classname]}';

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

    def GetMoveResult(self, cell_type, sprites_in_cell):
        """Each type of sprite should define this method."""
        if cell_type == CellType.WALL or cell_type == CellType.BARRIER:
            return MoveResult.STOP
        else:
            return MoveResult.MOVE

    def GetSpeed(self):
        """Returns speed on a scale from 1-6 steps/second."""
        return 1;

    def MoveOneSpace(self):
        """Moves the sprite one space."""
        direction = self.GetMoveDirection()
        if direction is None:
            # print( f'Sprite {self.debug_name} not moving' )
            return
        self.last_direction = direction
        next_cell_type = self.board.getCellType(self.row + direction.row_delta,
            self.col + direction.col_delta)
        if next_cell_type not in ( CellType.WALL, CellType.BARRIER):
            next_cell_type = CellType.EMPTY
        sprites_in_cell = self.board.getSprites(self.row + direction.row_delta,
            self.col + direction.col_delta)
        result = self.GetMoveResult(next_cell_type, sprites_in_cell)
        # print( f'Moving {self.debug_name}, {direction}, ' +
        #     f'next cell type={next_cell_type} move result={result}' );
        if result == MoveResult.MOVE:
            self.row += direction.row_delta
            self.col += direction.col_delta
            self.center_x, self.center_y = self.board.getCoordinates(self.row, self.col)
        elif result == MoveResult.DELETE:
            self.board.removeSprite( self )
        elif result == MoveResult.STOP:
            pass # Wait here.


class Hero(Sprite):
    """Sprite class for hero"""

    def __init__(self, board):
        super().__init__(board, row=10, col=12)
        self.health = 3
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
        self.board = board
        self.set_texture(2)
        self.is_ghost = False
        self.has_shoe = False
        self.next_direction = None

    def draw_inventory(self):
        shoe = Shoe(self.board, 15, 0)
        if self.has_shoe:
            shoe.draw()
        heart = Heart(self.board, 0, 1)
        for i in range(self.health):
            heart.draw()
            heart.center_x += 20

    def SetMoveDirection(self, direction):
        self.next_direction = direction

    def GetMoveDirection(self):
        """Returns the last direction chosen by the user, if any."""
        direction = self.next_direction
        self.next_direction = None
        return direction

    def GetSpeed(self):
        return 3; # medium speed

    def GetMoveResult(self, cell_type, sprites_in_cell):
        """Each type of sprite should define this method. Default is silly."""
        if (cell_type == CellType.BARRIER or
            (cell_type == CellType.WALL and not self.is_ghost)):
            arcade.set_background_color(arcade.color.DARK_RED)
            return MoveResult.STOP

        for sprite in sprites_in_cell:
            if isinstance(sprite, (Projectile, Monster)):
                self.GetHurt()
            elif isinstance(sprite, Sock):
                self.board.removeSprite( sprite )
                self.health += 1
            elif isinstance(sprite, Shoe):
                self.board.removeSprite( sprite )
                self.ghost( True )
            elif isinstance(sprite, Door):
                self.board.finished = True
        return MoveResult.MOVE

    def GetHurt(self):
        self.health -= 1
        if self.health == 0:
            print( 'I DIE' )

    def shoot(self):
        """Shooting method"""
        arrow = Arrow(self.board, self.row, self.col, self.last_direction)
        return arrow

    def ghost(self, is_ghost):
        self.is_ghost = is_ghost
        if is_ghost:
            self.alpha = 0.2
        else:
            self.alpha = 1

class Monster(Sprite):
    """Sprite class for all monsters"""

    def __init__(self, board, row, col, filename, scale, hero):
        super().__init__(board, row, col)
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.set_texture(0)
        self.hero = hero

    def GetMoveDirection(self):
        """Always move closer to the hero."""
        hero_row_distance = self.hero.row - self.row
        hero_col_distance = self.hero.col - self.col
        if abs(hero_col_distance) > abs(hero_row_distance):
            if hero_col_distance > 0:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if hero_row_distance < 0:
                return Direction.DOWN
            else:
                return Direction.UP

    def GetMoveResult(self, cell_type, sprites_in_cell):
        result = super().GetMoveResult( cell_type, sprites_in_cell )
        if result != MoveResult.STOP:
            for sprite in sprites_in_cell:
                if isinstance(sprite, Projectile):
                    self.board.removeSprite( sprite )
                    return MoveResult.DELETE
                if isinstance(sprite, Hero):
                    sprite.GetHurt()
        return result


class Projectile(Sprite):
    """Sprite class for all Projectiles"""

    def __init__(self, board, row, col, filename, scale, direction):
        self.direction = direction
        super().__init__(board, row, col)
        self.angle = direction.angle
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.set_texture(0)
    def GetMoveDirection(self):
        return self.direction

    def GetSpeed(self):
        return 6;

    def GetMoveResult(self, cell_type, sprites_in_cell):
        result = super().GetMoveResult( cell_type, sprites_in_cell )
        if result == MoveResult.STOP:
            return MoveResult.DELETE
        for sprite in sprites_in_cell:
            if isinstance(sprite, (Projectile, Monster)):
                self.board.removeSprite( sprite )
                return MoveResult.DELETE
            if isinstance(sprite, Hero):
                sprite.GetHurt()
                return MoveResult.DELETE
        return MoveResult.MOVE

class Arrow(Projectile):
    """Sprite class for arrows"""
    def __init__(self, board, row, col, direction):
        super().__init__(board, row, col, "img/arrow.png", 1, direction)

class Fire(Projectile):
    """Sprite class for fire"""
    def __init__(self, board, row, col, direction):
        super().__init__(board, row, col, "img/fire ball.png", 2, direction)

class Item(Sprite):
    """Sprite class for all items"""

    def __init__(self, board, row, col, filename, scale):
        super().__init__(board, row, col)
        self.textures.append(arcade.load_texture(filename, scale=scale))
        self.set_texture(0)
    def GetMoveDirection(self):
        return None

class Shoe(Item):
    """Sprite class for Invisibility shoe"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/Haunted shoe.png', 1)

class Sock(Item):
    """Sprite class for Health sock"""

    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/health sock.png', 1)
class Heart(Item):
    """Sprite class for "Health" """
    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/Heart.png', 1)

class Door(Item):
    """Sprite class for "Door" """
    def __init__(self, board, row, col):
        super().__init__(board, row, col, 'img/door.png', 2)
        self.center_x += 5

class Dragon(Monster):
    """Sprite class for Dragon"""

    def __init__(self, board, row, col, hero):
        super().__init__(board, row, col, 'img/dragon.png', 1, hero)

    def GetSpeed(self):
        return 2; # slower than Hero

class Ninja(Monster):
    """Sprite class for Ninja"""

    def __init__(self, board, row, col, hero):
        super().__init__(board, row, col, 'img/ninja.png', 1.15, hero)

    def GetSpeed(self):
        return 3; # same as Hero


class GameBoard():
    """Stores board state as a 2-d grid."""

    def __init__(self, board_number):
        self.num_cols = WINDOW_COLS
        self.num_rows = WINDOW_ROWS
        self.rows = []
        self.finished = False
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
                elif cell_code == "E":
                    self.rows[row][col] = CellType.DOOR


    def removeAll(self, row, col):
        """Deletes the monster at row,col."""
        for sprite in self.getSprites(row, col):
            self.sprites.remove( sprite )

    def removeSprite(self, sprite):
        self.sprites.remove( sprite )

    def getSprites(self, row, col):
        found = []
        for sprite in self.sprites:
            if sprite.row == row and sprite.col == col:
                found.append( sprite )
        return found

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

    def set_up(self, hero, sprites):
        self.sprites = sprites
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_type = self.getCellType(row, col)
                if cell_type == CellType.DRAGON:
                    self.sprites.append(Dragon(self, row, col, hero))
                elif cell_type == CellType.NINJA:
                    self.sprites.append(Ninja(self, row, col, hero))
                elif cell_type == CellType.SOCK:
                    self.sprites.append(Sock(self, row, col))
                elif cell_type == CellType.SHOE:
                    self.sprites.append(Shoe(self, row, col))
                elif cell_type == CellType.DOOR:
                    self.sprites.append(Door(self, row, col))

class CellType(Enum):
    EMPTY = 1
    WALL = 2
    BARRIER = 3
    NINJA = 4
    DRAGON = 5
    SHOE = 6
    SOCK = 7
    DOOR = 8

class Direction(Enum):
    UP = (1, 0, 90)
    DOWN = (-1, 0, 270)
    LEFT = (0, -1, 180)
    RIGHT = (0, 1, 0)

    def __init__(self, row_delta, col_delta, angle):
        self.row_delta = row_delta
        self.col_delta = col_delta
        self.angle = angle
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
        self.frame_update = 0

    def setup(self):
        """ One-time setup """
        self.board = GameBoard(0)

        self.sprites = arcade.SpriteList()
        self.hero = Hero(self.board)
        self.sprites.append(self.hero)
        self.board.set_up(self.hero, self.sprites)

    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.BUD_GREEN)
        self.board.draw()
        if self.hero.health <= 0:
            arcade.set_background_color(arcade.color.RED)
        elif self.board.finished == True:
            arcade.set_background_color((145, 191, 179))
        self.hero.draw_inventory()
        self.sprites.draw()
        arcade.draw_text('Monsters', 410, 612, color=arcade.color.BUD_GREEN, font_size=24)

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # self.sprite.angle += self.angle_delta
        if self.hero.health <= 0 or self.board.finished == True:
            return
        self.hero.update()
        self.frame_update += 1
        for sprite in self.sprites:
            frames_between_moves = 60 / sprite.GetSpeed()
            if self.frame_update % frames_between_moves == 0:
                sprite.MoveOneSpace()
        if self.frame_update % 6000 == 0:
            self.frame_update = 0 # reset to avoid overflow

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
        # elif key == arcade.key.G:
        #     if self.hero.is_ghost:
        #         self.hero.ghost(False)
        #     else:
        #         self.hero.ghost(True)
        elif key in KEYS_TO_DIRECTIONS:
            self.hero.SetMoveDirection(KEYS_TO_DIRECTIONS[key])
        elif key == arcade.key.SPACE:
            self.sprites.append(self.hero.shoot())


    def on_key_release(self, key, modifiers):
        pass



def main():
    print('Starting up, directory "${0}"'.format(os.getcwd()))
    game = MonsterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
