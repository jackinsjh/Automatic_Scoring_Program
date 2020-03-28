import numpy as np
import cv2

from skimage.measure import compare_ssim
import argparse
import imutils




mouse_is_pressing = False
clickX, clickY = -1, -1
clickCoordinates = []




def mouseCallbackSpot(event,x,y,flags,param):
	global clickX, clickY, clickCount, clickCoordinates

	if event == cv2.EVENT_LBUTTONDOWN:
		mouse_is_pressing = True
		clickX, clickY = x, y
		clickCoordinates.append([clickX, clickY])





def mouseCallbackROI(event,x,y,flags,param):
	global clickX, clickY,mouse_is_pressing

	if event == cv2.EVENT_LBUTTONDOWN:
		mouse_is_pressing = True
		clickX, clickY = x, y


	elif event == cv2.EVENT_LBUTTONUP:
		mouse_is_pressing = False
		# 원본 영역에서 두 점 (clickY, clickX), (x,y)로 구성되는 사각영역을 잘라내어 변수 img_cat이 참조하도록 합니다.
		ROI = thresh[ clickY:y, clickX:x]
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




curTestCase = input("Enter testcase number")




# read unmarked image
src = cv2.imread("unmarked" + curTestCase + ".jpg", cv2.IMREAD_COLOR)
height = src.shape[0]
width = src.shape[1]

if height >= width:
	resizeScale = 1000 / height
else:
	resizeScale = 1000 / width
src = cv2.resize(src, (int(width * resizeScale), int(height * resizeScale)), interpolation=cv2.INTER_AREA)

print("Changed dimensions : ", src.shape)



height, width, channel = src.shape

cv2.imshow("UnmarkedOriginal", src)
cv2.setMouseCallback('UnmarkedOriginal', mouseCallbackSpot)


print("Click 4 spot of the image, starting from left-upper side, clockwise")
print("After that, press any key")
cv2.waitKey(0)
cv2.destroyAllWindows()
print(clickCoordinates)


srcPoint=np.array(clickCoordinates, dtype=np.float32)
clickCoordinates = []

# assign 4 test paper's edges' coordinates and warp it to the original image size
# srcPoint=np.array([[66, 36], [699, 31], [734, 977], [41, 973]], dtype=np.float32) # for imageSet 1
# srcPoint=np.array([[72, 57], [692, 54], [758, 976], [39, 995]], dtype=np.float32) # for imageSet 2
dstPoint=np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint)
# dstUnmarked : warped testing paper with no mark as original size
dstUnmarked = cv2.warpPerspective(src, matrix, (width, height))


# read marked image
src = cv2.imread("marked" + curTestCase + ".jpg", cv2.IMREAD_COLOR)
height = src.shape[0]
width = src.shape[1]

if height >= width:
	resizeScale = 1000 / height
else:
	resizeScale = 1000 / width
src = cv2.resize(src, (int(width * resizeScale), int(height * resizeScale)), interpolation=cv2.INTER_AREA)

print("Changed dimensions : ", src.shape)




height, width, channel = src.shape


cv2.imshow("markedOriginal", src)
cv2.setMouseCallback('markedOriginal', mouseCallbackSpot)


print("Click 4 spot of the image, starting from left-upper side, clockwise")
print("After that, press any key")
cv2.waitKey(0)
cv2.destroyAllWindows()
print(clickCoordinates)


srcPoint=np.array(clickCoordinates, dtype=np.float32)
clickCoordinates = []



# assign 4 test paper's edges' coordinates and warp it to the original image size
# srcPoint=np.array([[210, 220], [641, 228], [682, 953], [50, 875]], dtype=np.float32) # for imageSet 1
# srcPoint=np.array([[65, 39], [692, 48], [751, 987], [11, 996]], dtype=np.float32) # for imageSet 2
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

# cv2.imwrite('thresh.jpg', thresh)

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
cv2.setMouseCallback('Thresh', mouseCallbackROI)

print("drag mouse from left-top to right-bottom to capture area and check validity of that area")

cv2.waitKey(0)
cv2.destroyAllWindows()