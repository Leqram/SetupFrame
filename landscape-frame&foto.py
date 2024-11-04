import cv2
import numpy as np
import json

def cek_frame_transparant(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    dimensi = (900, 600)
    
    image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
    center = []
    takes = 3

    takes = int(takes)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            tengah_frame = (x + (w // 2)) + (y + (h // 2))
            if int(h * (1024 / 680) < w):
                h = int(w / (1024 / 680))
            if int(w / (1024 / 680) < h):
                w = int(h * (1024 / 680))

                tengah_foto = (x + (w // 2)) + (y + (h // 2))
                selisih_tengah = tengah_foto - tengah_frame
                x = x - selisih_tengah
            

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            x -= 5
            y += 2
            w += 10
            posisi.append([[x, y, w]])

    del posisi[0]
    posisi = list(reversed(posisi))
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2)    

    data = {"take": takes,
            "position": posisi}

    print(f"posisi awal: {posisi}")

    posisi = [ [posisi[i][0], posisi[i + 1][0]] for i in range(0, len(posisi), 2) ]

    print(f"posisi baru: {posisi}")
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)


image_path = "img/frame-landscape.png"
cek_frame_transparant(image_path)
