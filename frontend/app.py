import streamlit as st
import requests
import time
BACKEND_URL="http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Instagram Analyzer",
    page_icon="🤖",
    layout="wide",
)

def init_state():
    st.session_state.setdefault('summary',None)
    st.session_state.setdefault('recommendation',None)
    st.session_state.setdefault('image_url',None)
init_state()


st.title("AI Instagram Channel Analyzer")
st.markdown(
    "Enter an Instagram channel name to analyze its performance and get AI-powered recommendations for the next post."
)

channel_name=st.text_input(
    "Instagram Channel Name",
    placeholder="provide your channel name",
)

if st.button("Analyze Channel",type="primary"):
    for key in ['summary','recommendation','image_url']:
        st.session_state[key] = None

    if not channel_name:
        st.warning("Please enter a channel name")
    else:
        try:
            with st.spinner(f"Analyzing '{channel_name}'... please wait"):
                collect_res=requests.post(f"{BACKEND_URL}/collect-data",json={"channel_name":channel_name})
                collect_res.raise_for_status()
                summary_res=requests.get(f"{BACKEND_URL}/summarize")
                summary_res.raise_for_status()
                st.session_state.summary=summary_res.json()

                rec_res = requests.get(f"{BACKEND_URL}/recommend")
                rec_res.raise_for_status()
                st.session_state.recommendation=rec_res.json()

            st.success("Analysis complete")
        except requests.exceptions.HTTPError as e:
            detail=e.response.json().get("detail","Unknown error")
            st.error(f"API Error:{detail}")
        except requests.exceptions.RequestException:
            st.error(f"Connection Error:Could not connect to the backend at {BACKEND_URL}.")
        except Exception as e:
            st.error(f"An unexpected error occurred:{e}")

if st.session_state.summary and st.session_state.recommendation:
    col1,col2=st.columns(2)

    with col1:
        st.subheader("AI Performance Summary")
        st.write(st.session_state.summary.get("summary"))

    with col2:
        st.subheader("AI Post Recommendation")
        rec=st.session_state.recommendation
        with st.container(border=True):
            st.markdown(f"**Caption:** {rec.get('caption')}")
            st.markdown(f"**Hashtags:** {rec.get('hashtags')}")
            st.markdown(f"**Justification:** {rec.get('justification')}")

            if st.button("Generate Thumbnail"):
                with st.spinner("Generating AI thumbnail... This takes more time."):
                    try:
                        thumb_res=requests.post(f"{BACKEND_URL}/generate-thumbnail",json={"caption":rec.get('caption')})
                        thumb_res.raise_for_status()
                        st.session_state.image_url=thumb_res.json().get("image_url")
                    except requests.exceptions.HTTPError as e:
                        detail=e.response.json().get("detail" "Unknown error")
                        st.error(f"Thumbnail generation failed:{detail}")
                    except Exception as e:
                        st.error(f"An error occurred:{e}")

        if st.session_state.image_url:
            st.subheader("Generated Thumbnail")
            image_url_with_cache_buster =f"{BACKEND_URL}{st.session_state.image_url}?t={time.time()}"
            st.image(image_url_with_cache_buster, caption="AI-Generated Thumbnail", use_container_width=True)