# Micro Racers
# Code Angel
# track module

import pygame
import os


# Load the track images into a dictionary
def load_track_pieces():

    # Load track images
    up_right_image = load_image('track', 'up_right_turn')
    horiz_straight_image = load_image('track', 'horiz_straight')
    right_down_image = load_image('track', 'right_down_turn')
    down_right_image = load_image('track', 'down_right_turn')
    vert_straight_image = load_image('track', 'vert_straight')
    down_left_image = load_image('track', 'down_left_turn')
    start_grid_image = load_image('track', 'start_grid')
    check_point_image = load_image('track', 'check_point')

    # Dictionary of track piece images
    track_pieces = {'up_right_image': up_right_image,
                    'horiz_straight_image': horiz_straight_image,
                    'right_down_image': right_down_image,
                    'down_right_image': down_right_image,
                    'vert_straight_image': vert_straight_image,
                    'down_left_image': down_left_image,
                    'start_grid_image': start_grid_image,
                    'check_point_image': check_point_image}

    return track_pieces


# Get a track for a given level
def get_track(level, track_pieces):

    track = []

    track_1 = [
        {'loc': [3, 1], 'image': track_pieces.get('start_grid_image')},
        {'loc': [4, 1], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [5, 1], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [6, 1], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [7, 1], 'image': track_pieces.get('right_down_image')},
        {'loc': [7, 2], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 3], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 4], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 5], 'image': track_pieces.get('down_left_image')},
        {'loc': [6, 5], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [5, 5], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [4, 5], 'image': track_pieces.get('check_point_image')},
        {'loc': [3, 5], 'image': track_pieces.get('down_right_image')},
        {'loc': [3, 4], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [3, 3], 'image': track_pieces.get('right_down_image')},
        {'loc': [2, 3], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [1, 3], 'image': track_pieces.get('down_right_image')},
        {'loc': [1, 2], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [1, 1], 'image': track_pieces.get('up_right_image')},
        {'loc': [2, 1], 'image': track_pieces.get('horiz_straight_image')}
    ]

    track_2 = [
        {'loc': [2, 1], 'image': track_pieces.get('start_grid_image')},
        {'loc': [3, 1], 'image': track_pieces.get('right_down_image')},
        {'loc': [3, 2], 'image': track_pieces.get('down_right_image')},
        {'loc': [4, 2], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [5, 2], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [6, 2], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [7, 2], 'image': track_pieces.get('right_down_image')},
        {'loc': [7, 3], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 4], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 5], 'image': track_pieces.get('down_left_image')},
        {'loc': [6, 5], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [5, 5], 'image': track_pieces.get('check_point_image')},
        {'loc': [4, 5], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [3, 5], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [2, 5], 'image': track_pieces.get('down_right_image')},
        {'loc': [2, 4], 'image': track_pieces.get('right_down_image')},
        {'loc': [1, 4], 'image': track_pieces.get('down_right_image')},
        {'loc': [1, 3], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [1, 2], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [1, 1], 'image': track_pieces.get('up_right_image')},
    ]

    track_3 = [
        {'loc': [2, 1], 'image': track_pieces.get('start_grid_image')},
        {'loc': [3, 1], 'image': track_pieces.get('right_down_image')},
        {'loc': [3, 2], 'image': track_pieces.get('down_right_image')},
        {'loc': [4, 2], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [5, 2], 'image': track_pieces.get('down_left_image')},
        {'loc': [5, 1], 'image': track_pieces.get('up_right_image')},
        {'loc': [6, 1], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [7, 1], 'image': track_pieces.get('right_down_image')},
        {'loc': [7, 2], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 3], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [7, 4], 'image': track_pieces.get('down_left_image')},
        {'loc': [6, 4], 'image': track_pieces.get('up_right_image')},
        {'loc': [6, 5], 'image': track_pieces.get('down_left_image')},
        {'loc': [5, 5], 'image': track_pieces.get('check_point_image')},
        {'loc': [4, 5], 'image': track_pieces.get('down_right_image')},
        {'loc': [4, 4], 'image': track_pieces.get('right_down_image')},
        {'loc': [3, 4], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [2, 4], 'image': track_pieces.get('horiz_straight_image')},
        {'loc': [1, 4], 'image': track_pieces.get('down_right_image')},
        {'loc': [1, 3], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [1, 2], 'image': track_pieces.get('vert_straight_image')},
        {'loc': [1, 1], 'image': track_pieces.get('up_right_image')},
    ]

    if level == 1:
        track = track_1
    elif level == 2:
        track = track_2
    elif level == 3:
        track = track_3

    return track


# Get traffic light location
def get_lights_loc(level):

    lights_loc_list = [[380, 240], [360, 280], [392, 280]]

    return lights_loc_list[level - 1]


# Get an image from folder
def load_image(folder_name, filename):
    full_path = os.path.dirname(os.path.realpath(__file__))
    images_path = os.path.join(full_path, 'images')
    folder_path = os.path.join(images_path, folder_name)
    full_filename = os.path.join(folder_path, filename + '.png')

    image = pygame.image.load(full_filename).convert_alpha()

    return image
