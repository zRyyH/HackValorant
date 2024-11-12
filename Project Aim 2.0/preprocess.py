import cv2
import numpy as np


class PreProcess():
    def __init__(self):
        self.split_screen = None
        self.hsv_min = None
        self.hsv_max = None
        self.size_x = None
        self.size_y = None
        self.width = None
        self.delta_median = None
    
    
    def set_values(self, delta_median=5, size_x=200, size_y=100, hsv_min=(136, 100, 150), hsv_max=(150, 255, 255), split_screen=5):
        self.size_x = size_x
        self.size_y = size_y
        self.hsv_min = hsv_min
        self.hsv_max = hsv_max
        self.split_screen = split_screen
        self.delta_median = delta_median
        
        self.width = int(self.size_x / self.split_screen)
        
        
        
    def paint_line(self, img, x_start, y_start, x_end, y_end):
        cv2.line(img, (int(x_start), int(y_start)), (int(x_end), int(y_end)), (255,0,0), 1)
        
        
    def paint_circle(self, img, x, y, size=3, rgb=(0,255,0), thickness=1):
        cv2.circle(img, (x, y), size, rgb, thickness)


    def hsv_filter(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        lower_green = np.array(self.hsv_min)
        upper_green = np.array(self.hsv_max)
        
        mask = cv2.inRange(hsv_img, lower_green, upper_green)
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        
        return masked_img


    def get_active_pixels(self, img):
        return np.column_stack(np.where(img > 0))


    def split_function(self, img):
        arr_cuts = []
        
        for num in range(0, self.split_screen):
            arr_cuts.append(img[:, self.width*num:self.width*(num+1)])
        return arr_cuts


    def paint_lines(self, img):
        for num in range(0, self.split_screen+1):
            self.paint_line(img, self.width*num, 0, self.width*num, self.size_x / 2)
                    
                    
    def find_heads(self, img):
        array_heads = []
        array_screens = self.split_function(img)
        
        for num, screen in enumerate(array_screens):
            position_head = self.get_active_pixels(screen)
            if position_head.any():
                head_x = position_head[0][1] + (self.width * num)
                head_y = position_head[0][0]
                array_heads.append([num, head_x, head_y])
                        
        return np.asarray(array_heads)


    def median_heads(self, array_heads, img):
        sum_median = 0
        if array_heads.any():
            for item in array_heads:
                sum_median += item[2]

            median = int(sum_median / array_heads.shape[0]) + self.delta_median
            return median


    def true_heads(self, array_heads, median):
        arr = []

        for head in array_heads:
            if head[2] <= median:
                arr.append(head)
        return arr


    def ordenar(self, arrays):
        return sorted(arrays, key=lambda x: abs(x[1] - self.size_x / 2))



    def new_head(self, true_heads):
        heads = self.ordenar(true_heads)
        
        if heads:
            return heads[0]
        else:
            return np.asarray([])
    
    
    
    def find_head_left(self, array_heads):
        pass
    
    
    
    def calc_delta(self, mask):
        start = int(int(self.size_x/2)-10)
        end = int(int(self.size_x/2)+10)
        
        cut_mask = mask[:, start:end]
        active_pixels = self.get_active_pixels(cut_mask)
        delta = int(len(active_pixels)/80)
        delta = 0 if delta <= 5 else 2
        
        return delta