import cv2
import numpy as np
import json

def cek_bertabrakan(box1, box2):
    x1, y1, w1 = box1
    x2, y2, w2 = box2
    return x1 + w1 > x2 and y1 + ( w1 / (1024 / 680)) > y2


def tampil_tempat_transparant(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # dimensi = (2400, 3600)
    # image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
    tinggi = []
    takes = -1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            if int(h * (1024 / 680) < w):
                h = int(w / (1024 / 680))
            if int(w / (1024 / 680) < h):
                w = int(h * (1024 / 680))
            

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            takes += 1
            x -= 5
            y -= 5
            w += 10
            posisi.append([[x, y, w]])
            tinggi.append([[h]])
            
    # for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
    #     cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2)    

    del posisi[0]
    posisi = list(reversed(posisi))
    for take in range(len(posisi) - 1):
        # print(posisi[take][0])
        # print(posisi[take+1][0])
        # print(take)
        current_box = posisi[take][0]
        next_box = posisi[take+1][0]
        if cek_bertabrakan(current_box, next_box):
            print("Data pada index {} dan index {} bertabrakan".format(take, take+1))
    data = {"take": takes,
            "position": posisi}
    print(data)
    print(tinggi)
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)


image_path = "img/frame.png"
tampil_tempat_transparant(image_path)
