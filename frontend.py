import cv2
import streamlit as st
from datetime import datetime

st.title("motion detector")
start = st.button("activate camera")

if start:
    st_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now = datetime.now()

        cv2.putText(
            img=frame,
            text=now.strftime("%A %d/%m/%y"),
            org=(30, 50),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=2,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.FILLED
        )

        cv2.putText(
            img=frame,
            text=now.strftime("%H:%M:%S"),
            org=(30, 110),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=2,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.FILLED
        )

        st_image.image(frame)