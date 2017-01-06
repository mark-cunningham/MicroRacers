# Micro Racers

import pygame, sys
from pygame.locals import *
import math


# Define the colours
MUSTARD = (236, 227, 74)
BLACK = (0, 0, 0)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
SCOREBOARDMARGIN = 4
SCOREBOARDHEIGHT = 28
TEXTLINEHEIGHT = 18

ACCELERATION = 0.2
OFFTRACKACCELERATION = 0.05
MAXSPEED = 3
DRAG = 0.93#0.9
ANGLEDRAG = 0.92#0.95
TURNSPEED = 0.5
TRACKBLOCKSIZE = 80

COMPUTERCARTURNANGLE = 5
COMPUTERCARMAXSPEED = 3


CARLENGTH = 16
CARWIDTH = 8
GRIDWIDTH = 10

RACELAPS = 1


# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Micro Racers")
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

# Load images
background_image = pygame.image.load("background.png").convert()
up_right_image = pygame.image.load("up_right_turn.png").convert()
horiz_straight_image = pygame.image.load("horiz_straight.png").convert()
right_down_image = pygame.image.load("right_down_turn.png").convert()
down_right_image = pygame.image.load("down_right_turn.png").convert()
vert_straight_image = pygame.image.load("vert_straight.png").convert()
down_left_image = pygame.image.load("down_left_turn.png").convert()
start_grid_image = pygame.image.load("start_grid.png").convert()
check_point_image = pygame.image.load("check_point.png").convert()

car_image = pygame.image.load("red_car.png").convert()
computer_car_image = pygame.image.load("blue_car.png").convert()

lights_off_image = pygame.image.load("lights_off.png").convert()
lights_red_image = pygame.image.load("lights_red.png").convert()
lights_amber_image = pygame.image.load("lights_amber.png").convert()
lights_green_image = pygame.image.load("lights_green.png").convert()


# Initialise variables

level = 1

full_track = [[[3, 1], start_grid_image], [[4, 1], horiz_straight_image], [[5, 1], horiz_straight_image],
              [[6, 1], horiz_straight_image], [[7, 1], right_down_image], [[7, 2], vert_straight_image],
              [[7, 3], vert_straight_image], [[7, 4], vert_straight_image], [[7, 5], down_left_image],
              [[6, 5], horiz_straight_image], [[5, 5], horiz_straight_image], [[4, 5], check_point_image],
              [[3, 5], down_right_image], [[3, 4], vert_straight_image], [[3, 3], right_down_image],
              [[2, 3], horiz_straight_image], [[1, 3], down_right_image], [[1,2], vert_straight_image],
              [[1, 1], up_right_image], [[2, 1], horiz_straight_image]]


start_grid_x = full_track[0][0][0] * TRACKBLOCKSIZE
start_grid_y = full_track[0][0][1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

car_center_x = start_grid_x + TRACKBLOCKSIZE/2 - CARLENGTH - GRIDWIDTH
computer_car_center_x = car_center_x

car_center_y = start_grid_y - CARWIDTH
computer_car_center_y = start_grid_y  + CARWIDTH * 2

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
computer_car_angle_speed = 0
computer_car_new_angle = computer_car_angle
computer_laps = 0
computer_lap_counted = True
computer_car_acceleration = 0.15

race_start = True
green_light = False
green_light_time = pygame.time.get_ticks()

lights_loc = [5, 3]
lights_x = lights_loc[0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2
lights_y = lights_loc[1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

race_won = False



while True: # main game loop

    # Keypress events
    for event in pygame.event.get():
        key_pressed = pygame.key.get_pressed()

        if race_start is False and race_won is False:

            # SPACE key pressed - accelerate
            if key_pressed[pygame.K_SPACE]:
                if event.type == pygame.KEYDOWN:
                    car_accelerator = True

            elif key_pressed[pygame.K_RIGHT] and key_pressed[pygame.K_SPACE]:
                car_accelerator = True
            elif key_pressed[pygame.K_LEFT] and key_pressed[pygame.K_SPACE]:
                car_accelerator = True
            else:
                    car_accelerator = False


            if key_pressed[pygame.K_RIGHT]:
                angle_speed = angle_speed - TURNSPEED
            elif key_pressed[pygame.K_LEFT]:
                angle_speed = angle_speed + TURNSPEED

        if key_pressed[pygame.K_RETURN] and race_won is True:

            if level == 2 and laps == RACELAPS:
                full_track = [[[2, 1], start_grid_image], [[3, 1], right_down_image], [[3, 2], down_right_image],
                              [[4, 2], horiz_straight_image], [[5, 2], horiz_straight_image],
                              [[6, 2], horiz_straight_image],
                              [[7, 2], right_down_image], [[7, 3], vert_straight_image], [[7, 4], vert_straight_image],
                              [[7, 5], down_left_image], [[6, 5], horiz_straight_image], [[5, 5], check_point_image],
                              [[4, 5], horiz_straight_image], [[3, 5], horiz_straight_image],
                              [[2, 5], down_right_image],
                              [[2, 4], right_down_image], [[1, 4], down_right_image], [[1, 3], vert_straight_image],
                              [[1, 2], vert_straight_image], [[1, 1], up_right_image]]

                lights_loc = [5, 3]
                lights_x = lights_loc[0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2
                lights_y = lights_loc[1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

                computer_car_acceleration = 0.17

            elif level == 3 and laps == RACELAPS:
                full_track = [[[2, 1], start_grid_image], [[3, 1], right_down_image], [[3, 2], down_right_image],
                              [[4, 2], horiz_straight_image], [[5, 2], down_left_image], [[5, 1], up_right_image],
                              [[6, 1], horiz_straight_image], [[7, 1], right_down_image], [[7, 2], vert_straight_image],
                              [[7, 3], vert_straight_image], [[7, 4], down_left_image], [[6, 4], up_right_image],
                              [[6, 5], down_left_image], [[5, 5], check_point_image], [[4, 5], down_right_image],
                              [[4, 4], right_down_image], [[3, 4], horiz_straight_image],
                              [[2, 4], horiz_straight_image], [[1, 4], down_right_image], [[1, 3], vert_straight_image],
                              [[1, 2], vert_straight_image], [[1, 1], up_right_image]]

                lights_loc = [3, 2]
                lights_x = lights_loc[0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2
                lights_y = lights_loc[1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

                computer_car_acceleration = 0.18

            elif level == 4 or computer_laps == RACELAPS:
                level = 1
                full_track = [[[3, 1], start_grid_image], [[4, 1], horiz_straight_image],
                              [[5, 1], horiz_straight_image],
                              [[6, 1], horiz_straight_image], [[7, 1], right_down_image], [[7, 2], vert_straight_image],
                              [[7, 3], vert_straight_image], [[7, 4], vert_straight_image], [[7, 5], down_left_image],
                              [[6, 5], horiz_straight_image], [[5, 5], horiz_straight_image],
                              [[4, 5], check_point_image],
                              [[3, 5], down_right_image], [[3, 4], vert_straight_image], [[3, 3], right_down_image],
                              [[2, 3], horiz_straight_image], [[1, 3], down_right_image], [[1, 2], vert_straight_image],
                              [[1, 1], up_right_image], [[2, 1], horiz_straight_image]]

                lights_loc = [5, 3]
                lights_x = lights_loc[0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2
                lights_y = lights_loc[1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

                computer_car_acceleration = 0.15

            start_grid_x = full_track[0][0][0] * TRACKBLOCKSIZE
            start_grid_y = full_track[0][0][1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

            car_center_x = start_grid_x + TRACKBLOCKSIZE / 2 - CARLENGTH - GRIDWIDTH
            computer_car_center_x = car_center_x

            car_center_y = start_grid_y - CARWIDTH
            computer_car_center_y = start_grid_y + CARWIDTH * 2

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
            computer_car_angle_speed = 0
            computer_car_new_angle = computer_car_angle
            computer_laps = 0
            computer_lap_counted = True


            race_start = True
            green_light = False
            green_light_time = pygame.time.get_ticks()
            lights_loc = [5, 3]
            lights_x = lights_loc[0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2
            lights_y = lights_loc[1] * TRACKBLOCKSIZE + SCOREBOARDHEIGHT

            race_won = False

    if event.type == QUIT:
        pygame.quit()     
        sys.exit()

    if car_accelerator is True:
        if car_on_track is True:
            speed_x = speed_x + math.sin(math.radians(angle)) * ACCELERATION
            speed_y = speed_y + math.cos(math.radians(angle)) * ACCELERATION

            if speed_x > MAXSPEED:
                speed_x = MAXSPEED

            if speed_y > MAXSPEED:
                speed_y = MAXSPEED
        else:
            speed_x = speed_x + math.sin(math.radians(angle)) * OFFTRACKACCELERATION
            speed_y = speed_y + math.cos(math.radians(angle)) * OFFTRACKACCELERATION

    computer_car_speed_x = computer_car_speed_x + math.sin(math.radians(computer_car_angle)) * computer_car_acceleration
    computer_car_speed_y = computer_car_speed_y + math.cos(math.radians(computer_car_angle)) * computer_car_acceleration

    if computer_car_speed_x > COMPUTERCARMAXSPEED:
        computer_car_speed_x = COMPUTERCARMAXSPEED

    if computer_car_speed_y > COMPUTERCARMAXSPEED:
        computer_car_speed_y = COMPUTERCARMAXSPEED
            
    car_rect = car_image.get_rect()
    computer_car_rect = computer_car_image.get_rect()

    car_center_x = car_center_x + speed_x
    car_center_y = car_center_y + speed_y

    if race_start is False and race_won is False:
        computer_car_center_x = computer_car_center_x + computer_car_speed_x
        computer_car_center_y = computer_car_center_y + computer_car_speed_y





    speed_x = speed_x * DRAG
    speed_y = speed_y * DRAG



    computer_car_speed_x = computer_car_speed_x * DRAG
    computer_car_speed_y = computer_car_speed_y * DRAG

    angle = angle + angle_speed
    angle_speed = angle_speed * ANGLEDRAG


    if computer_car_new_angle < computer_car_angle:
        computer_car_angle = computer_car_angle - COMPUTERCARTURNANGLE
    elif computer_car_new_angle > computer_car_angle:
        computer_car_angle = computer_car_angle + COMPUTERCARTURNANGLE

    if computer_car_angle == -270:
        computer_car_angle = 90
        computer_car_new_angle = computer_car_angle

    if car_center_x < 0:
        car_center_x = 0

    if car_center_x> SCREENWIDTH:
        car_center_x = SCREENWIDTH

    if car_center_y < SCOREBOARDHEIGHT:
        car_center_y = SCOREBOARDHEIGHT

    if car_center_y > SCREENHEIGHT:
        car_center_y = SCREENHEIGHT

    car_rect.centerx = car_center_x    
    car_rect.centery = car_center_y

    computer_car_rect.centerx = computer_car_center_x
    computer_car_rect.centery = computer_car_center_y

    car_on_track = False
    for track_piece in range(len(full_track)):
        track_piece_left = full_track[track_piece][0][0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE/2
        track_piece_top = full_track[track_piece][0][1] * TRACKBLOCKSIZE - TRACKBLOCKSIZE/2 + SCOREBOARDHEIGHT
        track_piece_right = full_track[track_piece][0][0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2 + TRACKBLOCKSIZE
        track_piece_bottom = full_track[track_piece][0][1] * TRACKBLOCKSIZE - TRACKBLOCKSIZE / 2 + TRACKBLOCKSIZE + SCOREBOARDHEIGHT

        if car_center_x >= track_piece_left and car_center_x <= track_piece_right and\
                        car_center_y >= track_piece_top and car_center_y <= track_piece_bottom:
            car_on_track = True

            car_track = full_track[track_piece][1]

            if car_track == start_grid_image and check_point_passed is True and car_center_x > track_piece_right - CARLENGTH:
                if lap_counted is False:
                    laps = laps + 1
                    lap_counted = True
                    check_point_passed = False
                    if laps == RACELAPS:
                        race_won = True
                        level = level + 1
                        car_accelerator = False
            elif car_track != start_grid_image:
                lap_counted = False

            if car_track == check_point_image:
                check_point_passed = True


        if computer_car_center_x >= track_piece_left and computer_car_center_x <= track_piece_right and \
                    computer_car_center_y >= track_piece_top and computer_car_center_y <= track_piece_bottom:
            computer_car_track = full_track[track_piece][1]
            if computer_car_track == right_down_image and computer_car_angle == 90:
                computer_car_new_angle = 0
            elif computer_car_track == down_right_image and computer_car_angle == 0:
                computer_car_new_angle = 90
            elif computer_car_track == down_left_image and computer_car_angle == 0:
                computer_car_new_angle = -90
            elif computer_car_track == down_right_image and computer_car_angle == -90:
                computer_car_new_angle = -180
            elif computer_car_track == right_down_image and computer_car_angle == -180:
                computer_car_new_angle = -90
            elif computer_car_track == up_right_image and computer_car_angle == -180:
                computer_car_new_angle = -270
            elif computer_car_track == down_left_image and computer_car_angle == 90:
                computer_car_new_angle = 180
            elif computer_car_track == up_right_image and computer_car_angle == 180:
                computer_car_new_angle = 90
            elif computer_car_track == up_right_image and computer_car_angle == -90:
                computer_car_new_angle = 0

            if computer_car_track == start_grid_image and computer_car_center_x > track_piece_right - CARLENGTH:
                if computer_lap_counted is False:
                    computer_laps = computer_laps + 1
                    computer_lap_counted = True
                    if computer_laps == RACELAPS:
                        race_won = True
                        car_accelerator = False
            elif computer_car_track != start_grid_image:
                computer_lap_counted = False




    display_car_image = pygame.transform.rotate(car_image, angle)
    computer_display_car_image = pygame.transform.rotate(computer_car_image, computer_car_angle)

    game_screen.blit(background_image, [0, 0])

    for track_piece in range(len(full_track)):
        track_x = full_track[track_piece][0][0] * TRACKBLOCKSIZE - TRACKBLOCKSIZE/2
        track_y = full_track[track_piece][0][1] * TRACKBLOCKSIZE - TRACKBLOCKSIZE/2 + SCOREBOARDHEIGHT
        track_image = full_track[track_piece][1]
        game_screen.blit(track_image, [track_x, track_y])
        
    game_screen.blit(display_car_image, car_rect)
    game_screen.blit(computer_display_car_image, computer_car_rect)

    # Display scores and level
    scoreboard_background_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT)
    pygame.draw.rect(game_screen, MUSTARD, scoreboard_background_rect)

    laps_text = "Player Laps: " + str(laps)
    text = font.render(laps_text, True, (BLACK))
    game_screen.blit(text, [SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    computer_laps_text = "Computer Laps: " + str(computer_laps)
    text = font.render(computer_laps_text, True, (BLACK))
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    level_text = "Level: " + str(level)
    text = font.render(level_text, True, (BLACK))
    text_rect = text.get_rect()
    game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, SCOREBOARDMARGIN])

    # Display end of race message
    if race_won is True:
        if laps == RACELAPS and computer_laps != RACELAPS:
            winner_text = "Player Wins"
            if level == 4:
                return_text = "Ultimate Champion - Hit RETURN for new game"
            else:
                return_text = "Level Complete - Hit RETURN for new level"

        else:
            winner_text = "Computer Wins"
            return_text = "Game Over - Hit RETURN for new game"

        text = font.render(return_text, True, (BLACK))
        text_rect = text.get_rect()

        bk_block_width = text_rect.width + SCOREBOARDMARGIN * 4
        bk_block_height = TEXTLINEHEIGHT * 4 + SCOREBOARDMARGIN * 4

        race_won_background_rect = ((SCREENWIDTH - bk_block_width) / 2, (SCREENHEIGHT - bk_block_height) / 2, bk_block_width, bk_block_height)

        pygame.draw.rect(game_screen, MUSTARD, race_won_background_rect)
        game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, (SCREENHEIGHT - bk_block_height) / 2 + TEXTLINEHEIGHT * 3])

        text = font.render(winner_text, True, (BLACK))
        text_rect = text.get_rect()
        game_screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2, (SCREENHEIGHT - bk_block_height) / 2 + TEXTLINEHEIGHT])


    # Display light sequence
    if race_start is True:
        new_time = pygame.time.get_ticks()
        delta_time = new_time - green_light_time

        if delta_time <= 1000:
            game_screen.blit(lights_off_image, [lights_x, lights_y])
        elif delta_time <= 2000:
            game_screen.blit(lights_red_image, [lights_x, lights_y])

        elif delta_time <= 3000:
            game_screen.blit(lights_amber_image, [lights_x, lights_y])

        elif delta_time <= 4000:
            game_screen.blit(lights_green_image, [lights_x, lights_y])
            race_start = False
            green_light = True

    if green_light is True:
        new_time = pygame.time.get_ticks()
        delta_time = new_time - green_light_time
        if delta_time <= 5000:
            game_screen.blit(lights_green_image, [lights_x, lights_y])
        else:
            green_light = False





    pygame.display.update()
    clock.tick(60)
            

