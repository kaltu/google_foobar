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

import unittest

thought = """
Given n pegs := [p1, p2, p3, ... , pn]
Calculate n - 1 gears := [a, b, c, d, e, ...]
and their constrains C := [a_min <= a <= a_max, b_min <= b <= b_max, ..., ]
If constrains conflict or not possible, return impossible early
So that:
1.) "2 = (a / b) * (b / c) * (c / d) * ... * (Gn-2 / Gn-1) = (a / Gn-1)"
2.) "a + b = p2 - p1; b + c = p3 - p2; ..."
3.) "pn - p1 = a + 2b + 2c + 2d + ... + 2Gn-2 + Gn-1"
"""


def solution(pegs):
    # Your code here
    n = len(pegs)
    impossible = [-1, -1]

    from fractions import gcd as get_gcd

    def gap(a, b):
        return pegs[max(a, b)] - pegs[min(a, b)]

    def simplify(a, b):
        gcd = get_gcd(a, b)
        return a / gcd, b / gcd

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
            return impossible
    phy_constrains = dict(zip(pegs, zip(min_table, max_table)))
    return phy_constrains


class TestCase(unittest.TestCase):
    def test_4_30_50(self):
        self.assertEqual(solution([4, 30, 50]), [12, 1])

    def test_4_17_50(self):
        self.assertEqual(solution([4, 17, 50]), [-1, -1])

    def test_15_17_50_52(self):
        self.assertEqual(solution([15, 17, 50, 52]), [-1, -1])


if __name__ == "__main__":
    unittest.main(verbosity=9)
