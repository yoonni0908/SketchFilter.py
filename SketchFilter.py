import numpy as np
import tkinter
from tkinter.filedialog import askopenfilename
import cv2

DELTA = 0
KSIZE = 5

tkinter.Tk().withdraw()
filename = askopenfilename(title='Select input a Image')
im = cv2.imread(filename, 0)
width = im.shape[1]
height = im.shape[0]

hueIm = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h1, s1, v = cv2.split(hueIm)

r = im[:, :, 2].copy()
g = im[:, :, 1].copy()
b = im[:, :, 0].copy()

me = np.finfo(float).eps

v1 = v.copy()

def sketchFilter(intensity):
    for x in range(KSIZE // 2, height - KSIZE // 2):  #KSIZE는 필터크기
        for y in range(KSIZE // 2, width - KSIZE // 2): # 각 화소를 접근 하는 다중 for문
            d = [] # 빈 리스트 생성
            for x1 in range(-KSIZE // 2 + 1, KSIZE // 2 + 1):
                for y1 in range(-KSIZE // 2 + 1, KSIZE // 2 + 1): #각 주위 화소값들을 비교하는 다중 for문
                    d.append(v[x + x1, y + y1]) #비교하여 가장 큰 값들을 d리스트에 넣어줌
            intensity[x, y] = intensity[x, y] / (max(d) + me + DELTA) * 255 #sketch filter 공식



sketchFilter(v1)

sketchFilter(r)
sketchFilter(g)
sketchFilter(b)


print("그림을 준비 중입니다")

result1 = cv2.merge([h1, s1, v1])
result2 = cv2.merge([r, g, b])
result1 = cv2.cvtColor(result1, cv2.COLOR_HSV2BGR)

(h, w) = result1.shape[:2]
max_size = 800

if h >= w:
    if h > max_size:
        ns = h / max_size
        nh = int(h / ns)
        nw = int(w / ns)
    else:
        nh = h
        nw = w

else:
    if w > max_size:
        ns = w / max_size
        nh = int(h / ns)
        nw = int(w / ns)
    else:
        nh = h
        nw = w

im = cv2.resize(im, (nw, nh))

result1 = cv2.resize(result1, (nw, nh))

result2 = cv2. resize(result2, (nw, nh))

cv2.imshow("Original", im)
cv2.imshow("HSV My Sketch", result1)
cv2.imwrite('result1.png', result1)
cv2.imshow("RGB My Sketch", result2)
cv2.imwrite('result2.png', result2)
cv2.waitKey()
cv2.destroyAllWindows()