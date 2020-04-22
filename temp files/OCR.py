"""
import tempfile

import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def process_image_for_ocr(file_path):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image
"""

"""
import cv2


def nothing():
    pass


x = 0.2
y = 0.2

img_gray = cv2.imread('test5.jpg', cv2.IMREAD_GRAYSCALE)
img_gray = cv2.resize(img_gray, dsize=(0, 0), fx=x, fy=y, interpolation=cv2.INTER_LINEAR + cv2.INTER_CUBIC)


cv2.namedWindow("Canny Edge")
cv2.createTrackbar('low threshold', 'Canny Edge', 0, 1000, nothing)
cv2.createTrackbar('high threshold', 'Canny Edge', 0, 1000, nothing)

cv2.setTrackbarPos('low threshold', 'Canny Edge', 50)
cv2.setTrackbarPos('high threshold', 'Canny Edge', 150)

cv2.imshow("Original", img_gray)

while True:

    low = cv2.getTrackbarPos('low threshold', 'Canny Edge')
    high = cv2.getTrackbarPos('high threshold', 'Canny Edge')

    img_canny = cv2.Canny(img_gray, low, high)
    cv2.imshow("Canny Edge", img_canny)

    if cv2.waitKey(1)&0xFF == 27:
        break


cv2.destroyAllWindows()
"""


import re
import cv2
import numpy as np
import pytesseract

x = 0.5
y = 0.5
img = cv2.imread('ocrTest2.jpg')
img = cv2.resize(img, dsize=(0, 0), fx=x, fy=y, interpolation=cv2.INTER_LINEAR + cv2.INTER_CUBIC)   # 높이와 너비도 정확도에 영향, 작을수록 정확해
copy_img = img.copy()
#cv2.imshow("test", img)
print('x:',x,'y:',y)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)

#blur = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#blur = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
blur = cv2.GaussianBlur(gray, (3,3),0)
#cv2.imshow("blur", blur)

canny = cv2.Canny(blur,100,200)
cv2.imshow("canny", canny)


contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


box1 = []
for i in range(len(contours)):
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area = w*h #area size
    aspect_ratio = float(w)/h #ratio = width / height

    if aspect_ratio >= 0.2 and aspect_ratio <= 1.0 and rect_area >= 100 and rect_area <= 700:
        rectangle = cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0),1)
        box1.append(cv2.boundingRect(cnt))

        cv2.imshow("rectangle", rectangle)


#Bubble Sort on Python
for i in range(len(box1)):
    for j in range(len(box1)-(i+1)):
        if box1[j][0] > box1[j+1][0]:
            temp = box1[j]
            box1[j] = box1[j+1]
            box1[j+1] = temp

f_count = 0
for m in range(len(box1)):
    count = 0
    for n in range(m+1, (len(box1)-1)):
        delta_x = abs(box1[n+1][0]-box1[m][0])
        if delta_x > 150:
            break
        delta_y = abs(box1[n+1][1] - box1[m][1])
        if delta_x == 0:
            delta_x = 1
        if delta_y == 0:
            delta_y = 1
        gradient = float(delta_y) / float(delta_x)
        if gradient < 0.25:
            count = count + 1

    #measure number plate size
    if count > f_count:
        select = m
        f_count = count;
        plate_width = delta_x

number_plate = copy_img[box1[select][1]-10:box1[select][1] + 20, box1[select][0]-10:140+box1[select][0]]

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#gray = cv2.GaussianBlur(gray, 10)


resize_plate = cv2.resize(number_plate, dsize=(0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR + cv2.INTER_CUBIC)
plate_gray = cv2.cvtColor(resize_plate, cv2.COLOR_BGR2GRAY)
th_plate = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

kernel = np.ones((3,3),np.uint8)
er_plate = cv2.erode(th_plate, kernel, iterations=1)
cv2.imshow("er_plate",er_plate)

text = pytesseract.image_to_string(er_plate,lang='euc') #영어면 'euc'

print(text)

"""
import PIL
import re
import cv2
import numpy as np
import pytesseract

img = cv2.imread('test2.jpg')
img = cv2.resize(img, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
cv2.imshow("test", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#gray = PIL.Image.fromarray(gray)
cv2.imshow("gray", gray)

# Denoising
#denoised = cv2.fastNlMeansDenoising(gray, h=10, searchWindowSize=21, templateWindowSize=7)
#cv2.imshow("denoised", denoised)



result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]




#cv2.waitKey(0)
#cv2.destroyAllWindows()

#gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#gray = cv2.medianBlur(gray, 10)

text = pytesseract.image_to_string(result,lang='kor') #영어면 'euc'

print(text)
"""