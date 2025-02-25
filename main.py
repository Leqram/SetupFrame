import cv2
import numpy as np
import json
from flask import Flask, send_file, request

app = Flask(__name__)

@app.route('/setup_frame', methods=['POST'])
def SetupFrame():
    takes = request.form['take']
    type_frame = request.form['tipe_frame']
    type_foto = request.form['tipe_foto']
    takes = int(takes)
    imageSTR = request.files['frame'].read()
    image_byte = np.fromstring(imageSTR, np.uint8)
    image = cv2.imdecode(image_byte, cv2.IMREAD_UNCHANGED)

    if type_frame == 'landscape':
        dimensi = (3600, 2400)
    if type_frame == 'potrait':
        dimensi = (2400, 3600)

    image = cv2.resize(image, dimensi, interpolation = cv2.INTER_NEAREST)

    alpha_channel = image[:, :, 3]
    
    transparent_pixels = np.where(alpha_channel == 0)

    contours, _ = cv2.findContours(alpha_channel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 8640

    posisi = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            tengah_frame = (x + (w // 2)) + (y + (h // 2))
            
            if type_foto == 'square':
                if int(h < w):
                    h = w
                if int(w < h):
                    w = h
                    
            if type_foto == 'landscape':
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

    del posisi[0]
    posisi = list(reversed(posisi))
 
    if takes == 3:
        posisi = [ [posisi[i][0], posisi[i + 1][0]] for i in range(0, len(posisi), 2) ]
    data = {"take": takes,
            "position": posisi}
    with open("format.json", "w") as json_file:
        json.dump(data, json_file, indent=3)


    # for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
    #     cv2.rectangle(image, (x, y), (x, y), (102, 255, 255), 2) 
    new_dimensi = (int(dimensi[0] / 4), int(dimensi[1] / 4))
    preview = cv2.resize(image, new_dimensi)

    cv2.imshow("Detected Transparent Area", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return send_file('format.json', as_attachment=True)


if __name__ == "__main__":
    app.run(debug = True)
    # app.run(debug = True, host='0.0.0.0', port = 3001)


