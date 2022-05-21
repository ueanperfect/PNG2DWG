import cv2
from utils.Dot_Reader import Dot_Reader
from utils.Judge import Judger

img = cv2.imread("../imgs/2.jpg") # input
dot_reader = Dot_Reader(img)
dot_positions = dot_reader.dot_positions
judger = Judger(img, dot_positions)

judger.draw_new_img('ok.png')