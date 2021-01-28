import math
import os
import random

import numpy
from PIL import Image, ImageEnhance


def adjust_image_brightness(image, factor):
    # image brightness enhancer
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def get_tiles_from(tiles_directory):
    # convert_tile_extension_to_jpg(tiles_directory)

    files = os.listdir(tiles_directory)
    tiles = []

    for file in files:
        file_path = os.path.abspath(os.path.join(tiles_directory, file))
        tile_path = open(file_path, "rb")
        tile = Image.open(tile_path).convert('RGB')

        tiles.append(tile)
        tile.load()
        tile_path.close()

    return tiles


def get_average_rgb(image):
    numpy_image = numpy.array(image)
    h, w, d = numpy_image.shape
    reshaped_array = numpy_image.reshape(w * h, d)
    return tuple(reshaped_array.mean(axis=0))


# Split target image by base on gird size
def split_image(image, size):
    target_image_width, target_image_height = image.size[0], image.size[1]
    grid_height, grid_width = size

    split_image_width, split_image_height = int(target_image_width / grid_width), int(target_image_height / grid_height)

    split_images = []

    for i in range(grid_width):
        for j in range(grid_height):
            split_images.append(image.crop((j * split_image_width, i * split_image_height, (j + 1) * split_image_width,
                                            (i + 1) * split_image_height)))

    return split_images


def get_best_match_index(checked_average_rgb, total_average_rgb):
    checked_rgb = checked_average_rgb
    index = 0
    min_index = 0
    min_dist = float("inf")  # infinite value

    for average_rgb in total_average_rgb:
        dist = ((average_rgb[0] - checked_rgb[0]) ** 2 +
                (average_rgb[1] - checked_rgb[1]) ** 2 +
                (average_rgb[2] - checked_rgb[2]) ** 2)

        if dist < min_dist:  # First value of 'min_dist' is infinite => initial value of 'dist' will always be approved
            min_dist = dist
            min_index = index

        index += 1

    return min_index


def create_image_grid(matched_tiles, grid_size):
    grid_height, grid_width = grid_size

    matched_tile_max_width = max(
        [img.size[0] for img in matched_tiles])  # Get the largest tile width among matched tiles
    matched_tile_max_height = max(
        [img.size[1] for img in matched_tiles])  # Get the largest tile height among matched tiles

    # Create a blank photo has the size base on grid_size and matched_tile size
    generated_mosaic_photo = Image.new('RGB',
                                       (grid_width * matched_tile_max_width, grid_height * matched_tile_max_height))
    tile_index = 0

    for row in range(grid_height):
        for col in range(grid_width):
            generated_mosaic_photo.paste(matched_tiles[tile_index],
                                         (col * matched_tile_max_width, row * matched_tile_max_height))
            tile_index += 1

    return generated_mosaic_photo


def create_mosaic_photo(target_image, tiles_path, grid_size,
                        duplicated_tile=True, resize_allowed=True):
    split_target_images = split_image(target_image, grid_size)

    matched_tiles = []
    count = 0
    batch_size = int(len(split_target_images) / 10)

    all_tile_average_rgb = []

    print('Start importing tiles from', tiles_path)

    tiles = get_tiles_from(tiles_path)

    # Check for empty tile directory
    if not tiles:
        print('No image found in %s. Exiting.' % (tiles_path,))
        exit()

    random.shuffle(tiles)

    # If don't allow to duplicate tile, ensure: grid_height x grid_width <= tile quantity
    if not duplicated_tile:
        if grid_size[0] * grid_size[1] > len(tiles):
            print(
                f"""Can\' create mosaic photo without using duplicated tile
                        (Grid size less than number of total tile images)
                        Exiting.""")
            exit()

    print(f"""Finish importing tiles. There is a total of {len(tiles)} tiles.""")

    print('Start creating mosaic photo...')

    # Resize tile if allowed
    if resize_allowed:
        resize_all_tiles(tiles, target_image, grid_size)

    # Get average color of all tiles
    for tile in tiles:
        try:
            all_tile_average_rgb.append(get_average_rgb(tile))
        except ValueError:
            continue

    for current_image in split_target_images:
        average_rgb = get_average_rgb(current_image)
        match_index = get_best_match_index(average_rgb, all_tile_average_rgb)

        matched_tiles.append(tiles[match_index])

        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print(f"""Processed {count} of {len(split_target_images)}""")

        count += 1

        # Remove selected image from input if flag set
        if not duplicated_tile:
            tiles.remove(match_index)

    mosaic_image = create_image_grid(matched_tiles, grid_size)

    return mosaic_image


def resize_all_tiles(tiles, target_image, grid_size):
    print('Resizing tiles...')

    # For given grid size, compute max dims w,h of tiles
    new_size = (int(target_image.size[0] / grid_size[1]),
                int(target_image.size[1] / grid_size[0]))

    # resize
    for tile in tiles:
        tile.thumbnail(new_size)


def generate_mosaic_photo(target_image, tiles_path, grid_size, scale=3, duplicated_tile=True, color_mode='RGB',
                          output_filename='Result.jpg'):
    original_image = Image.open(target_image)

    width, height = original_image.size

    scaled_image = original_image.resize((math.floor(width * scale), math.floor(height * scale)))

    mosaic_image = create_mosaic_photo(scaled_image, tiles_path, grid_size, duplicated_tile).convert(color_mode)

    # Write image out
    mosaic_image.save(output_filename, 'jpeg')

    print("Saving output to %s" % (output_filename,))
    print('Finished.')


# ======================================================================================================================

if __name__ == '__main__':
    generate_mosaic_photo(target_image='../data/Face.jpg',
                          tiles_path='../data/Face/',
                          output_filename='Result.jpg',
                          scale=5,
                          grid_size=(150, 150),
                          duplicated_tile=True,
                          color_mode='RGB')
