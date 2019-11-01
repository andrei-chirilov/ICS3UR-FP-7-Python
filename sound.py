#!/usr/bin/env python3

# Created by: Andrei Chirilov
# Created on: Oct 2019
# This program does sounds when pressed on a specific button

import ugame
import stage

import constants


def menu_scene():
    NEW_PALLETE = (b'\xff\xff\x00\x22\xcey\x22\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                    b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')


# an image bank for CircuitPython
image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

# Sets the background
background = stage.Grid(image_bank_1, constants.SCREEN_X, constants.SCREEN_Y)

# a list of sprites that will be updated every frame
sprites = []

# add text objects
text = []
text1 = stage.Text(width=29, height=12, font=None, palette=NEW_PALLETE,
        buffer=None)
text1.move(20, 10)
text1.text("MT Game Studios")
text.append(text1)

text2 = stage.Text(width=29, height=12, font=None, palette=NEW_PALLETE,
        buffer=None)
text2.move(40, 110)
text2.text("PRESS START")
text.append(text2)


# create a stage for the background to show up on
#   and set the frape rate to 60fps
game = stage.Stage(ugame.display, 60)
# set the layers, items show up in order
game.layers = text + sprites + [background]
# render the background and initial location of sprite list
# most likely you will only render background once per scene
game.render_block()

# repeat forever, game loop
while True:
    # get user input
    keys = ugame.buttons.get_pressed()
    # print(keys)

    # Start button is pressed
    if keys & ugame.K_START != 0:
        game_scene()


def game_scene():
    # this function is a scene
    # buttons that keep state information
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X,
                            constants.SCREEN_Y)

    # create a sprite
    # parameters (image_bank, image # in bank, x, y)
    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2 -
                        constants.SPRITE_SIZE / 2),
                        int(constants.SCREEN_Y - constants.SPRITE_SIZE +
                        constants.SPRITE_SIZE / 2))
    sprites.append(ship)  # insert at the top of sprite list

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = sprites + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # (keys)
        if keys & ugame.K_X != 0:  # a button (fire)
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_O:  # b
            pass
        if keys & ugame.K_START:  # start
            pass
        if keys & ugame.K_SELECT:  # select
            pass
        if keys & ugame.K_RIGHT != 0:  # right
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)
            pass
        if keys & ugame.K_LEFT != 0:  # left
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)
            pass
        if keys & ugame.K_UP:  # up
            ship.move(ship.x, ship.y - 1)
            pass
        if keys & ugame.K_DOWN:  # down
            ship.move(ship.x, ship.y + 1)
            pass
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # update game logic

        # redraw sprite list
        game.render_sprites(sprites)
        game.tick()


if __name__ == "__main__":
    game_scene()
