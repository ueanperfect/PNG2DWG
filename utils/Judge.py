
class Judger():
    def __init__(self,img,dot_positions,line_thickness,overlap_threshold):
        self.img = img
        self.dot_positions = dot_positions
        self.line_thickness = line_thickness
        self.dot_groups = self.get_dot_group()
        self.dot_groups_dic = self.get_dot_group_dic()
        self.new_dot_groups_dic = self.get_new_doc_groups_dic()
        self.new_dot_groups = self.get_new_dot_groups()
        self.overlap_threshold = overlap_threshold
        self.original_mask = self.get_original_mask()
        self.result_list = self.get_judge_result_list()

    def get_dot_group_dic(self):
        import numpy as np
        new_dot_groups = self.dot_groups
        new_dot_groups_dic = {}
        for dot_group in new_dot_groups:
            if dot_group[0] in new_dot_groups_dic:
                new_dot_groups_dic[dot_group[0]].append(dot_group[1])
            else:
                new_dot_groups_dic[dot_group[0]] = []
                new_dot_groups_dic[dot_group[0]].append(dot_group[1])
        return new_dot_groups_dic

    def delete_from_single_dot(self,head_dot, tail_dots):
        from utils.tools import azimuthAngle
        from utils.tools import caculate_length
        from utils.tools import angle
        angle_list = []
        len_list = []
        for tail_dot in tail_dots:
            angle_list.append(angle([head_dot[0], head_dot[1], tail_dot[0], tail_dot[1]]))
            len_list.append(caculate_length(head_dot, tail_dot))
        angle_dic = {}
        for index, angle in enumerate(angle_list):
            if angle in angle_dic:
                if len_list[index] < len_list[angle_dic[angle]]:
                    angle_dic[angle] = index
                else:
                    continue
            else:
                angle_dic[angle] = index
        return angle_dic

    def get_new_doc_groups_dic(self):
        dic = self.dot_groups_dic
        for head_dot in dic:
            new_tail_list = []
            angle_dic = self.delete_from_single_dot(head_dot, dic[head_dot])
            for angle in angle_dic:
                new_tail_list.append(dic[head_dot][angle_dic[angle]])
            dic[head_dot] = new_tail_list
        return dic

    def get_new_dot_groups(self):
        dic = self.new_dot_groups_dic
        new_dot_group = []
        for head_dot in dic:
            tail_dots = dic[head_dot]
            for tail_dot in tail_dots:
                new_dot_group.append((head_dot,tail_dot))
        return new_dot_group

    def get_original_mask(self):
        mask = self.img[:,:,0]<255
        return mask.astype(int)

    def get_dot_group(self):
        import itertools
        dot_group = list(itertools.combinations(self.dot_positions, 2))
        return dot_group

    def get_singe_line_mask(self,dot1:tuple,dot2:tuple):
        import numpy as np
        import cv2
        mask_background = np.zeros(self.img.shape)
        single_line_mask_img = cv2.line(mask_background,dot1,dot2,color=(2,2,2),thickness=self.line_thickness)
        return single_line_mask_img[:,:,0]

    def judge_single_dot(self,dot1,dot2,line_mask):
        import numpy as np
        import math
        new_mask = line_mask+self.original_mask
        new_mask = new_mask==3
        new_mask = new_mask.astype(int)
        len_overlap = np.sum(new_mask)
        pingfang = (dot1[0] - dot2[0])** 2 + (dot1[1] - dot2[1])** 2
        len_line = math.sqrt(pingfang)
        if len_overlap > self.overlap_threshold*len_line:
            return 1
        else:
            return 0

    def get_judge_result_list(self):
        judge_result_list = []
        for index,dot_group in enumerate(self.new_dot_groups):
            print('processing line:'+str(index)+'/'+str(len(self.new_dot_groups)),end='\r')
            dot1 = dot_group[0]
            dot2 = dot_group[1]
            line_mask = self.get_singe_line_mask(dot1,dot2)
            judge_single_result = self.judge_single_dot(dot1,dot2,line_mask)
            judge_result_list.append(judge_single_result)
        return judge_result_list

    def draw_new_img(self,path):
        import numpy as np
        import cv2
        img_background = np.ones(self.img.shape)*255
        for index,dot_group in enumerate(self.new_dot_groups):
            if self.result_list[index]==1:
                dot1 = dot_group[0]
                dot2 = dot_group[1]
                img_background = cv2.line(img_background, dot1, dot2, color=(0, 0, 0), thickness=1)
            else:
                continue
        cv2.imwrite(path,img_background)