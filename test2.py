import cv2
import numpy as np

def find_transparent_pixels(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]

    transparent_pixels = np.argwhere(alpha_channel == 0)

    return transparent_pixels

image_path = 'img/frame.png'
transparent_pixels = find_transparent_pixels(image_path)
take = len(transparent_pixels) / 8

print("Jumlah piksel transparan:", len(transparent_pixels))
print(take)
print("Posisi piksel transparan:")
# for pixel in transparent_pixels:
#     print("X:", pixel[1], "Y:", pixel[0])
