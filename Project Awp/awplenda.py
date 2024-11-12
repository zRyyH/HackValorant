import cv2
# import numpy as np
import pyautogui
import screen

screen.run()

while True:
    try:
        np_img = screen.screenshot()
        
        frame_bgr = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

        # Converta o frame para o espaço de cores HSV
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

        # Defina a faixa HSV para a cor verde (ajuste conforme necessário)
        min_hsv = (140, 90, 180)                                                  # Definindo filtro HSV minimo
        max_hsv = (170, 210, 255)

        # Crie uma máscara usando a faixa HSV especificada
        mask = cv2.inRange(frame_hsv, min_hsv, max_hsv)

        # Aplique a máscara ao frame original
        result = cv2.bitwise_and(frame_bgr, frame_bgr, mask=mask)
        
        # Adicione uma linha branca no meio da tela
        line_thickness = 1 # Ajuste conforme necessário
        cv2.line(result, (result.shape[1] // 2, 0), (result.shape[1] // 2, result.shape[0]), (255, 255, 255), thickness=line_thickness)

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
                    
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    except:
        pass