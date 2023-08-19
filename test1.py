import cv2

def is_transparent_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    num_channels = image.shape[2]

    return num_channels == 4

image_path = 'img/frame.png'
is_transparent = is_transparent_image(image_path)

if is_transparent:
    print("Gambar memiliki latar belakang transparan.")
else:
    print("Gambar tidak memiliki latar belakang transparan.")
