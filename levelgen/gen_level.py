from PIL import Image

im = Image.open("level.png")
pixels = im.load()
x, y = im.size
level = [[-1 for i in range(x)] for j in range(y)]

for j in range(y):
    for i in range(x):
        if pixels[i, j] == (128, 64, 0, 255) or pixels[i, j] == (128, 64, 0):
            level[j][i] = 0
        elif pixels[i, j] == (237, 28, 36, 255) or pixels[i, j] == (237, 28, 36):  # цвет в RGBA и RGB
            level[j][i] = 15  # игрок
        elif pixels[i, j] == (128, 80, 0, 255) or pixels[i, j] == (128, 80, 0):
            level[j][i] = 4
        elif pixels[i, j] == (158, 64, 0, 255) or pixels[i, j] == (158, 64, 0):
            level[j][i] = 5
        elif pixels[i, j] == (98, 64, 0, 255) or pixels[i, j] == (98, 64, 0):
            level[j][i] = 3
        elif pixels[i, j] == (128, 64, 10, 255) or pixels[i, j] == (128, 64, 10):
            level[j][i] = 7
        elif pixels[i, j] == (128, 54, 10, 255) or pixels[i, j] == (128, 54, 10):
            level[j][i] = 6
        elif pixels[i, j] == (128, 54, 0, 255) or pixels[i, j] == (128, 54, 0):
            level[j][i] = 1
        elif pixels[i, j] == (128, 74, 10, 255) or pixels[i, j] == (128, 74, 10):
            level[j][i] = 8
        elif pixels[i, j] == (255, 242, 0, 255) or pixels[i, j] == (255, 242, 0):
            level[j][i] = 800
        elif pixels[i, j] == (255, 200, 0, 255) or pixels[i, j] == (255, 200, 0):
            level[j][i] = 801
        elif pixels[i, j] == (28, 235, 237, 255) or pixels[i, j] == (28, 235, 237):
            level[j][i] = 16
        elif pixels[i, j] == (1, 70, 71, 255) or pixels[i, j] == (1, 70, 71):
            level[j][i] = 702
        elif pixels[i, j] == (32, 81, 82, 255) or pixels[i, j] == (32, 81, 82):
            level[j][i] = 701
        elif pixels[i, j] == (168, 16, 23, 255) or pixels[i, j] == (168, 16, 23):
            level[j][i] = 703
        elif pixels[i, j] == (237, 225, 28, 255) or pixels[i, j] == (237, 225, 28):
            level[j][i] = 704

with open('level.csv', 'w') as file:
    file.write(str(level).replace('], ', '], \n').replace('], ', '').replace('[', '').replace(']', '').replace(' ', ''))