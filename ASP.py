import numpy as np
import cv2

from skimage.measure import compare_ssim
import argparse
import imutils




mouse_is_pressing = False
start_x, starty = -1, -1


def mouse_callback(event,x,y,flags,param):
	global start_x, start_y,mouse_is_pressing

	if event == cv2.EVENT_LBUTTONDOWN:
		mouse_is_pressing = True
		start_x, start_y = x, y


	elif event == cv2.EVENT_LBUTTONUP:
		mouse_is_pressing = False
		# 원본 영역에서 두 점 (start_y, start_x), (x,y)로 구성되는 사각영역을 잘라내어 변수 img_cat이 참조하도록 합니다.
		ROI = thresh[ start_y:y, start_x:x]
		unique, counts = np.unique(ROI, return_counts=True)

		print("validity of chosen area")
		if 0 not in unique:
			print(1)
		elif 255 not in unique:
			print(0)
		else:
			validity = counts[1] / (counts[0] + counts[1])
			print(validity)


		cv2.imshow("ROI", ROI)





# read unmarked image
src = cv2.imread("unmarked.jpg", cv2.IMREAD_COLOR)
height, width, channel = src.shape

# assign 4 test paper's edges' coordinates and warp it to the original image size
# srcPoint=np.array([[66, 36], [699, 31], [734, 977], [41, 973]], dtype=np.float32) # for imageSet 1
srcPoint=np.array([[72, 57], [692, 54], [758, 976], [39, 995]], dtype=np.float32) # for imageSet 2
dstPoint=np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
# dstUnmarked : warped testing paper with no mark as original size
dstUnmarked = cv2.warpPerspective(src, matrix, (width, height))


# read marked image
src = cv2.imread("marked.jpg", cv2.IMREAD_COLOR)
height, width, channel = src.shape

# assign 4 test paper's edges' coordinates and warp it to the original image size
# srcPoint=np.array([[210, 220], [641, 228], [682, 953], [50, 875]], dtype=np.float32) # for imageSet 1
srcPoint=np.array([[65, 39], [692, 48], [751, 987], [11, 996]], dtype=np.float32) # for imageSet 2
dstPoint=np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
# dstMarked : warped testing paper with markings as original size
dstMarked = cv2.warpPerspective(src, matrix, (width, height))


# convert the images to grayscale
grayA = cv2.cvtColor(dstUnmarked, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(dstMarked, cv2.COLOR_BGR2GRAY)



# blur

for i in range(10):
	grayA = cv2.GaussianBlur(grayA, (7, 7), 0)
	grayB = cv2.GaussianBlur(grayB, (7, 7), 0)


# minus = abs(grayB - grayA)



# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True)
# diff = (diff * 255).astype("uint8")  # multiplication number can be changed!
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))




# threshold the difference image, followed by finding contours to
# image binarization : classify every pixels as 0 or 1, not continuous one.
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
 	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

cv2.imwrite('thresh.jpg', thresh)

# Region of Interest (ROI)



"""
for i in thresh:
	print(i)
"""


"""
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


# loop over the contours
for c in cnts:
    # compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle dstUnmarked, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(dstMarked, (x, y), (x + w, y + h), (0, 0, 255), 2)
"""

# show the output images
cv2.imshow("UnmarkedOriginal", grayA)
cv2.imshow("MarkedOriginal", grayB)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)
cv2.setMouseCallback('Thresh', mouse_callback)
# cv2.imshow("Minus", minus)
cv2.waitKey(0)
cv2.destroyAllWindows()