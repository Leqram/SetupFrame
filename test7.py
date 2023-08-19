import cv2
import numpy as np

def show_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]
    transparent_pixels = np.where(alpha_channel == 0)


    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    posisi = []
    num_boxes = -1
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x, y), (0, 0, 255), 2)
        num_boxes += 1
        # print("X: ", x)
        # print("Y: ", y)
        # print("Width: ", w)
        # print("Height: ", h)
        # posisi.append([x, y, w, h])
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2)    


    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(posisi, "\n")


    # print("Jumlah kotak yang dimunculkan:", num_boxes)

image_path = "img/frame.png"
show_transparent_area(image_path)
