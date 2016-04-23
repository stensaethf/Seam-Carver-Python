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

	image = Image.open(filename)
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
				x_1 = CODE.
				x_2 = CODE.
			else if x == width - 1:
				x_1 = CODE.
				x_2 = CODE.
			else:
				x_1 = CODE.
				x_2 = CODE.

			if y == 0:
				y_1 = CODE.
				y_2 = CODE.
			else if y == height - 1:
				y_1 = CODE.
				y_2 = CODE.
			else:
				y_1 = CODE.
				y_2 = CODE.

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