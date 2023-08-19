import cv2
import numpy as np
import json

def cek_frame_transparant(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    dimensi = (2400, 3600)
    image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
    center = []
    takes = -1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + (w // 2)
            if int(h * (1024 / 680) < w):
                h = int(w / (1024 / 680))
            if int(w / (1024 / 680) < h):
                w = int(h * (1024 / 680))
            x = center_x - w // 2
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            takes += 1
            # x -= 5
            # w += 10

            posisi.append([[x, y, w]])

    # for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
    #     cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2)    
    del posisi[0]
    posisi = list(reversed(posisi))
    for take in range(0, len(posisi) - 1, 2):
        x1, y1, w1 = posisi[take][0]
        x2, y2, w2 = posisi[take+1][0]
        if x1 + w1 > x2 :
            selisih_lebar = x1 + w1 - x2
            if selisih_lebar > 0:
                x1 -= selisih_lebar
            posisi[take][0][0] = x1

        # if y1 + (w1 / (1024 / 680)) > y3:
        #     selisih_tinggi = y1 + ( w1 / (1024 / 680)) - y3
        #     if selisih_tinggi > 0:
        #         y1 -= selisih_tinggi              
        #     posisi[take][0][1] = int(y1)

    data = {"take": takes,
            "position": posisi}
    print(data)
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)


image_path = "img/frame.png"
cek_frame_transparant(image_path)
