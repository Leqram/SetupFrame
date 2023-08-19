import cv2
import numpy as np
import json

def show_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 255

    posisi = []
    num_boxes = -1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            # h = int(w / (1024 / 680))
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            num_boxes += 1
            posisi.append([[x, y, w]])
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2)    

    del posisi[0]
    posisi = list(reversed(posisi))
    data = {"take": num_boxes,
            "position": posisi}
    print(data)
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)


image_path = "img/frame.png"
show_transparent_area(image_path)
