from math import pi, sin, atan


def circle_area(rad):

    return rad**2 * pi


def triangle_area(ray1, ray2, angle):

    # angle in radians

    return round((ray1*ray2*(sin(angle*pi/180)))/2, 2)


def angle(t1, t2):

    # didn't even need the y intersection point, used trigonometry to solve.

    m1 = t1[0]
    m2 = t2[0]

    alpha = abs(atan(1/m1)*180/pi)

    beta = abs(atan(1/m2)*180/pi)

    return alpha+beta

assert str(angle((2, 4), (-3, 16))) == "45.0"
assert str(circle_area(10))== "314.1592653589793"
assert str(triangle_area(4, 8, 30)) == "8.0"
