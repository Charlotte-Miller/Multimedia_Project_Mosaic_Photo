import os


def convert_tile_extension_to_jpg(collection):
    os.getcwd()
    path = collection + '/'

    for i, filename in enumerate(os.listdir(collection)):
        try:
            os.rename(path + filename, path + str(i) + ".jpg")
        except FileExistsError:
            pass
