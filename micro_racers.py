#!/usr/bin/python
# Micro Racers
# Code Angel

import sys
import os
import pygame
from pygame.locals import *
import math

import track

# Define the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (227, 0, 13)
BLUE = (8, 34, 255)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCOREBOARD_MARGIN = 8
SCOREBOARD_HEIGHT = 36
SCOREBOARD_CAR_WIDTH = 128
TEXT_LINE_HEIGHT = 18
RESULT_BLOCK_WIDTH = 320
RESULT_BLOCK_HEIGHT = 150

TRACK_BLOCK_SIZE = 80
TRACK_HEIGHT = 20

ACCELERATION = 0.2
OFF_TRACK_ACCELERATION = 0.05
MAX_SPEED = 3
DRAG = 0.93
ANGLE_DRAG = 0.92
TURN_SPEED = 0.5

COMPUTER_CAR_ACCELERATION = 0.15
COMPUTER_CAR_TURN_ANGLE = 5
COMPUTER_CAR_MAX_SPEED = 3

CAR_LENGTH = 16
CAR_WIDTH = 8
GRID_WIDTH = 10

RACE_LAPS = 3

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Micro Racers')
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Helvetica', 16)

background_image = track.load_image('general', 'background')
car_image = track.load_image('general', 'red_car')
computer_car_image = track.load_image('general', 'blue_car')

lights_off_image = track.load_image('general', 'lights_off')
lights_red_image = track.load_image('general', 'lights_red')
lights_amber_image = track.load_image('general', 'lights_amber')
lights_green_image = track.load_image('general', 'lights_green')


def main():

    # Initialise variables
    level = 1
    race = 1

    # Track details
    track_pieces = track.load_track_pieces()

    current_track = track.get_track(level, track_pieces)
    start_grid = current_track[0]
    start_grid_x = get_x_coord(start_grid.get('loc'))
    start_grid_y = get_y_coord(start_grid.get('loc'))

    lights_loc = track.get_lights_loc(level)

    # Player and computer car start positions
    car_center_x = start_grid_x + TRACK_BLOCK_SIZE - CAR_LENGTH - GRID_WIDTH
    computer_car_center_x = car_center_x

    car_center_y = start_grid_y - CAR_WIDTH + TRACK_BLOCK_SIZE / 2
    computer_car_center_y = start_grid_y + CAR_WIDTH * 2 + TRACK_BLOCK_SIZE / 2

    # Player car starting data
    speed_x = 0
    speed_y = 0
    angle = 90
    angle_speed = 0
    car_accelerator = False
    car_on_track = True

    laps = 0
    lap_counted = True
    check_point_passed = False

    # Computer car starting data
    computer_car_speed_x = 0
    computer_car_speed_y = 0
    computer_car_angle = 90
    computer_car_new_angle = computer_car_angle
    computer_laps = 0
    computer_lap_counted = True
    computer_car_acceleration = COMPUTER_CAR_ACCELERATION

    race_start = True
    race_over = False
    race_winner = ''
    green_light = False
    start_light_time = pygame.time.get_ticks()

    # Main game loop
    while True:

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            if race_start is False and race_over is False:

                # SPACE key pressed - accelerate car
                if key_pressed[pygame.K_SPACE]:
                    if event.type == pygame.KEYDOWN:
                        car_accelerator = True

                # No SPACE pressed - no acceleration
                else:
                    car_accelerator = False

                # Right key pressed - adjust angle of car
                if key_pressed[pygame.K_RIGHT]:
                    angle_speed -= TURN_SPEED

                # Left key pressed - adjust angle of car
                elif key_pressed[pygame.K_LEFT]:
                    angle_speed += TURN_SPEED

            if key_pressed[pygame.K_RETURN] and race_over is True:

                if race_winner == 'player':
                    computer_car_acceleration += 0.01
                    race += 1
                    if level == 4:
                        level = 1
                else:
                    level = 1
                    race = 1
                    computer_car_acceleration = 0.15

                # New level / game - reset track and car data
                current_track = track.get_track(level, track_pieces)
                start_grid = current_track[0]
                start_grid_x = get_x_coord(start_grid.get('loc'))
                start_grid_y = get_y_coord(start_grid.get('loc'))

                lights_loc = track.get_lights_loc(level)

                # Player and computer car start positions
                car_center_x = start_grid_x + TRACK_BLOCK_SIZE - CAR_LENGTH - GRID_WIDTH
                computer_car_center_x = car_center_x

                car_center_y = start_grid_y - CAR_WIDTH + TRACK_BLOCK_SIZE / 2
                computer_car_center_y = start_grid_y + CAR_WIDTH * 2 + TRACK_BLOCK_SIZE / 2

                speed_x = 0
                speed_y = 0
                angle = 90
                angle_speed = 0
                car_accelerator = False
                car_on_track = True

                laps = 0
                lap_counted = True
                check_point_passed = False

                computer_car_speed_x = 0
                computer_car_speed_y = 0
                computer_car_angle = 90
                computer_car_new_angle = computer_car_angle
                computer_laps = 0
                computer_lap_counted = True

                race_start = True
                race_over = False
                race_winner = ''
                green_light = False
                start_light_time = pygame.time.get_ticks()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Accelerate player car increasing speed_x and speed_y (if space pressed)
        if car_accelerator is True:

            # If player car is on the track, accelerate by ACCELERATION
            if car_on_track is True:
                speed_x += math.sin(math.radians(angle)) * ACCELERATION
                speed_y += math.cos(math.radians(angle)) * ACCELERATION

                # Don't let player car get above the maximum speed
                if speed_x > MAX_SPEED:
                    speed_x = MAX_SPEED

                if speed_y > MAX_SPEED:
                    speed_y = MAX_SPEED

            # If player car is off the track, accelerate by OFF_TRACK_ACCELERATION
            else:
                speed_x += math.sin(math.radians(angle)) * OFF_TRACK_ACCELERATION
                speed_y += math.cos(math.radians(angle)) * OFF_TRACK_ACCELERATION

        # Factor in player car drag resistance
        speed_x *= DRAG
        speed_y *= DRAG

        angle += angle_speed
        angle_speed *= ANGLE_DRAG

        # Accelerate computer car increasing car_speed_x and car_speed_y
        computer_car_speed_x += math.sin(math.radians(computer_car_angle)) * computer_car_acceleration
        computer_car_speed_y += math.cos(math.radians(computer_car_angle)) * computer_car_acceleration

        # Don't let computer car get above the maximum speed
        if computer_car_speed_x > COMPUTER_CAR_MAX_SPEED:
            computer_car_speed_x = COMPUTER_CAR_MAX_SPEED

        if computer_car_speed_y > COMPUTER_CAR_MAX_SPEED:
            computer_car_speed_y = COMPUTER_CAR_MAX_SPEED

        # Factor in computer car drag resistance
        computer_car_speed_x *= DRAG
        computer_car_speed_y *= DRAG

        if computer_car_new_angle < computer_car_angle:
            computer_car_angle -= COMPUTER_CAR_TURN_ANGLE
        elif computer_car_new_angle > computer_car_angle:
            computer_car_angle += COMPUTER_CAR_TURN_ANGLE

        if computer_car_angle == -270:
            computer_car_angle = 90
            computer_car_new_angle = computer_car_angle

        # Prevent the player car from leaving the screen
        if car_center_x < 0:
            car_center_x = 0

        if car_center_x > SCREEN_WIDTH:
            car_center_x = SCREEN_WIDTH

        if car_center_y < SCOREBOARD_HEIGHT:
            car_center_y = SCOREBOARD_HEIGHT

        if car_center_y > SCREEN_HEIGHT:
            car_center_y = SCREEN_HEIGHT

        # Update the player car rectangle centre point by adding x and y speeds
        car_rect = car_image.get_rect()
        car_center_x = car_center_x + speed_x
        car_center_y = car_center_y + speed_y

        car_rect.centerx = car_center_x
        car_rect.centery = car_center_y

        # Update the computer car rectangle centre point by adding x and y speeds
        computer_car_rect = computer_car_image.get_rect()

        if race_start is False and race_over is False:
            computer_car_center_x = computer_car_center_x + computer_car_speed_x
            computer_car_center_y = computer_car_center_y + computer_car_speed_y

        computer_car_rect.centerx = computer_car_center_x
        computer_car_rect.centery = computer_car_center_y

        # Check if the player car is on the track, and if so, if it has crossed the start line
        car_on_track = False
        for track_piece in current_track:
            track_piece_left = get_x_coord(track_piece.get('loc'))
            track_piece_top = get_y_coord(track_piece.get('loc'))
            track_piece_right = track_piece_left + TRACK_BLOCK_SIZE
            track_piece_bottom = track_piece_top + TRACK_BLOCK_SIZE

            # check if the player car is on the track
            if (track_piece_left <= car_center_x <= track_piece_right and
                    track_piece_top <= car_center_y <= track_piece_bottom):

                # the player car is on the track
                car_on_track = True
                car_track = track_piece.get('image')

                # check if the player car is at the start line and has passed the check point
                if (car_track == track_pieces.get('start_grid_image') and
                        check_point_passed is True and
                        car_center_x > track_piece_right - CAR_LENGTH):

                    # player car has passed the start line
                    if lap_counted is False:
                        laps += 1
                        lap_counted = True
                        check_point_passed = False
                        if laps == RACE_LAPS:
                            race_over = True
                            race_winner = 'player'
                            level += 1
                            car_accelerator = False

                elif car_track != track_pieces.get('start_grid_image'):
                    lap_counted = False

                # The check point midway round track ensures player can't take a short cut
                if car_track == track_pieces.get('check_point_image'):
                    check_point_passed = True

            # check if the computer car is on the track
            if (track_piece_left <= computer_car_center_x <= track_piece_right and
                    track_piece_top <= computer_car_center_y <= track_piece_bottom):

                computer_car_track = track_piece.get('image')

                # check if the computer car needs to turn, and if so work out new angle
                if computer_car_track == track_pieces.get('right_down_image') and computer_car_angle == 90:
                    computer_car_new_angle = 0
                elif computer_car_track == track_pieces.get('down_right_image') and computer_car_angle == 0:
                    computer_car_new_angle = 90
                elif computer_car_track == track_pieces.get('down_left_image') and computer_car_angle == 0:
                    computer_car_new_angle = -90
                elif computer_car_track == track_pieces.get('down_right_image') and computer_car_angle == -90:
                    computer_car_new_angle = -180
                elif computer_car_track == track_pieces.get('right_down_image') and computer_car_angle == -180:
                    computer_car_new_angle = -90
                elif computer_car_track == track_pieces.get('up_right_image') and computer_car_angle == -180:
                    computer_car_new_angle = -270
                elif computer_car_track == track_pieces.get('down_left_image') and computer_car_angle == 90:
                    computer_car_new_angle = 180
                elif computer_car_track == track_pieces.get('up_right_image') and computer_car_angle == 180:
                    computer_car_new_angle = 90
                elif computer_car_track == track_pieces.get('up_right_image') and computer_car_angle == -90:
                    computer_car_new_angle = 0

                # check if the computer car is at the start finish line
                if (computer_car_track == track_pieces.get('start_grid_image') and
                        computer_car_center_x > track_piece_right - CAR_LENGTH):
                    if computer_lap_counted is False:
                        computer_laps += 1
                        computer_lap_counted = True
                        if computer_laps == RACE_LAPS:
                            race_over = True
                            race_winner = 'computer'
                            car_accelerator = False
                elif computer_car_track != track_pieces.get('start_grid_image'):
                    computer_lap_counted = False

        # Display background
        game_screen.blit(background_image, [0, 0])

        # Display track pieces
        for track_piece in current_track:
            track_x = get_x_coord(track_piece.get('loc'))
            track_y = get_y_coord(track_piece.get('loc'))
            track_image = track_piece.get('image')
            game_screen.blit(track_image, [track_x, track_y])

        # Display player car
        display_car_image = pygame.transform.rotate(car_image, angle)
        game_screen.blit(display_car_image, car_rect)

        # Display computer car
        computer_display_car_image = pygame.transform.rotate(computer_car_image, computer_car_angle)
        game_screen.blit(computer_display_car_image, computer_car_rect)

        # Dsiplay scoreboard
        display_scoreboard(laps, computer_laps, race)

        # Display end of race messages
        if race_over is True:
            display_end_race_message(race_winner, level)

        # Display start light sequence
        if race_start is True:

            # Start light sequence
            new_time = pygame.time.get_ticks()
            delta_time = new_time - start_light_time

            if delta_time <= 1000:
                game_screen.blit(lights_off_image, lights_loc)

            elif delta_time <= 2000:
                game_screen.blit(lights_red_image, lights_loc)

            elif delta_time <= 3000:
                game_screen.blit(lights_amber_image, lights_loc)

            elif delta_time <= 4000:
                game_screen.blit(lights_green_image, lights_loc)
                race_start = False
                green_light = True

        # Pause on green light before hiding lights
        if green_light is True:
            new_time = pygame.time.get_ticks()
            delta_time = new_time - start_light_time

            if delta_time <= 5000:
                game_screen.blit(lights_green_image, lights_loc)
            else:
                green_light = False

        pygame.display.update()
        clock.tick(60)


# Get the actual x coordinate of the centre point of a track piece
def get_x_coord(coordinates):
    return coordinates[0] * TRACK_BLOCK_SIZE - TRACK_BLOCK_SIZE / 2


# Get the actual y coordinate of the centre point of a track piece
def get_y_coord(coordinates):
    return coordinates[1] * TRACK_BLOCK_SIZE + TRACK_HEIGHT - TRACK_BLOCK_SIZE / 2


# Display the scoreboard at the top of the screen
def display_scoreboard(laps, computer_laps, race_number):

    # Draw the black, red and blue rectangles
    scoreboard_back_rect = (0, 0, SCREEN_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(game_screen, BLACK, scoreboard_back_rect)

    scoreboard_red_car_rect = (0, 0, SCOREBOARD_CAR_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(game_screen, RED, scoreboard_red_car_rect)

    scoreboard_blue_car_rect = (SCREEN_WIDTH - SCOREBOARD_CAR_WIDTH, 0, SCOREBOARD_CAR_WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(game_screen, BLUE, scoreboard_blue_car_rect)

    # Display player laps, computer laps and race number
    laps_text = 'Player Laps: ' + str(laps)
    text = font.render(laps_text, True, WHITE)
    game_screen.blit(text, [SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    computer_laps_text = 'Computer Laps: ' + str(computer_laps)
    text = font.render(computer_laps_text, True, WHITE)
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREEN_WIDTH - text_rect.width - SCOREBOARD_MARGIN, SCOREBOARD_MARGIN])

    race_text = 'RACE: ' + str(race_number)
    text = font.render(race_text, True, WHITE)
    game_screen.blit(text, [centre_text_x(text), SCOREBOARD_MARGIN])


# Display box with end of race message
def display_end_race_message(winner, level):

    # Display rectangle
    message_block_x = (SCREEN_WIDTH - RESULT_BLOCK_WIDTH) / 2
    message_block_y = (SCREEN_HEIGHT - RESULT_BLOCK_HEIGHT) / 2
    race_over_background_rect = (message_block_x, message_block_y, RESULT_BLOCK_WIDTH, RESULT_BLOCK_HEIGHT)
    pygame.draw.rect(game_screen, BLACK, race_over_background_rect)

    # Display 'RESULT' centred
    text = font.render('RESULT', True, WHITE)
    game_screen.blit(text, [centre_text_x(text), message_box_line_y(2)])

    # Display end of race message centred
    if winner == 'player':
        winner_text = 'Player Wins'
        if level == 4:
            return_text = 'Ultimate Champion - Hit RETURN for new game'
        else:
            return_text = 'Level Complete - Hit RETURN for new level'

    else:
        winner_text = 'Computer Wins'
        return_text = 'Hit RETURN for new game'

    text = font.render(winner_text, True, WHITE)
    game_screen.blit(text, [centre_text_x(text), message_box_line_y(3)])

    text = font.render(return_text, True, WHITE)
    game_screen.blit(text, [centre_text_x(text), message_box_line_y(5)])


# Work out x coordinate to centre a block of text
def centre_text_x(text_image):
    text_rect = text_image.get_rect()
    return (SCREEN_WIDTH - text_rect.width) / 2


# Work out y coordinate to display a line of text in the end of game message box, given the line number
def message_box_line_y(line_number):
    return (SCREEN_HEIGHT - RESULT_BLOCK_HEIGHT) / 2 + TEXT_LINE_HEIGHT * line_number


if __name__ == '__main__':
    main()
