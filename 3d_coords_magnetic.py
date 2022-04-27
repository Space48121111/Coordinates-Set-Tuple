from __future__ import annotations
from collections import Counter
from typing import NamedTuple

input = '''\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
'''

'''
output = 79 beacons in total
output1 = 3621 largest apart 1197 + 1175 + 1249 scanners2 (1105,-1205,1229) and 3 (-92,-2380,-20)
x, y, z pos: >= 12 beacons adjacent contiguous differ the same -> DFS
magnetic: 24 beacons pair rotate clockwise canonical swap flip mirror
12 beacons overlapping detection cubes from perspective0(relative pos to scanner0):
-618,-824,-621
-537,-823,-458
-447,-329,318
404,-588,-901
544,-627,-890
528,-643,409
-661,-816,-575
390,-675,-793
423,-701,434
-345,-311,381
459,-707,401
-485,-357,347
overlapping detection cubes from perspective1:
686,422,578
605,423,415
515,917,-361
-336,658,858
-476,619,847
-460,603,-452
729,430,532
-322,571,750
-355,545,-477
413,935,-424
-391,539,-444
553,889,-390
scanner1: 68,-1246,-43(relative to 0)
Mahatten distance: sum(abs(p1 - p2))

'''

class Scanner(NamedTuple):
    s_id: int
    points: list[tuple[int, int, int]]
    @classmethod
    def parse(cls, s: str) -> Scanner:
        lines = s.splitlines()
        _, _, s_id_s, _ = lines[0].split()
        points = []
        for line in lines[1:]:
            x, y, z = line.split(',')
            x = int(x)
            y = int(y)
            z = int(z)
            points.append((x, y, z))
        return cls(int(s_id_s), points)
class AxisInfo(NamedTuple):
    axis: int
    sign: int
    diff: int
def x_edge_from(src: Scanner, scanner_by_id: dict[int, Scanner]) -> dict[int, AxisInfo]:
    x_edges = {}
    for other in scanner_by_id.values():
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_x: Counter[int] = Counter()
                for x, _, _ in src.points:
                    for other_pt in other.points:
                        d_x[x - sign * other_pt[axis]] += 1
                (x_diff, x_n), = d_x.most_common(1)
                # print('X diff ', x_diff, x_n)
                if x_n >= 12:
                    x_edges[other.s_id] = AxisInfo(axis = axis, sign = sign, diff = x_diff)
    return x_edges

def yz_edge_from(src: Scanner, x_edges: dict[int, AxisInfo], scanner_by_id: dic[int, Scanner]) -> tuple[dict[int, AxisInfo], dict[int, AxisInfo]]:
    y_edges = {}
    z_edges = {}
    for dst_id in x_edges:
        other = scanner_by_id[dst_id]
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_y: Counter[int] = Counter()
                d_z: Counter[int] = Counter()
                # print('Counter y z', d_y, d_z)
                for _, y, z in src.points:
                    for other_pt in other.points:
                        d_y[y - sign * other_pt[axis]] += 1
                        d_z[z - sign * other_pt[axis]] += 1
                (y_diff, y_n), = d_y.most_common(1)
                if y_n >= 12:
                    y_edges[dst_id] = AxisInfo(axis = axis, sign = sign, diff = y_diff)

                (z_diff, z_n), = d_z.most_common(1)
                if z_n >= 12:
                    z_edges[dst_id] = AxisInfo(axis = axis, sign = sign, diff = z_diff)

    return y_edges, z_edges

def compute(s: str) -> int:
    scanners = [Scanner.parse(part) for part in s.split('\n\n')]
    scanner_by_id = {scanner.s_id: scanner for scanner in scanners}
    scanner_pos = {0: (0, 0, 0)}
    all_pts = set(scanner_by_id[0].points)
    stack = [scanner_by_id.pop(0)]
    print('Stack ', stack)
    while stack:
        src = stack.pop()
        x_edges = x_edge_from(src, scanner_by_id)
        y_edges, z_edges = yz_edge_from(src, x_edges, scanner_by_id)
        for k in x_edges:
            print('K ', k)
            dst_x = x_edges[k].diff
            dst_y = y_edges[k].diff
            dst_z = z_edges[k].diff
            print('Diff x y z', dst_x, dst_y, dst_y)
            scanner_pos[k] = (dst_x, dst_y, dst_z)
            next_s = scanner_by_id.pop(k)
            print('Next s ', next_s)
            next_s.points[:] = [(
                dst_x + x_edges[k].sign * pt[x_edges[k].axis],
                dst_y + y_edges[k].sign * pt[y_edges[k].axis],
                dst_z + z_edges[k].sign * pt[z_edges[k].axis]
            ) for pt in next_s.points]
            all_pts.update(next_s.points)
            stack.append(next_s)

    # return len(all_pts)

    largest_dst = 0
    pos = list(scanner_pos.values())
    for i, (x1, y1, z1) in enumerate(pos):
        for x2, y2, z2 in pos[i:]:
            largest_dst = max(largest_dst,
            abs(x2 - x1) + abs(y2 - y1) + abs(z2 -z1)
            )

    return largest_dst


print(compute(input))









# end
