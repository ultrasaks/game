from PIL import Image

im = Image.open("level.png")
pixels = im.load()
x, y = im.size
level = [[-1 for i in range(x)] for j in range(y)]

for j in range(y):
    for i in range(x):
        if pixels[i, j] == (128, 64, 0, 255):
            level[j][i] = 7
        elif pixels[i, j] == (237, 28, 36, 255):  # цвет в RGBA
            level[j][i] = 15  # игрок
        elif pixels[i, j] == (113, 56, 0, 255):
            level[j][i] = 4

with open('level.csv', 'w') as file:
    file.write(str(level).replace('], ', '], \n').replace('], ', '').replace('[', '').replace(']', '').replace(' ', ''))