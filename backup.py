import cv2
import numpy as np
import json
from flask import Flask, send_file, request

app = Flask(__name__)

@app.route('/setup_frame', methods=['POST'])
def SetupFrame():
    takes = request.form['take']
    takes = int(takes)
    # tipe_frame = request.form['tipe_frame']
    # tipe_foto = request.form['tipe_foto']
    imageSTR = request.files['frame'].read()
    image_byte = np.fromstring(imageSTR, np.uint8)
    image = cv2.imdecode(image_byte, cv2.IMREAD_UNCHANGED)

    dimensi = (3600, 2400)
    # if tipe_frame == 'potrait':
    #     dimensi = (2400, 3600)
    # if tipe_frame == 'landscape' or 'lanskap':
    #     dimensi = (3600, 2400)

    # if tipe_foto == 'potrait':
    #     dimensi_foto = 680 / 1024
    # if tipe_foto == 'landscape':
    #     dimensi_foto = 1024 / 680

    image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    # transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
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
            

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 6)

            x -= 5
            y -= 5
            w += 10
            posisi.append([[x, y, w]])

    # Mewarnai bagian yang transparant
    # for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
    #     cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2) 

    del posisi[0]
    posisi = list(reversed(posisi))

    # # biar tidak tabrakan

    # for take in range(0, len(posisi) - 1, 2):
    #     x1, y1, w1 = posisi[take][0]
    #     x2, y2, w2 = posisi[take+1][0]
    #     if x1 + w1 > x2 :
    #         selisih_lebar = x1 + w1 - x2
    #         if selisih_lebar > 0:
    #             x1 -= selisih_lebar
    #         posisi[take][0][0] = x1
    if takes == 3:
        posisi = [ [posisi[i][0], posisi[i + 1][0]] for i in range(0, len(posisi), 2) ]
    data = {"take": takes,
            "position": posisi}
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)

    # cv2.imshow("Detected Transparent Area", cv2.resize(image, tuple(map(lambda x: x // 5, dimensi)), interpolation = cv2.INTER_NEAREST))
    # cv2.imshow("Detected Transparent Area", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return send_file('format.json', as_attachment=True)


if __name__ == "__main__":
    app.run(debug = True)
    # app.run(debug = True, host='0.0.0.0', port = 3001)


