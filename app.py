import streamlit as st
import streamlit.components.v1 as components

st.title("Projectile Lab Assistant")

st.write("Mô phỏng ném xiên PhET")

components.iframe(
    "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_en.html",
    height=700
)