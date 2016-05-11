"""
seamCarver.py
Frederik Roenn Stensaeth
04.22.16

Python program to perform content-aware image resizing using seam carving.
"""

import sys
from PIL import Image

def carveSeams(filename, seam_num, direction):
    """
    carveSeams() resizes an image by finding a given amount of 'seams' and
    removing them.

    @params: filename,
             number of seams to be removed,
             direction of the resizing
    @return: resized image
    """
    im = Image.open(filename)
    new_image = im

    if direction != 'V' and direction != 'H':
        print 'Error. Sorry, direction needs to be either V or H...'
        sys.exit(1)

    while seam_num > 0:
        print 'Seam number: ' + str(seam_num)
        new_image = carveSeam(new_image, direction)
        seam_num -= 1

    return new_image

def carveSeam(image, direction):
    """
    carveSeam() removes a single seam from an image. Computes the energy
    before finding and removing a seam.

    @params: image, direction of seam
    @return: image (w/o one seam)
    """
    energy = computeEnergy(image)
    seam = findSeam(energy, direction)
    new_image = removeSeam(image, seam, direction)
    return new_image

def computeEnergy(im):
    """
    computeEnergy() computes the energy table for an image.

    @params: image
    @return: energy table
    """
    width, height = im.size
    image = im.load()
    energy_table = [[None for y in range(height)] for x in range(width)]

    # loop over every pixel in the image and compute its energy.
    # the energy of a pixel is defined as the difference in the rgb value of
    # surrounding pixels.
    for y in range(height):
        for x in range(width):
            if x == 0:
                x_1 = image[x, y]
                x_2 = image[x + 1, y]
            elif x == width - 1:
                x_1 = image[x - 1, y]
                x_2 = image[x, y]
            else:
                x_1 = image[x - 1, y]
                x_2 = image[x + 1, y]

            if y == 0:
                y_1 = image[x, y]
                y_2 = image[x, y + 1]
            elif y == height - 1:
                y_1 = image[x, y - 1]
                y_2 = image[x, y]
            else:
                y_1 = image[x, y - 1]
                y_2 = image[x, y + 1]

            # compute the difference in the rgb values and sum them.
            x_red = abs(x_1[0] - x_2[0])
            x_green = abs(x_1[1] - x_2[1])
            x_blue = abs(x_1[2] - x_2[2])

            y_red = abs(y_1[0] - y_2[0])
            y_green = abs(y_1[1] - y_2[1])
            y_blue = abs(y_1[2] - y_2[2])

            energy = x_red + x_green + x_blue + y_red + y_green + y_blue

            energy_table[x][y] = energy

    return energy_table

def findHorizontalSeam(energy_table):
    """
    findHorizontalSeam() finds a horizontal seam using an energy table.
    The lowest energy seam is found, as it traces out the path from left to
    right in the picture where the least amount of stuff is "happening".

    @params: energy table
    @return: seam (two dimensional list)
    """
    width = len(energy_table)
    height = len(energy_table[0])
    seam_dynamic = [[None for y in range(height)] for x in range(width)]
    backtracker = [[None for y in range(height)] for x in range(width)]

    # loops over the energy table to find the lowest energy path. we are
    # looking for the lowest energy path, because it tells us where the least
    # is "happening" in the image.
    for x in range(width):
        for y in range(height):
            if x == 0:
                seam_dynamic[x][y] = energy_table[x][y]
                backtracker[x][y] = -1
            else:
                if y == 0:
                    minimum = min(seam_dynamic[x - 1][y], seam_dynamic[x - 1][y + 1])
                    if minimum == seam_dynamic[x - 1][y]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 2
                elif y == height - 1:
                    minimum = min(seam_dynamic[x - 1][y], seam_dynamic[x - 1][y - 1])
                    if minimum == seam_dynamic[x - 1][y]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 0
                else:
                    minimum = min(seam_dynamic[x - 1][y - 1], seam_dynamic[x - 1][y], seam_dynamic[x - 1][y + 1])
                    if minimum == seam_dynamic[x - 1][y - 1]:
                        backtracker[x][y] = 0
                    elif minimum == seam_dynamic[x - 1][y]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 2

                seam_dynamic[x][y] = energy_table[x][y] + minimum
    
    # now that we have computed the paths, we need to backtrace the min one.
    # first we need to find the min at the end.
    min_num = seam_dynamic[width - 1][0]
    min_index = 0
    for y in range(height):
        if min_num > seam_dynamic[width - 1][y]:
            min_index = y
            min_num = seam_dynamic[width - 1][y]

    # now that we have the min we need to backtrace it.
    y_index = min_index
    x_index = width - 1
    seam = [[None for y in range(2)] for x in range(width)]
    seam[x_index][0] = x_index
    seam[x_index][1] = y_index
    while x_index > 0:
        backtrack = backtracker[x_index][y_index]
        if backtrack == 0:
            y_index -= 1
        elif backtrack != 1:
            y_index += 1
        x_index -= 1

        seam[x_index][0] = x_index
        seam[x_index][1] = y_index

    return seam

def findVerticalSeam(energy_table):
    """
    findVerticalSeam() finds a vertical seam using an energy table.
    The lowest energy seam is found, as it traces out the path from top to
    bottom in the picture where the least amount of stuff is "happening".

    @params: energy table
    @return: seam (two dimensional list)
    """
    width = len(energy_table)
    height = len(energy_table[0])
    seam_dynamic = [[None for y in range(height)] for x in range(width)]
    backtracker = [[None for y in range(height)] for x in range(width)]

    # loops over the energy table to find the lowest energy path. we are
    # looking for the lowest energy path, because it tells us where the least
    # is "happening" in the image.
    for y in range(height):
        for x in range(width):
            if y == 0:
                seam_dynamic[x][y] = energy_table[x][y]
                backtracker[x][y] = -1
            else:
                if x == 0:
                    minimum = min(seam_dynamic[x][y - 1], seam_dynamic[x + 1][y - 1])
                    if minimum == seam_dynamic[x][y - 1]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 2
                elif x == width - 1:
                    minimum = min(seam_dynamic[x][y - 1], seam_dynamic[x - 1][y - 1])
                    if minimum == seam_dynamic[x][y - 1]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 0
                else:
                    minimum = min(seam_dynamic[x - 1][y - 1], seam_dynamic[x][y - 1], seam_dynamic[x + 1][y - 1])
                    if minimum == seam_dynamic[x - 1][y - 1]:
                        backtracker[x][y] = 0
                    elif minimum == seam_dynamic[x][y - 1]:
                        backtracker[x][y] = 1
                    else:
                        backtracker[x][y] = 2

                seam_dynamic[x][y] = energy_table[x][y] = minimum
    
    # now that we have computed the paths, we need to backtrace the min one.
    # first we need to find the min at the end.
    min_num = seam_dynamic[0][height - 1]
    min_index = 0
    for x in range(width):
        if min_num > seam_dynamic[x][height - 1]:
            min_index = x
            min_num = seam_dynamic[x][height - 1]

    # now that we have the min we need to backtrace it.
    y_index = height - 1
    x_index = min_index
    seam = [[None for y in range(2)] for x in range(height)]
    seam[y_index][0] = x_index
    seam[y_index][1] = y_index
    while y_index > 0:
        backtrack = backtracker[x_index][y_index]
        if backtrack == 0:
            x_index -= 1
        elif backtrack != 1:
            x_index += 1
        y_index -= 1

        seam[y_index][0] = x_index
        seam[y_index][1] = y_index

    return seam

def findSeam(energy_table, direction):
    """
    findSeam() finds and returns the lowest energy seam in an energy table.

    @params: energy table, direction of seam 
    @return: seam (two dimensional list)
    """
    if direction == 'V':
        seam = findVerticalSeam(energy_table)
    elif direction == 'H':
        seam = findHorizontalSeam(energy_table)
    else:
        print 'Invalid direction: ' + direction
        sys.exit(1)

    return seam

def removeSeam(im, seam, direction):
    """
    removeSeam() removes a provided seam from a given image.

    @params: image, seam, direction of seam
    @return: image (w/o one seam)
    """
    width, height = im.size
    image = im.load()

    # remove the provided seam from the image by backtracking the seam through
    # the image and bumping pixels over to effectively remove the pixels in
    # the seam.
    if direction == 'V':
        new_image = Image.new("RGB", (width - 1, height), "white")
        pix = new_image.load()
        for y in range(height):
            shift = False
            for x in range(width):
                if not ((seam[y][0] == x) and (seam[y][1] == y)):
                    color = image[x, y]
                    if shift:
                        pix[x -1, y] = color
                    else:
                        pix[x, y] = color
                else:
                    shift = True
    elif direction == 'H':
        new_image = Image.new("RGB", (width, height - 1), "white")
        pix = new_image.load()
        for x in range(width):
            shift = False
            for y in range(height):
                if not ((seam[x][0] == x) and (seam[x][1] == y)):
                    color = image[x, y]
                    if shift:
                        pix[x, y - 1] = color
                    else:
                        pix[x, y] = color
                else:
                    shift = True
    else:
        print 'Invalid direction: ' + direction
        sys.exit(1)

    return new_image

def main():
    if len(sys.argv) < 5:
        print 'Too few arguments provided.'
        print 'Usage: $ python seamCarver.py <input filename> <num of seams> <seam direction> <output filename> [--show]'
        sys.exit(1)
    image = carveSeams(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    image.save(sys.argv[4])
    if len(sys.argv) == 6 and sys.argv[5] == '--show':
        image.show()

if __name__ == '__main__':
    main()