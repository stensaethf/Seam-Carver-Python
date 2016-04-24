"""
seamCarver.py
Frederik Roenn Stensaeth
04.22.16

Python program to perform content-aware image resizing using seam carving.
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

def findSeam(energy_table, direction):
	print 'Running: findSeam()'

	width = len(energy_table)
	height = len(energy_table[0])
	seam_dynamic = [[None for y in range(height)] for x in range(width)]
	backtracker = [[None for y in range(height)] for x in range(width)]

	if direction == 'V':
		for y in range(height):
			for x in range(width):
				if y == 0:
					seam_dynamic[x][y] = energy_table[x][y]
					backtracker[x][y] = -1
				else:
					if x == 0:
						minimum = min(seam_dynamic[x][y - 1], seam_dynamic[x + 1][y - 1])
						if minimum = seam_dynamic[x][y - 1]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 2
					else if x == width - 1:
						minimum = min(seam_dynamic[x][y - 1], seam_dynamic[x - 1][y - 1])
						if minimum = seam_dynamic[x][y - 1]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 0
					else:
						minimum = min(seam_dynamic[x - 1][y - 1], seam_dynamic[x][y - 1], seam_dynamic[x + 1][y - 1])
						if minimum = seam_dynamic[x - 1][y - 1]:
							backtracker[x][y] = 0
						elif minimum = seam_dynamic[x][y - 1]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 2

					seam_dynamic[x][y] = energy_table[x][y] = minimum
		
		min_num = seam_dynamic[0][height - 1]
		min_index = 0
		for x in range(width):
			if min_num > seam_dynamic[x][height - 1]:
				min_index = x
				min_num = seam_dynamic[x][height - 1]

		y_index = height - 1
		x_index = min_index
		seam = [[None for y in range(2)] for x in range(height)]
		seam[y_index][0] = x_index
		seam[y_index][1] = y_index
		while y_index > 0:
			backtrack = backtracker[x_index][y_index]
			if backtrack == 0:
				x_index -= 1
			else if backtrack != 1:
				x_index += 1
			y_index -= 1

			seam[y_index][0] = x_index
			seam[y_index][1] = y_index
	elif direction == 'H':
		for x in range(width):
			for y in range(height):
				if x == 0:
					seam_dynamic[x][y] = energy_table[x][y]
					backtracker[x][y] = -1
				else:
					if y == 0:
						minimum = min(seam_dynamic[x - 1][y], seam_dynamic[x - 1][y + 1])
						if minimum = seam_dynamic[x - 1][y]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 2
					elif y == height - 1:
						minimum = min(seam_dynamic[x - 1][y], seam_dynamic[x - 1][y - 1])
						if minimum = seam_dynamic[x - 1][y]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 0
					else:
						minimum = min(seam_dynamic[x - 1][y - 1], seam_dynamic[x - 1][y], seam_dynamic[x - 1][y + 1])
						if minimum = seam_dynamic[x - 1][y - 1]:
							backtracker[x][y] = 0
						elif minimum == seam_dynamic[x - 1][y]:
							backtracker[x][y] = 1
						else:
							backtracker[x][y] = 2

					seam_dynamic[x][y] = energy_table[x][y] + minimum
		
		# code
	else:
		print 'Invalid direction: ' + direction
		sys.exit(1)

	return seam

def removeSeam(image, seam, direction):
	print 'Running: removeSeam()'

	# code.

def showImage(image):
	print 'Running: showImage'
	image.show()

def main():
	print 'Running: Main()'

	image = carveSeams(sys.argv[1], sys.arvg[2], sys.argv[3])
	showImage(image)

if __name__ == '__main__':
	main()