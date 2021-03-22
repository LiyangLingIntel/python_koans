#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.

# Triangle analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#

def check_edges(a, b, c):
    if a < 0 or b < 0 or c < 0:
        return False
    edges = sorted([a, b, c])
    if edges[0] + edges[1] <= edges[2]:
        return False
    return True


def triangle(a, b, c):
    # DELETE 'PASS' AND WRITE THIS CODE

    if not check_edges(a, b, c):
        raise TriangleError

    edges = {a, b, c}
    if len(edges) == 1:
        return 'equilateral'
    elif len(edges) == 2:
        return 'isosceles'
    else:
        return 'scalene'


# Error class used in part 2.  No need to change this code.
class TriangleError(Exception):
    pass
