import os
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Hero(arcade.Sprite):
    """Sprite class for hero"""

    def __init__(self, x, y):
        super().__init__('img/character.png', scale=0.5, center_x=x, center_y=y)

class Monster(arcade.Sprite):
    """Sprite class for all monsters"""

    def __init__(self, filename, scale, x, y):
        super().__init__(filename, scale=scale, center_x=x, center_y=y)


class Ogre(Monster):
    """Sprite class for Ogre"""

    def __init__(self, x, y):
        super().__init__('img/Ogre.png', 3, x, y)

class Duck(Monster):
    """Sprite class for Duck"""

    def __init__(self, x, y):
        super().__init__('img/Duck.png', 2, x=x, y=y)


class MonsterGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title='monsters')

        arcade.set_background_color(arcade.color.AMAZON)
        self.angle_delta = 1
        self.show_points = False

    def setup(self):
        """ One-time setup """

        self.sprites = arcade.SpriteList()



        self.sprites.append(Hero(300, 350))
        for j in range(4):
            for o in range(12):
                x = 100 + 50 * o
                y = 300 - 50 * j

                if random.randint(1, 5) == 5:
                    fred=Duck(x, y)
                else:
                    fred=Ogre(x, y)
                """Make Ogre or duck in the cords"""
                self.sprites.append(fred)
        # self.sprite = arcade.Sprite('img/character.png', scale=0.5, center_x=200, center_y=300)
        # self.sprite.angle = 0
        # self.sprite.alpha = 1.0
        # self.sprites = arcade.SpriteList(use_spatial_hash=False)
        # self.sprites.append(self.sprite)




    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_text('Dowsha', 300, 500, arcade.color.BLACK, 18)
        if self.show_points:
            for x, y in self.sprite.get_points():
                arcade.draw_point( x, y, arcade.color.BLACK, 2 )
        self.sprites.draw()

        arcade.button()


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        # self.sprite.angle += self.angle_delta
        pass

    def on_key_press(self, key, modifiers):
        """ Handles keyboard. Quits on 'q'. """
        if key == arcade.key.Q:
            self.quit()
        # elif key == arcade.key.SPACE:
        #     self.angle_delta *= -1
        # elif key == arcade.key.G:
        #     self.sprite.alpha = 1.2 - self.sprite.alpha
        #     print('Ghost!', self.sprite.alpha)
        # elif key == arcade.key.S:
        #     self.show_points = not self.show_points
        arcade.set_background_color(arcade.color.BLUE_GRAY)

    def on_key_release(self, key, modifiers):
        arcade.set_background_color(arcade.color.AMAZON)


def main():
    print('Starting up, directory "${0}"'.format(os.getcwd()))
    game = MonsterGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
