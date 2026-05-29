import streamlit as st
import cv2
import numpy as np
import tempfile
import pandas as pd
import plotly.express as px

st.title("Water Jet Analysis")

video = st.file_uploader(
    "Upload video",
    type=["mp4", "mov", "avi"]
)

if video is not None:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video.read())

    cap = cv2.VideoCapture(tfile.name)

    ret, frame = cap.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # làm mượt
        gray = cv2.GaussianBlur(gray,(5,5),0)

        # tìm vùng sáng (nước)
        _, thresh = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY
        )

        ys, xs = np.where(thresh > 0)

        df = pd.DataFrame({
            "x": xs,
            "y": -ys
        })

        st.image(
            thresh,
            caption="Detected water region"
        )

        fig = px.scatter(
            df,
            x="x",
            y="y",
            title="Water Jet Shape"
        )

        st.plotly_chart(fig)

    cap.release()
