from __future__ import annotations

txt = open('coordinates_set_tuple.txt' , 'r')
input1 = txt.read()
input = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''

'''
output = 17
#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

algorithm/brutal force:
parsing: lines, folds = input.split('\n\n') x, y = splitlines. split(',')
points = set() -> no overlapping points.add(x, y)
axis = lines, fold_p in folds.splitlines() .split('=') [-1]
fold: (x1, y1) y0 (x1, y0 + (y0 - y1))
axis = 'y': points y = 2 * fold_p - y
axis = 'x':
visible dots: len(points(points)))

drawing: within max range double for loops #
'''
def print_points(points: set[tuple[int, int]]) -> None:
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in points:
                print('#', end = ' ')
            else:
                print('.', end = ' ')
        print()

lines, folds = input.split('\n\n')
points = set()
for line in lines.splitlines():
    x, y = line.split(',')
    points.add((int(x), int(y)))

for fold in folds.splitlines():
    axis_s, fold_p_s = fold.split('=')
    fold_p = int(fold_p_s)
    axis = axis_s[-1]

    if axis == 'x':
        points = {
            (
             x if x < fold_p else 2 * fold_p - x,
             y
            )
            for x, y in points
        }
    elif axis =='y':
        points = {
            (
            x,
            y if y < fold_p else 2 * fold_p - y,
            )
            for x, y in points
        }
    else:
        raise AssertionError(f'Wrong axis {axis}')

    # break

print_points(points)
print(len(points))






# end
