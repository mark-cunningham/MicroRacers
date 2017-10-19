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


