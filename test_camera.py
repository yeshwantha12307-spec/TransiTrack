import cv2

# Use DirectShow for better stability (Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera open aagala ❌")
    exit()

# Set resolution (optional but useful)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

print("Camera working... Press ESC to exit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Frame read error ❌")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()