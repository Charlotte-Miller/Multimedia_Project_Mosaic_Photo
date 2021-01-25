import math
import os
import random

import numpy
from PIL import Image


def get_tiles_from(tiles_directory, color_mode='RGB'):
    # convert_tile_extension_to_jpg(tiles_directory)

    files = os.listdir(tiles_directory)
    tiles = []

    for file in files:
        file_path = os.path.abspath(os.path.join(tiles_directory, file))
        tile_path = open(file_path, "rb")
        tile = Image.open(tile_path).convert(color_mode)

        tiles.append(tile)
        tile.load()
        tile_path.close()

    print('Checking tile directory...')

    # check if any valid input images found
    if not tiles:
        print('No image found in %s. Exiting.' % (tiles_directory,))
        exit()

    return tiles


def get_average_rgb(image):
    im = numpy.array(image)
    w, h, d = im.shape
    return tuple(numpy.average(im.reshape(w * h, d), axis=0))


def split_image(image, size):
    W, H = image.size[0], image.size[1]
    m, n = size
    w, h = int(W / n), int(H / m)
    imgs = []
    for j in range(m):
        for i in range(n):
            imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
    return (imgs)


def get_best_match_index(input_avg, avgs):
    avg = input_avg
    index = 0
    min_index = 0
    min_dist = float("inf")
    for val in avgs:
        dist = ((val[0] - avg[0]) * (val[0] - avg[0]) +
                (val[1] - avg[1]) * (val[1] - avg[1]) +
                (val[2] - avg[2]) * (val[2] - avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1
    return min_index


def create_image_grid(images, dims):
    m, n = dims
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])
    grid_img = Image.new('RGB', (n * width, m * height))
    for index in range(len(images)):
        row = int(index / n)
        col = index - n * row
        grid_img.paste(images[index], (col * width, row * height))
    return (grid_img)


def create_mosaic_photo(target_image, tiles_path, grid_size,
                        duplicated_tile=True, color_mode='RGB'):
    target_images = split_image(target_image, grid_size)

    output_images = []
    count = 0
    batch_size = int(len(target_images) / 10)

    avgs = []

    tiles = get_tiles_from(tiles_path, color_mode)

    for tile in tiles:
        try:
            avgs.append(get_average_rgb(tile))
        except ValueError:
            continue

    random.shuffle(tiles)

    # resize the input to fit original image size?
    resize_input = True

    print('Start creating mosaic photo...')

    # if images can't be reused, ensure m*n <= num_of_images
    if not duplicated_tile:
        if grid_size[0] * grid_size[1] > len(tiles):
            print(
                f"""Can\' create mosaic photo without using duplicated tile
                (Grid size less than number of total tile images)
                Exiting.""")
            exit()

    # resizing input
    if resize_input:
        print('resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims = (int(target_image.size[0] / grid_size[1]),
                int(target_image.size[1] / grid_size[0]))
        print("max tile dims: %s" % (dims,))

        # resize
        for img in tiles:
            img.thumbnail(dims)

    for tile in target_images:
        average_rgb = get_average_rgb(tile)
        match_index = get_best_match_index(average_rgb, avgs)
        output_images.append(tiles[match_index])
        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print('processed %d of %d...' % (count, len(target_images)))
        count += 1
        # remove selected image from input if flag set
        if not duplicated_tile:
            tiles.remove(match_index)

    mosaic_image = create_image_grid(output_images, grid_size)

    return mosaic_image


def generate_mosaic_photo(target_image, tiles, grid_size, duplicated_tile=True, color_mode='L',
                          output_filename='Result.jpg'):
    mosaic_image = create_mosaic_photo(target_image, tiles, grid_size, duplicated_tile, color_mode)

    # Write image out
    mosaic_image.save(output_filename, 'jpeg')

    print("Saving output to %s" % (output_filename,))
    print('Finished.')


# =======================================================================================


if __name__ == '__main__':
    original_image = Image.open('../data/Sample.jpg')
    width, height = original_image.size
    scale = 3

    target_image = original_image.resize((math.floor(width * scale), math.floor(height * scale)))

    tile_path = '../data/Dior/'
    size = 100

    # target_image = Image.open(
    #     f"""../data/{input('Enter target image name inside folder data (with the extension): ')}""")

    # # material images
    # print('reading input folder...')
    # # materials = get_material_images_directory(
    # #     f"""../data/{input('Enter the folder name of your material images: ')}/""")
    # # input_images = get_images(args.images)
    #
    # # check if any valid input images found
    # if not tiles:
    #     print('No input images found in %s. Exiting.' % ('../data/Dior/',))
    #     exit()

    # shuffle list - to get a more varied output?
    # random.shuffle(tiles)

    # size of grid
    # size = int(input('Enter the grid size: '))
    grid_size = (size, size)

    # output
    # output_filename = 'mosaic.jpeg'
    # if args.output:
    #     output_filename = args.output

    # # re-use any image in input
    # reuse_images = True
    #
    # # resize the input to fit original image size?
    # resize_input = True
    #
    # print('Start creating mosaic photo...')
    #
    # # if images can't be reused, ensure m*n <= num_of_images
    # if not reuse_images:
    #     if grid_size[0] * grid_size[1] > len(tiles):
    #         print('grid size less than number of images')
    #         exit()
    #
    # # resizing input
    # if resize_input:
    #     print('resizing images...')
    # # for given grid size, compute max dims w,h of tiles
    # dims = (int(target_image.size[0] / grid_size[1]),
    #         int(target_image.size[1] / grid_size[0]))
    # print("max tile dims: %s" % (dims,))
    # # resize
    # for img in tiles:
    #     img.thumbnail(dims)

    # create mosaic photo
    generate_mosaic_photo(target_image, tile_path, grid_size, duplicated_tile=True, color_mode='L')
