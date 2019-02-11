import os
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MonsterGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, title='monsters')

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        # Set up your game here
        pass

    def quit(self):
        """ Exit the game """
        arcade.close_window()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        sprite = arcade.Sprite('img/character.png', scale=0.2, center_x=200, center_y=300)
        sprites = arcade.SpriteList()
        sprites.append(sprite)
        sprites.draw()


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass

    def on_key_press(self, key, modifiers):
        """ Handles keyboard. Quits on 'q'. """
        if key == arcade.key.Q:
            self.quit()
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
