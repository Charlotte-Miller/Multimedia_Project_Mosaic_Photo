import os


def convert_tile_extension_to_jpg(directory_path):
    os.getcwd()
    path = directory_path + '/'

    for i, filename in enumerate(os.listdir(directory_path)):
        try:
            os.rename(path + filename, path + str(i) + ".jpg")
        except FileExistsError:
            continue


if __name__ == '__main__':
    convert_tile_extension_to_jpg(directory_path='../Assets/Face/')
