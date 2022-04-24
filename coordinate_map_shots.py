from __future__ import annotations

input = '''\
target area: x=20..30, y=-10..-5
'''
txt = open('coordinate_map_shots.txt', 'r')
input1 = txt.read()

'''
output = 6,9 max_y = 45

arch parabola vertex(sharpest turn)(halfway between the focus and directrix)
initial: x forward to the right, y upward
x, y position add by x, y velocity
drag: x -1 if > 0, +1 if < 0
gravity: y -1
target area: x=20..30, y=-10..-5
simulation trajectory: max y overshoot the target area
zero -> negtive 6,3
check the bounds
...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

algorithm/brutal force:
test each x, y on each step and compare max(y)
parse: split('') [2: -1] split('..')
max_y = 0
range: (x1, abs(x1)) (2 * y + 2) (x1, x2) (y1, y2) >x2, <y1
var: vx, vy x_p, y_p max path x_p += vx max(vx - 1, 0) vy -=1
res: max path = 0 max(max path, y_p) max(max path, max_y)

'''

def compute(s: str) -> int:
    _, _, x_s, y_s = s.split()
    xs = x_s[2: -1]
    ys = y_s[2:]
    x1_s, x2_s = xs.split('..')
    y1_s, y2_s = ys.split('..')
    x1, x2, y1, y2 = int(x1_s), int(x2_s), int(y1_s), int(y2_s)
    print('Coords ', x1, x2, y1, y2)
    max_y = 0
    total = 0
    for y in range(y1, abs(y1)):
        for x in range(1, x2 + 1):
            vx, vy = x, y
            x_p, y_p = 0, 0
            max_y_path = 0
            for t in range(2 * abs(y1) + 2):
                x_p += vx
                y_p += vy
                vx = max(vx - 1, 0)
                vy -= 1
                max_y_path = max(max_y_path, y_p)
                if x1 <= x_p <= x2 and y1 <= y_p <= y2:
                    # print('X, Y pos ', x_p, y_p)
                    max_y = max(max_y_path, max_y)
                    total += 1
                    break
                elif x_p > x2 or y_p < y1:
                    break
    return max_y, total

print(compute(input1))











# end
