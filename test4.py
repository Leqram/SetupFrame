import cv2
import numpy as np

def detect_transparent_area(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]

    transparent_pixels = np.where(alpha_channel == 0)

    print("Transparent Pixels Coordinates:")
    for x, y in zip(transparent_pixels[1], transparent_pixels[0]):
        print(f"({x}, {y})")

image_path = "img/frame.png"
detect_transparent_area(image_path)
