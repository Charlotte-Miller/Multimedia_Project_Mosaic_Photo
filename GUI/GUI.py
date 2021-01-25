from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, ttk

# Initial setting for app's GUI
root = Tk()
root.configure(background="black")
root.geometry("800x600")
root.title('Mosaic Photo Generator')
root.iconbitmap('./Assets/icon.ico')


def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo  # avoid garbage collection


background_image = Image.open('./Assets/background.png')
copy_of_image = background_image.copy()
photo = ImageTk.PhotoImage(background_image)
label = ttk.Label(root, image=photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand=YES)


# Setting background image
# background_image = ImageTk.PhotoImage(Image.open('./Assets/background.png'))
# background_label = Label(root, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)


def open_target_image():
    global target_image

    # Get the imported image's path
    root.image_path = filedialog.askopenfilename(initialdir='../data', title='Select Target Image',
                                                 filetypes=(('jpg files', '*.jpg'), ('all files', '*.*')))

    # Get image by path
    target_image = ImageTk.PhotoImage(Image.open(root.image_path))

    # Show image
    Label(image=target_image).grid(column=1, row=0)


# Open target image button
open_target_image_button = Button(root, text='Select image', command=open_target_image)
open_target_image_button.grid(column=0, row=0)

root.mainloop()
