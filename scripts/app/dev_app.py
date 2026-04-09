import streamlit as st
import time

import sys
sys.path.append('scripts')

from pipelines.load_dev_branch_analytics import get_image_video_max_confidence

st.set_page_config(page_title="Fine-tuned YOLOv11 Analytics", layout="wide")

st.title("🚀 Fine-tuned YOLOv11 Live Confidence Analytics (Dockerized)")

# 1. Add a Sidebar Control for the Stream
st.sidebar.header("Stream Controls")
auto_refresh = st.sidebar.toggle("Enable Live Stream", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (sec)", 1, 60, 5)

# 2. Wrapping analytics in a Fragment
# This allows the function to "automatically refresh" in real time
# based on the user's settings in the sidebar.
@st.experimental_fragment(run_every=refresh_interval if auto_refresh else None)
def display_live_analytics():
    st.write(f"⏱️ Last updated: {time.strftime('%H:%M:%S')}")
    
    image_df, video_df = get_image_video_max_confidence()

    col1, col2 = st.columns(2)

    with col1:
        if image_df is not None and not image_df.empty:
            st.subheader("🖼️ Top 5 Image Classes")
            st.dataframe(image_df, use_container_width=True)
            st.bar_chart(
                image_df.set_index('top5_classes')['top5_confidences'],
                color="#FF4B4B"
            )
        else:
            st.warning("No image data found.")

    with col2:
        if video_df is not None and not video_df.empty:
            st.subheader("📹 Top 5 Video Classes")
            st.dataframe(video_df, use_container_width=True)
            st.bar_chart(
                video_df.set_index('top5_classes')['top5_confidences'],
                color="#0068C9"
            )
        else:
            st.warning("No video data found.")

# 3. Call the fragment
display_live_analytics()