import cv2
import pyzbar.pyzbar as pyzbar


def scan_qr() -> str:
    """Scan a QR code using the first webcam and return the decoded text."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise RuntimeError("Failed to access webcam")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                continue
            decoded = pyzbar.decode(frame)
            if decoded:
                cam.release()
                cv2.destroyAllWindows()
                return decoded[0].data.decode("utf-8")
    finally:
        cam.release()
        cv2.destroyAllWindows()
