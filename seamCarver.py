"""
seamCarver.py
Frederik Roenn Stensaeth
04.22.16

Python implementation of a content-aware image resizing algorithm.
"""

def carveSeams(image, seam_num, direction):
	print 'Running: carve()'
	print 'File: ' + filename
	print 'Number of seams: ' + seam_num
	print 'Direction: ' + direction

	# code.

def carveSeam(image, direction):
	print 'Running: carseSeam()'

	energy = computeEnergy(image)
	seam = findSeam(energy, direction)
	new_image = removeSeam(image, seam, direction)
	return new_image

def computeEnergy(image):
	print 'Running: computeEnergy()'

	# code.

def findSeam(energy, direction):
	print 'Running: findSeam()'

	# code.

def removeSeam(image, seam, direction):
	print 'Running: removeSeam()'

	# code.

def showImage(image):
	print 'Running: showImage'

	# code.

def main():
	print 'Running: Main()'

	# code.

if __name__ == '__main__':
	main()