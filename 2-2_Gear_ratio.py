"""
Gearing Up for Destruction
==========================

As Commander Lambda's personal assistant, you've been assigned the task of configuring the LAMBCHOP doomsday device's axial orientation gears. It should be pretty simple -- just add gears to create the appropriate rotation ratio. But the problem is, due to the layout of the LAMBCHOP and the complicated system of beams and pipes supporting it, the pegs that will support the gears are fixed in place.

The LAMBCHOP's engineers have given you lists identifying the placement of groups of pegs along various support beams. You need to place a gear on each peg (otherwise the gears will collide with unoccupied pegs). The engineers have plenty of gears in all different sizes stocked up, so you can choose gears of any size, from a radius of 1 on up. Your goal is to build a system where the last gear rotates at twice the rate (in revolutions per minute, or rpm) of the first gear, no matter the direction. Each gear (except the last) touches and turns the gear on the next peg to the right.

Given a list of distinct positive integers named pegs representing the location of each peg along the support beam, write a function solution(pegs) which, if there is a solution, returns a list of two positive integers a and b representing the numerator and denominator of the first gear's radius in its simplest form in order to achieve the goal above, such that radius = a/b. The ratio a/b should be greater than or equal to 1. Not all support configurations will necessarily be capable of creating the proper rotation ratio, so if the task is impossible, the function solution(pegs) should return the list [-1, -1].

For example, if the pegs are placed at [4, 30, 50], then the first gear could have a radius of 12, the second gear could have a radius of 14, and the last one a radius of 6. Thus, the last gear would rotate twice as fast as the first one. In this case, pegs would be [4, 30, 50] and solution(pegs) should return [12, 1].

The list pegs will be given sorted in ascending order and will contain at least 2 and no more than 20 distinct positive integers, all between 1 and 10000 inclusive.

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({4, 17, 50})
Output:
    -1,-1

Input:
Solution.solution({4, 30, 50})
Output:
    12,1

-- Python cases --
Input:
solution.solution([4, 30, 50])
Output:
    12,1

Input:
solution.solution([4, 17, 50])
Output:
    -1,-1
"""

from __future__ import print_function, division
import unittest
from fractions import gcd as get_gcd
from collections import OrderedDict as dict

thought = """
Given n pegs := [p1, p2, p3, ... , pn]
Calculate n gears (radius) := [G1, G2, G3, ..., Gn]
and their physical constrains := [G1_min <= G1 <= G1_max, G2_min <= G2 <= G2_max, ..., ]
where Gi_max denote the maximum radius before Gi collide with adjacent pegs, 
and Gi_min denote the minimum radius Gi requires to touch adjacent gears if the gears are already on their maximum radius (Gi-1_max and Gi+1_max).
If the physical constrains conflict or not possible, return impossible early

So that:
1.) "2 = (G1 / G2) * (G2 / G3) * (G3 / G4) * ... * (Gn-1 / Gn) = (G1 / Gn)"
2.) "G1 + G2 = |p2 - p1|; G2 + G3 = |p3 - p2|; ..."
3.) "pn - p1 = G1 + 2 G2 + 2 G3 + 2 G4 + ... + 2 Gn-1 + Gn"

From formula (1), we know that G1 / Gn = 2
So we can update G1_min, G1_max and Gn_min, Gn_max to 
4.) G1_min = 2 * Gn_min = max(G1_min, 2 * Gn_min)
5.) G1_max = 2 * Gn_max = min(G1_max, 2 * Gn_max)

From this point, because G1_max and Gn_max potentially got shorter, domino-ly update all adjacent gears 
"""


def simplify(a, b):
    gcd = get_gcd(a, b)
    return a // gcd, b // gcd


def solution(pegs):
    # Your code here
    n = len(pegs)
    impossible = [-1, -1]

    def gap(_a, _b):
        return pegs[max(_a, _b)] - pegs[min(_a, _b)]

    max_table = []
    for i in range(n):
        if i == 0:
            max_table.append(gap(0, 1))
        elif i == n - 1:
            max_table.append(gap(n - 2, n - 1))
        else:
            max_table.append(min(gap(i, i + 1), gap(i, i - 1)))

    min_table = []
    for i in range(n):
        if i == 0:
            min_table.append(gap(0, 1) - max_table[1])
        elif i == n - 1:
            min_table.append(gap(n - 2, n - 1) - max_table[-2])
        else:
            min_table.append(
                max(gap(i, i + 1) - max_table[i + 1], gap(i, i - 1) - max_table[i - 1])
            )
        if min_table[i] > max_table[i]:
            return impossible  # phy_constrains impossible
    if max_table[0] * 2 < min_table[-1] or min_table[0] * 2 > max_table[-1]:
        # from 2.) "2 = a / Gn"
        # if first gear cannot meet 2x gear ratio for last gear
        return impossible

    # update first and last gear so that "G1 / Gn = 2"
    new_max = min(max_table[0], 2 * max_table[-1])
    new_min = max(min_table[0], 2 * min_table[-1], 1)
    if new_min == new_max:
        n, d = simplify(new_min, 1)
        return [n, d]
    if new_min > new_max:
        return impossible
    min_table[0] = new_min
    min_table[-1] = new_min // 2
    max_table[0] = new_max
    max_table[-1] = new_max // 2

    # loop over and update every gears' constrains until converge
    modify = True
    while modify:
        modify = False
        for i in range(1, n - 1):
            print(131, dict(zip(pegs, zip(min_table, max_table))))
            new_min = max(gap(i, i - 1) - max_table[i - 1], gap(i, i + 1) - max_table[i + 1], 1)
            new_max = min(gap(i, i - 1) - min_table[i - 1], gap(i, i + 1) - min_table[i + 1])
            if new_min > new_max:
                return impossible
            if new_max != max_table[i] or new_min != min_table[i]:
                modify = True
                max_table[i] = new_max
                min_table[i] = new_min
        print(140, dict(zip(pegs, zip(min_table, max_table))))

        # update first gear
        new_min = max(gap(0, 1) - max_table[1], 1)
        new_max = gap(0, 1) - min_table[1]
        if new_min > new_max:
            print(146, new_min, new_max)
            return impossible
        if new_max != max_table[0] or new_min != min_table[0]:
            modify = True
            min_table[0] = new_min
            max_table[0] = new_max

        # update last gear
        new_min = max(gap(n - 2, n - 1) - max_table[-2], 1)
        new_max = gap(n - 2, n - 1) - min_table[-2]
        if new_min > new_max:
            print(155, new_min, new_max)
            return impossible
        if new_max != max_table[-1] or new_min != min_table[-1]:
            modify = True
            min_table[-1] = new_min
            max_table[-1] = new_max

        print(160, dict(zip(pegs, zip(min_table, max_table))))
        # update first and last gear so that "G1 / Gn = 2"
        new_max = min(max_table[0], 2 * max_table[-1])
        new_min = max(min_table[0], 2 * min_table[-1], 1)
        if new_min == new_max:
            n, d = simplify(new_min, 1)
            return [n, d]
        if new_min > new_max:
            print(168, new_min, new_max)
            return impossible
        if new_max != max_table[0] or new_min != min_table[0]:
            modify = True
            min_table[0] = new_min
            max_table[0] = new_max

        if new_max // 2 != max_table[-1] or new_min // 2 != min_table[-1]:
            modify = True
            min_table[-1] = new_min // 2
            max_table[-1] = new_max // 2

    return dict(zip(pegs, zip(min_table, max_table)))


class TestCase(unittest.TestCase):

    def test_30_60(self):
        self.assertEqual(solution([30, 60]), [20, 1])

    def test_4_30_50(self):
        self.assertEqual(solution([4, 30, 50]), [12, 1])

    def test_4_17_50(self):
        self.assertEqual(solution([4, 17, 50]), [-1, -1])

    def test_4_6_50_first_gear_too_small(self):
        self.assertEqual(solution([4, 6, 50]), [-1, -1])

    def test_4_48_50_first_gear_too_large(self):
        self.assertEqual(solution([4, 48, 50]), [-1, -1])

    def test_4_6_50_52_pegs_too_far(self):
        self.assertEqual(solution([4, 6, 50, 52]), [-1, -1])


if __name__ == "__main__":
    unittest.main(verbosity=9)
    # print(solution([4, 30, 50]))
    # print(solution([30, 60]))
