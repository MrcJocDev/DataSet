from math import sqrt, atan2, pi

import cv2 as cv #type:ignore   
import numpy as np #type:ignore


def cartesian_to_polar(x, y) -> tuple[float, float]:
    """
    Converts cartesian coordinates to polar coordinates.
    :param x: The x coordinate.
    :param y: The y coordinate.
    :return: Tuple[float, float] containing r, theta
    """
    r = sqrt(x ** 2 + y ** 2)
    theta = atan2(y, x)
    return r, theta


def polar_to_cartesian(r: int | float, theta: int | float) -> tuple[float, float]:
    """
    Converts polar coordinates to cartesian coordinates. gjj
    :param r: The r value of the coordinates.
    :param theta: The theta value of the coordinates.
    :return: tuple[float, float] of the cartesian coordinates.
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def convert_rectangular_coordinates_to_original_coordinates(x: int, y: int) -> tuple[float, float]:
    """
    Converts rectangular coordinates to original coordinates.
    :param x: X value for the rectangular coordinates.
    :param y: Y value for the rectangular coordinates.
    :return: The original coordinates.
    """
    x += INNER_CIRCLE
    theta = (y+180) * pi/180
    y2, x2 = map(int, polar_to_cartesian(x, theta+pi))

    x = y2 + cy
    y = x2 + cx

    return x, y


def convert_original_coordinates_to_rectangular_coordinates(x: int, y: int) -> tuple[float, float]:
    """
    Converts original coordinates to rectangular coordinates.
    :param x: The x value for the original coordinates.
    :param y: The y value for the original coordinates.
    :return:
    """
    # Get the polar coordinates about thr origin
    x, y = cartesian_to_polar(x-cx, y-cy)

    x = x - INNER_CIRCLE

    # If the radians are negative convert them to their positive equivalent
    if y < 0:
        y += 2 * pi

    # Convert the radians to degrees (y value is mapped 0-360)
    y *= 180 / pi

    return int(x), int(y)


def on_click_im2(event, x, y, *_):
    if event != cv.EVENT_LBUTTONDOWN:
        return None

    x, y = map(int, convert_rectangular_coordinates_to_original_coordinates(x, y))

    cv.circle(im, (x, y), 2, (0, 0, 255), thickness=-1, lineType=cv.LINE_AA)
    cv.imshow(WINDOW_NAME + ' im', im)  


def on_click_im1(event, x, y, *_):
    if event != cv.EVENT_LBUTTONDOWN:
        return None

    x, y = map(int, convert_original_coordinates_to_rectangular_coordinates(x, y))

    cv.circle(im2, (x, y), 2, (0, 0, 255), thickness=-1, lineType=cv.LINE_AA)
    cv.imshow(WINDOW_NAME + ' im2', im2)
    cv.waitKey(0)


if __name__ == '__main__':
    WINDOW_NAME = "Circle to Rectangle"

    im = cv.imread('1   .jpg')

    # Define the disk's diameters
    OUTER_CIRCLE = 200
    INNER_CIRCLE = 70

    # Define the center of the circle
    cx, cy = im.shape[0] // 2, im.shape[1] // 2
    cy -= 45

    # Display what we're transforming
    cv.circle(im, (cx, cy), 5, (0, 0, 255), -1)
    cv.circle(im, (cx, cy), OUTER_CIRCLE, (0, 255, 0), 2)
    cv.circle(im, (cx, cy), INNER_CIRCLE, (0, 255, 0), 2)

    # Define the size of the output image.
    x_distance = 360
    y_distance = OUTER_CIRCLE - INNER_CIRCLE

    # Use y, x instead of x, y, so we don't need to rotate the image after the transformation
    im2 = np.zeros((x_distance, y_distance, 3), dtype=np.uint8)

    for im2_x in range(x_distance):
        for im2_y in range(y_distance):
            im1_x, im1_y = polar_to_cartesian(INNER_CIRCLE + im2_y, im2_x * pi / 180)
            im1_x, im1_y = int(im1_x + cx), int(im1_y + cy)

            # Again, Use y, x instead of x, y, so we don't need to rotate the image after the transformation
            im2[im2_x, im2_y] = im[im1_y, im1_x]

    # Display the final image.
    cv.namedWindow(WINDOW_NAME + " im2")
    cv.setMouseCallback(WINDOW_NAME + " im2", on_click_im1)
    cv.imshow(WINDOW_NAME + " im2", im)
    cv.waitKey(0)

