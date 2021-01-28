# Mosaic Photo Generator

The program is made to generate a mosaic photo base on bunches of tile image. (specific from a folder)

Briefly, it uses average RGB color of each tiles image, compare to the average RGB of each split image (from original image). After that, put all the matched tile in a list then start creating a photo base on these matched images.

## Installation
Python version: 3.8.5

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
python3 -m pip install --upgrade pip
python3 -m pip install numpy
python3 -m pip install --upgrade Pillow
```

## Usage
1. Make sure folder to tiles image only contain image file and these files extension is .jpg or .jpeg. Convert all other image extension to .jpg by executing Convert_Images_To_JPG.py

```python
if __name__ == '__main__':
    convert_tile_extension_to_jpg(directory_path='../data/Face/')
```



2. Adjust the output mosaic photo by configuring these parameters of the generate_mosaic_photo() function in main.

```python
if __name__ == '__main__':
    generate_mosaic_photo(target_image='../data/Face.jpg',
                          tiles_path='../data/Face/',
                          output_filename='Result.jpg',
                          scale=5,
                          grid_size=(150, 150),
                          duplicated_tile=True,
                          color_mode='RGB')
```
Explain:
- target_image: path to the image which is used to make a mosaic photo.
- tiles_path: path to the directory of tile images.
- output_filename: path to the generated mosaic photo.
- scale: zoom level of the image after converting to the mosaic photo.
- grid_size: determine how many times you want to split the original image.
- duplicated_tile: allowing the program to use a tile image multiple time or not(otherwise, you have to make sure there's enough of tile image in the tiles folder fit up the grid_size).
- color_mode: 'RGB' for colorful, 'L' for grayscale

3. Execute Mosaic_Photo_Generator.py
