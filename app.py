
import streamlit as st
import cv2
import numpy as np
import tempfile
import pandas as pd
import plotly.express as px

st.title("Physics Video Tracking")

uploaded_file = st.file_uploader(
    "Upload video",
    type=["mp4", "mov", "avi","wmv"]
)

if uploaded_file is not None:

    # Lưu file tạm
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    points = []

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Giảm số frame để chạy nhẹ hơn
        if frame_count % 5 != 0:
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Nhận màu đỏ
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        mask = cv2.inRange(hsv, lower_red, upper_red)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:

            largest_contour = max(contours, key=cv2.contourArea)

            M = cv2.moments(largest_contour)

            if M["m00"] != 0:

                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                points.append({
                    "frame": frame_count,
                    "x": cx,
                    "y": -cy
                })

    cap.release()

    df = pd.DataFrame(points)

    st.write(df)

    if len(df) > 0:

        fig = px.scatter(
            df,
            x="x",
            y="y",
            title="Trajectory"
        )

        fig.update_traces(mode="lines+markers")

        st.plotly_chart(fig)

        st.success("Tracking complete!")

