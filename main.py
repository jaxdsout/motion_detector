import cv2
import os
import time
from send_email import send_email
import glob
from threading import Thread

webcam = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_dir():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = webcam.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(
        dilate_frame,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            3
        )

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/image-{count}.png", frame)
            count += 1
            all_captures = glob.glob("images/*.png")
            index = int(len(all_captures) / 2)
            target_capture = all_captures[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(target_capture, ))
        # daemon allows send_email, clean_dir to be run in the background
        email_thread.daemon = True
        email_thread.start()

        clean_thread = Thread(target=clean_dir)
        clean_thread.daemon = True

    cv2.imshow("recall capture", frame)

    # kill switch with q
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

webcam.release()
clean_thread.start()

