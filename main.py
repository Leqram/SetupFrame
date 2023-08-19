import cv2
import numpy as np
import json
from flask import Flask, send_file, request

app = Flask(__name__)

@app.route('/setup_frame', methods=['POST'])
def SetupFrame():
    imageSTR = request.files['frame'].read()
    image_byte = np.fromstring(imageSTR, np.uint8)
    image = cv2.imdecode(image_byte, cv2.IMREAD_UNCHANGED)

    dimensi = (2400, 3600)
    image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
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

            w += 10
            posisi.append([[x, y, w]])

    del posisi[0]
    posisi = list(reversed(posisi))
    # for take in range(0, len(posisi) - 1, 2):
    #     x1, y1, w1 = posisi[take][0]
    #     x2, y2, w2 = posisi[take+1][0]
    #     if x1 + w1 > x2 :
    #         selisih_lebar = x1 + w1 - x2
    #         if selisih_lebar > 0:
    #             x1 -= selisih_lebar
    #         posisi[take][0][0] = x1
    data = {"take": takes,
            "position": posisi}
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)

    return send_file('format.json', as_attachment=True)


if __name__ == "__main__":
    app.run(debug = True)


