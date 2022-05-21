import cv2
from utils.Dot_Reader import Dot_Reader
from utils.Judge import Judger

img = cv2.imread("imgs/1.jpg") # input
img = cv2.resize(img,None,fx=0.5,fy=0.5) #调尺寸
dot_reader = Dot_Reader(img)
dot_positions = dot_reader.dot_positions
judger = Judger(img, dot_positions,line_thickness=2,overlap_threshold=1.3)

judger.draw_new_img('ok1.png')











