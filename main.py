import streamlit as st
from utils import generate_script
import os
open_api_key = st.secrets("OPEN_API_KEY")

st.title("🎬 숏츠 스크립트 생성기")

subject = st.text_input("**👅 숏츠의 주제를 입력해주세요!**")
video_length = st.number_input("⏰ **동영상 길이를 대략 알려주세요!** (단위: 분, 기본 1분)", min_value=0.1, step=0.1, value=1.0)
creativity = st.slider("🦄 **스크립트의 창의력을 설정해주세요.** (숫자가 작을수록 안정적이고, 숫자가 높을수록 창의적이에요!)", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
submit = st.button("스크립트 생성")


if submit and not subject:
    st.info("주제를 입력해주세요!")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("동영상 길이는 무조건 0.1보다 커야 합니다!")
    st.stop()
if submit:
    with st.spinner("현재 AI가 생각 중이에요! 조금만 기다려주세요..."):
        search_result,title, script = generate_script(subject, video_length, creativity, open_api_key)
    st.success("스크립트 생성을 완료했어요!")
    st.subheader("🔥 제목: ")
    st.write(title)
    st.subheader("📓 스크립트: ")
    st.write(script)
    with st.expander("위키 백과의 검색 결과 👀"):
        st.info(search_result)
