import preprocess
import pyautogui
import screenrec
import cv2


PRE = preprocess.PreProcess()
PRE.set_values(delta_median=3, split_screen=5, size_x=100, size_y=50)


def awp(img):
    try:
        # Converta o frame para o espaço de cores BGR
        frame_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Converta o frame para o espaço de cores HSV
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

        # Crie uma máscara usando a faixa HSV especificada
        mask = cv2.inRange(frame_hsv, PRE.hsv_min, PRE.hsv_max)

        # Aplique a máscara ao frame original
        result = cv2.bitwise_and(frame_bgr, frame_bgr, mask=mask)
        
        # Procure por um pixel ativo apenas na metade esquerda da tela
        half_width = result.shape[1] // 2
        half_height = result.shape[0] // 2
        
        top_left_half_mask = mask[:half_height, :half_width]
        top_right_half_mask = mask[:half_height, half_width:]
        down_left_half_mask = mask[half_height:, :half_width]
        down_right_half_mask = mask[half_height:, half_width:]
        
        top_left_half_mask = cv2.findNonZero(top_left_half_mask)
        top_right_half_mask = cv2.findNonZero(top_right_half_mask)
        down_left_half_mask = cv2.findNonZero(down_left_half_mask)
        down_right_half_mask = cv2.findNonZero(down_right_half_mask)
        
        center_pixel_bgr = frame_bgr[frame_hsv.shape[0] // 2, frame_hsv.shape[1] // 2]
        
        if center_pixel_bgr[0] == 255 and center_pixel_bgr[1] == 0 and center_pixel_bgr[2] == 0:
            if top_left_half_mask is not None and top_right_half_mask is not None:
                if down_left_half_mask is not None and down_right_half_mask is not None:
                    pyautogui.click()
                    
    except Exception as error:
        print('Error:', error)
        
                
                
def DetectPlayer():
    try:
        img = screenrec.screenshot()
        mask = PRE.hsv_filter(img)
        
        awp(img)
        
        array_heads = PRE.find_heads(mask)
        median = PRE.median_heads(array_heads, mask)
        true_heads = PRE.true_heads(array_heads, median)
        head = PRE.new_head(true_heads)
        
        # if head.any():
        #     PRE.paint_line(img=mask, x_start=0, y_start=median, x_end=PRE.size_x, y_end=median)
        #     PRE.paint_lines(mask)
        #     PRE.paint_circle(img=mask, x=head[1], y=head[2])
        #     PRE.paint_circle(img=mask, x=array_heads[0][1], y=array_heads[0][2], rgb=(0,0,255), size=5)
        
        if head.any():
            x = int(int(head[1] - PRE.size_x / 2) / 3)
            y = int(int(head[2] - PRE.size_y / 2) / 3)
            
            y += PRE.calc_delta(mask=mask)
            
            return x, y
        return 0,0
    
    
    except Exception as error:
        print('| Error DetectPlayer', error)
        return 0, 0