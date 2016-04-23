"""
seamCarver.py
Frederik Roenn Stensaeth
04.22.16

Python implementation of a content-aware image resizing algorithm.
"""

import sys
from PIL import Image

def carveSeams(filename, seam_num, direction):
	print 'Running: carve()'
	print 'File: ' + filename
	print 'Number of seams: ' + str(seam_num)
	print 'Direction: ' + direction

	im = Image.open(filename)
	image = im.load()
	new_image = image

	while seam_num > 0:
		print 'Seam number: ' + str(seam_num)
		new_image = carveSeam(new_image, direction)
		num -= 1

	showImage(new_image)

	return new_image

def carveSeam(image, direction):
	print 'Running: carseSeam()'

	energy = computeEnergy(image)
	seam = findSeam(energy, direction)
	new_image = removeSeam(image, seam, direction)
	return new_image

def computeEnergy(image):
	print 'Running: computeEnergy()'

	width, height = image.size
	energy_table = [[None for y in range(height)] for x in range(width)]

	for y in range(height):
		for x in range(width):
			if x == 0:
				x_1 = image[x, y]
				x_2 = image[x + 1, y]
			else if x == width - 1:
				x_1 = image[x - 1, y]
				x_2 = image[x, y]
			else:
				x_1 = image[x - 1, y]
				x_2 = image[x + 1, y]

			if y == 0:
				y_1 = image[x, y]
				y_2 = image[x, y + 1]
			else if y == height - 1:
				y_1 = image[x, y - 1]
				y_2 = image[x, y]
			else:
				y_1 = image[x, y - 1]
				y_2 = image[x, y + 1]

			x_red = abs(x_1[0] - x_2[0])
			x_green = abs(x_1[1] - x_2[1])
			x_blue = abs(x_1[2] - x_2[2])

			y_red = abs(y_1[0] - y_2[0])
			y_green = abs(y_1[1] - y_2[1])
			y_blue = abs(y_1[2] - y_2[2])

			energy = x_red + x_green + x_blue + y_red + y_green + y_blue

			energy_table[x][y] = energy

	return energy_table

def findSeam(energy, direction):
	print 'Running: findSeam()'

	# code.

def removeSeam(image, seam, direction):
	print 'Running: removeSeam()'

	# code.

def showImage(image):
	print 'Running: showImage'
	image.show()

def main():
	print 'Running: Main()'

	image = carveSeams(sys.argv[1], sys.arvg[2], sys.argv[3])

if __name__ == '__main__':
	main()