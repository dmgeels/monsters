import os
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MonsterGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title='monsters')

        arcade.set_background_color(arcade.color.AMAZON)
        self.angle_delta = 1

    def setup(self):
        """ One-time setup """
        self.sprite = arcade.Sprite('img/character.png', scale=0.5, center_x=200, center_y=300)
        self.sprite.angle = 0
        self.sprite.alpha = 50
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(self.sprite)

    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_text('MONSTERS', 140, 200, arcade.color.BLACK, 18)
        self.sprites.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.sprite.angle += self.angle_delta

    def on_key_press(self, key, modifiers):
        """ Handles keyboard. Quits on 'q'. """
        if key == arcade.key.Q:
            self.quit()
        elif key == arcade.key.SPACE:
            self.angle_delta *= -1
        elif key == arcade.key.G:
            self.sprite.alpha = 300 - self.sprite.alpha
            print('Ghost!', self.sprite.alpha)
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
