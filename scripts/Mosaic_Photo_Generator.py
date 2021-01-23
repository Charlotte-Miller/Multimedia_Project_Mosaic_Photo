#!/usr/bin/env python
import os, random, argparse
from PIL import Image
import numpy as np


def get_material_images_directory(materials_directory):
    files = os.listdir(materials_directory)
    materials = []

    for file in files:
        file_path = os.path.abspath(os.path.join(materials_directory, file))
        try:
            fp = open(file_path, "rb")
            im = Image.open(fp)
            materials.append(im)
            im.load()
            fp.close()
        except:
            print("Invalid image: %s" % (file_path,))

    return materials


def get_average_rgb(image):
    im = np.array(image)
    w, h, d = im.shape
    return tuple(np.average(im.reshape(w * h, d), axis=0))


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


def create_mosaic_photo(target_image, input_images, grid_size,
                        reuse_images=True):
    target_images = split_image(target_image, grid_size)

    output_images = []
    count = 0
    batch_size = int(len(target_images) / 10)
    avgs = []
    for img in input_images:
        try:
            avgs.append(get_average_rgb(img))
        except ValueError:
            continue

    for img in target_images:
        avg = get_average_rgb(img)
        match_index = get_best_match_index(avg, avgs)
        output_images.append(input_images[match_index])
        if count > 0 and batch_size > 10 and count % batch_size is 0:
            print('processed %d of %d...' % (count, len(target_images)))
        count += 1
        # remove selected image from input if flag set
        if not reuse_images:
            input_images.remove(match_index)

    mosaic_image = create_image_grid(output_images, grid_size)
    return (mosaic_image)


### ---------------------------------------------


target_image = Image.open('../data/AirJordan.jpg')

# material images
print('reading input folder...')
materials = get_material_images_directory('../data/Dior/')
# input_images = get_images(args.images)

# check if any valid input images found
if not materials:
    print('No input images found in %s. Exiting.' % ('../data/Dior/',))
    exit()

# shuffle list - to get a more varied output?
random.shuffle(materials)

# size of grid
grid_size = (200, 200)

# output
output_filename = 'mosaic.jpeg'
# if args.output:
#     output_filename = args.output

# re-use any image in input
reuse_images = True

# resize the input to fit original image size?
resize_input = True

print('starting mosaic photo generator...')

# if images can't be reused, ensure m*n <= num_of_images
if not reuse_images:
    if grid_size[0] * grid_size[1] > len(materials):
        print('grid size less than number of images')
        exit()

# resizing input
if resize_input:
    print('resizing images...')
    # for given grid size, compute max dims w,h of tiles
    dims = (int(target_image.size[0] / grid_size[1]),
            int(target_image.size[1] / grid_size[0]))
    print("max tile dims: %s" % (dims,))
    # resize
    for img in materials:
        img.thumbnail(dims)

# create mosaic photo
mosaic_image = create_mosaic_photo(target_image, materials, grid_size, reuse_images)

# write out mosaic
mosaic_image.save(output_filename, 'jpeg')

print("saved output to %s" % (output_filename,))
print('done.')
