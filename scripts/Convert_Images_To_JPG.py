import os

os.getcwd()
collection = "D:/Downloads/Dior"

for i, filename in enumerate(os.listdir(collection)):
    os.rename("D:/Downloads/Dior/" + filename, "D:/Downloads/Dior/" + str(i) + ".jpg")
