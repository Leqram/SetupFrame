import cv2
import numpy as np

def show_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]

    transparent_pixels = np.where(alpha_channel == 0)
    non_transparent = np.where(alpha_channel != 0)
    boxes = []
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        cv2.rectangle(image, (x, y), (x+2, y+2), (102, 255, 255), 2)
        boxes.append([(x-2, y-2), (x+2, y+2)])
    
    print(len(boxes))
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_path = "img/frame.png"
show_transparent_area(image_path)
