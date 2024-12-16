import pyautogui
import cv2
import numpy as np
import time
import mss
from PIL import Image
import matplotlib.pyplot as plt

import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.setGeometry(x, y, w, h - p)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        self.lines = []
        self.circles = []

        self.show()

    def add_line(self, x1, y1, x2, y2, update_overlay=False):
        self.lines.append((x1, y1, x2, y2))
        if update_overlay:
            self.update()

    def add_circle(self, x, y, update_overlay=False):
        self.circles.append((x, y))
        if update_overlay:
            self.update()

    def clear(self, update_overlay=False):
        self.lines = []
        self.circles = []
        if update_overlay:
            self.update()

    def paintEvent(self, event):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        painter = QPainter(self)
        painter.setPen(QColor(255, 100, 200))

        for (x1, y1, x2, y2) in self.lines:
            painter.drawLine(x1, y1, x2, y2)
        
        for (x, y) in self.circles:
            painter.drawEllipse(x - 15, y - 15, 30, 30)

        painter.end()


def display(img):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()


def capture():
    with mss.mss() as sct:
        if w == 0:
            return sct.grab(sct.monitors[0])
        monitor = {"left": x, "top": y, "width": w, "height": h}  # Adjust based on BlueStacks region
        return sct.grab(monitor)


def to_np(img):
    img = Image.frombytes('RGB', (img.width, img.height), img.rgb)
    return np.array(img)


def find_ball(frame, show=False, prev=None):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    result = []

    for contour in contours:
        area = cv2.contourArea(contour)
        (x, y), radius = cv2.minEnclosingCircle(contour)

        if 1000 < area < 2000:
            center = (int(x), int(y))
            radius = int(radius)
            result.append((area, center, radius))
            cv2.circle(frame, center, radius, (0, 255, 0), 2)


        if 5000 < area < 10000:
            center = (int(x), int(y))
            radius = int(radius)
            x, y, w, h = cv2.boundingRect(contour)
            result.append((area, center, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (240, 32, 160), 2)

    if len(result) == 1:
        print('edged, reusult:',result)
    if show:
        display(threshold)
    return result


def find_border(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_frame, 120, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 200000 < area < 1000000:
            x, y, w, h = cv2.boundingRect(contour)
            return x, y, w, h


def wait():
    print('wait1')

    # check for hitting paddle
    while True:
        img = capture()
        r = find_ball(to_np(img))

        if len(r) != 2:       
            if r[0][0] > 8000:
                break
            continue

        yy,r,p = r[1][1][1],r[1][2],r[0][2]

        if abs(yy-(y+h)) < 100+p+r:
            time.sleep(.1)
            break


    """
    print('wait2')

    # check for being near wall
    while True:
        img = capture()
        r = find_ball(to_np(img))

        if len(r) == 1:
            break

        xx,r = r[1][1][0],r[1][2]

        if abs(xx-(x)) < 50+r or abs(xx-(x+w)) < 50+r:
            continue
        break
        
    """
    
    print('wait done')


time.sleep(1)

x,y,w,h = 0,0,0,0

cv2.setUseOptimized(True)
og_img = capture()

x,y,w,h = find_border(to_np(og_img))
result = find_ball(to_np(og_img))
p = result[0][2]

print(x,y,w,h)
print(result)



app = QApplication(sys.argv)
window = TransparentOverlay()


wait()


while True:
    print('LOOPING...')


    window.clear()


    img1 = capture()
    time.sleep(.02)
    img2 = capture()
    r1 = find_ball(to_np(img1))
    r2 = find_ball(to_np(img2))

    print(r1,r2)


    if len(r1) != 2 or len(r2) != 2:
        if r1 == r2:
            print('whyyyyyyyyyyy')
            find_ball(prev,show=True)
            break
        continue

    prev = to_np(img1)

    if r1 == r2:
        find_ball(to_np(img2),show=True)
        print('smth dumb happened')
    

    x1,y1,x2,y2,p,r = r1[1][1][0],r1[1][1][1],r2[1][1][0],r2[1][1][1],r1[0][2],r1[1][2]
    a,b,c,d = r-5,r-5,w-r+5,h-p-r+5

    
    if abs(x1-(a)) < 50+r or abs(x1-(c)) < 50+r or abs(x2-(a)) < 50+r or abs(x2-(c)) < 50+r:
        print('wall')
        continue
    
    try:
        m = -(y2-y1)/(x2-x1)
    except Exception as e:
        print(e)
        continue

    print(x1,y1,x2,y2,p,r)
    print(m)

    window.add_circle(x1,y1)
    window.add_circle(x2,y2)



    while True:
        if m >= 0:
            y3 = y2 - m*(c-x2)
            if y3 >= b:
                x2 = c
                y2 = y3
            else:
                x2 = x2 - (b-y2)/m
                y2 = b
                break
        else:
            y3 = y2 - m*(a-x2)
            if y3 >= b:
                x2 = a
                y2 = y3
            else:
                x2 = x2 - (b-y2)/m
                y2 = b
                break
        m *= -1

        window.add_line(int(x1),int(y1),int(x2),int(y2))
        x1,y1 = x2,y2

    window.add_line(int(x1),int(y1),int(x2),int(y2))
    x1,y1 = x2,y2

    app.processEvents()
    app.processEvents()

    while True:
        if m >= 0:
            y3 = y2 + m*(c-x2)
            if y3 <= d:
                x2 = c
                y2 = y3
            else:
                x2 = x2 + (d-y2)/m
                y2 = d
                break
        else:
            y3 = y2 + m*(a-x2)
            if y3 <= d:
                x2 = a
                y2 = y3
            else:
                x2 = x2 + (d-y2)/m
                y2 = d
                break
        m *= -1

        window.add_line(int(x1),int(y1),int(x2),int(y2))
        x1,y1 = x2,y2

    window.add_line(int(x1),int(y1),int(x2),int(y2))

    app.processEvents()
    app.processEvents()

    pyautogui.click(x2+x,y2+y+int(p/2))

    
    print('clciked')
    

    wait()




