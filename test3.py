import cv2
import numpy as np

def detect_transparent_regions(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    alpha_channel = image[:, :, 3]

    _, labels, stats, _ = cv2.connectedComponentsWithStats(alpha_channel, connectivity=8)

    detected_regions = []

    for label, stat in enumerate(stats[1:], start=1):
        area = stat[4] 
        if area > 0: 
            region_mask = (labels == label).astype(np.uint8) * 255
            
            contours, _ = cv2.findContours(region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                
                if 0.5 <= aspect_ratio <= 2.0:
                    detected_regions.append((x, y, w, h))
    
    return detected_regions

# Contoh penggunaan
image_path = 'img/frame.png'
detected_regions = detect_transparent_regions(image_path)

print("Jumlah bagian transparan yang terdeteksi:", len(detected_regions))
print("Informasi setiap bagian:")
for i, region in enumerate(detected_regions, start=1):
    print(f"Bagian {i}: Posisi: ({region[0]}, {region[1]}), Ukuran: ({region[2]}, {region[3]})")
