input = ''' \
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''
'''
output = 58 steps state before gridlocked
..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..

adjacent: Generator DFS
step_east x then step_south y
if x[-1], y[-1]: x[1], y[-1] wrapped around
for step in
    if adjacent == 0: if x[-1]; x = 0 else: if no x: y +=1 x += 1 step += 1
ret step

'''
s1 = open('map_move_simulation.txt').read().split()
# s1 = input.split()
# print(s1)
w, h = len(s1[0]), len(s1)
m = 0
finished = False
while not finished:
    finished = True
    s_new = []
    for s in s1:
        if s[w - 1] + s[0] == '>.':
            s = 'p' + s[1: w - 1] + ':'
        s_new += [s.replace('>.', '.>').replace(':', '.').replace('p', '>')]
        if s_new[-1] != s:
            finished = False
    # transpose
    s1 = [''.join(i) for i in zip(*s_new)]

    s_new = []
    for s in s1:
        if s[h - 1] + s[0] == 'v.':
            s = 'p' + s[1: h - 1] + ':'
        s_new += [s.replace('v.', '.v').replace(':', '.').replace('p', 'v')]
        if s_new[-1] != s:
            finished = False
    # transpose
    s1 = [''.join(i) for i in zip(*s_new)]
    m += 1

print(m)


















#end
