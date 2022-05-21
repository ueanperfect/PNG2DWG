import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist

class Dot_Reader():
    def __init__(self,img):
        self.img = img
        self.img_todo = self.img_process()
        self.dot_positions = self.get_dot_positions()

    def img_process(self):
        import cv2
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # 将图像转换成黑白图像
        img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (3, 3))  #高级处理
        img1 = img_close.copy()  # 复制一下经过处理的图，用来进行后续的处理
        return img1

    def get_dot_positions(self):
        import cv2
        import numpy as np
        corners = cv2.goodFeaturesToTrack(self.img_todo, 1000, 0.2, 20)  # 识别出像素突变的点，通过这个函数可以识别角点（图像大小改变参数应调整）
        corners = np.int0(corners)  # 对识别出来的点进行模式转换
        dot_positions = []
        for corner in corners:  # 建立一个遍历循环，将每个角点画出来
            x, y = corner.ravel()  # 对本点进行模式转换
            dot_positions.append((int(x), int(y)))  # 把本循环中识别出来的角点加到空列表 kps 中去
        return dot_positions