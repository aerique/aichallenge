#!/usr/bin/python
from random import randrange
from math import sqrt
import Image, ImageDraw, ImageChops

LAND = 0
FOOD = -1
WALL = -2

WALL_COLOR = (128, 128, 128)
LAND_COLOR = (139, 69, 19)
FOOD_COLOR = (255, 255, 255)

def distance(x1, y1, x2, y2, width, height):
    x1 = x1 % width
    x2 = x2 % width
    y1 = y1 % height
    y2 = y2 % height
    d_x = min(abs(x1 - x2), width - abs(x1 - x2))
    d_y = min(abs(y1 - y2), height - abs(y1 - y2))
    return d_x**2 + d_y**2

def voronoi(players=4):
    width = randrange(64, 256)
    height = randrange(64, 256)
    point_count = randrange(players*3, players*6)
    min_dist = width * height / point_count
    print('%s, %s  %s %s' % (width, height, min_dist, sqrt(min_dist)))
    px, py = 0, 0
    points = []
    while min_dist > 100 and len(points) < point_count:
        while min_dist > 100:
            px, py = randrange(width), randrange(height)
            for nx, ny in points:
                if distance(px, py, nx, ny, width, height) < min_dist:
                    break
            else:
                break
            min_dist -= 1
        points.append((px, py))
    #for px, py in points:
    #    for nx, ny in points:
    #        print('(%s)-(%s) = %s' % ((px,py),(nx,ny),distance(px, py, nx, ny, width, height)))
    path = {}
    closest = {}
    for p_x, p_y in points:
        nearest = {}
        for n_x, n_y in points:
            if (p_x, p_y) != (n_x, n_y):
                dist = distance(p_x, p_y, n_x, n_y, width, height)
                nearest[dist] = (n_x, n_y)
        sorted = nearest.keys()
        sorted.sort()
        path[(p_x, p_y)] = [nearest[key] for key in sorted[:3]]
        closest[(p_x, p_y)] = sorted[0]
    image = Image.new('RGB', (width, height), WALL_COLOR)
    draw = ImageDraw.Draw(image)
    for point in points:
        image.putpixel(point, (0,0,0))
        size = int(sqrt(closest[point]))//2 - 2
        draw.ellipse((point[0]-size, point[1]-size, point[0]+size, point[1]+size),
                fill=LAND_COLOR, outline=LAND_COLOR)
    from_point = (width//2, height//2)
    for point, path_neighbors in path.items():
        offset = (width//2 - point[0], height//2 - point[1])
        image = ImageChops.offset(image, offset[0], offset[1])
        draw = ImageDraw.Draw(image)
        for neighbor in path_neighbors:
            to_point = ((neighbor[0] + offset[0]) % width, (neighbor[1] + offset[1]) % height)
            draw.line((from_point, to_point), width=randrange(3,6), fill=LAND_COLOR)
        image = ImageChops.offset(image, -offset[0], -offset[1])
    image = image.resize((width*4, height*4))
    image.save('voronoi.png')
    
def random_box():
    players = 4
    width = randrange(16, 64) * 2
    height = randrange(16, 64) * 2
    m = [[WALL for x in range(width)] for y in range(height)]
    def carve(row, col):
        if m[row][col] == WALL:
            m[row][col] = LAND
    for box in range(randrange(7,14)):
        l = randrange(width-5)
        t = randrange(height-5)
        r = randrange(l+2, min(l+width//4,width))
        b = randrange(t+2, min(t+height//4,height))
        for y in range(t, b+1):
            for x in range(l, r+1):
                carve(y, x)
        for y in range(height-b-1, height-t):
            for x in range(l, r+1):
                carve(y, x)
        for y in range(t, b+1):
            for x in range(width-r-1, width-l):
                carve(y, x)
        for y in range(height-b-1, height-t):
            for x in range(width-r-1, width-l):
                carve(y, x)
        if box == 0:
            m[t][l] = 1
            m[height-t-1][l] = 2
            m[t][width-l-1] = 3
            m[height-t-1][width-l-1] = 4
            for y in range(t+1, height-t-1):
                carve(y, l)
                carve(y, width-l-1)
            for x in range(l+1, width-l-1):
                carve(t, x)
                carve(height-t-1, x)
    return ant_map(m)

def ant_map(m):
    tmp = 'D %s %s 4\n' % (len(m[0]), len(m))
    for row in m:
        tmp += 'M '
        for col in row:
            if col == LAND:
                tmp += '.'
            elif col == WALL:
                tmp += 'X'
            else:
                tmp += chr(col + 96)
        tmp += '\n'
    return tmp
    
if __name__ == '__main__':
    voronoi()
