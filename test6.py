import cv2
import numpy as np
import json

def show_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    positions = []
    alpha_channel = image[:, :, 3]

    transparent_pixels = np.where(alpha_channel == 0)
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        # num_pixels = len(transparent_pixels[0])
        # width = int(0.1 * num_pixels)
        # height = int(width / (1024 / 680))
        # left = x - width // 2
        # top = y - height // 2
        # position = [left, top, width]
        # positions.append(position)
        cv2.rectangle(image, (x-2, y-2), (x+2, y+2), (102, 255, 255), 2)
        left_top = (x-2, y-2)
        right_bottom = (x+2, y+2)

        # Hitung dan simpan nilai (x-2) dan (y-2) dalam variabel positions
        positions.append((x-2, y-2))

    total_x_minus_2 = sum(x for x, y in positions)
    total_y_minus_2 = sum(y for x, y in positions)
    print(total_x_minus_2)

    # result = {"position": positions}
    # for pos in result["position"]:
    #     pos[0] = int(pos[0])
    #     pos[1] = int(pos[1])
    #     pos[2] = int(pos[2])
    # format_json  = json.dumps(result, indent=2)

    # print(format_json)
    cv2.imshow("Detected Transparent Area", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_path = "img/frame.png"
show_transparent_area(image_path)
