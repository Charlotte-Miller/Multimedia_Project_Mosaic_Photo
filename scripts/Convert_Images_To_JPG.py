import os

os.getcwd()
collection = "D:/Downloads/Cardi B"

for i, filename in enumerate(os.listdir(collection)):
    os.rename("D:/Downloads/Cardi B/" + filename, "D:/Downloads/Cardi B/" + str(i) + ".jpg")
