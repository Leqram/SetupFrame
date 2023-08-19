import cv2
import numpy as np

def show_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]

    transparent_pixels = np.where(alpha_channel == 0)
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        width = 3  
        height = int(width * (1024 / 680)) 
        top_left = (x - width // 3, y - height // 3)
        bottom_right = (x + width // 3, y + height // 3)
        cv2.rectangle(image, top_left, bottom_right, (102, 255, 255), 2)
        
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_path = "img/frame.png"
show_transparent_area(image_path)
