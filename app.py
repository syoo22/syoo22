import streamlit as st
import pandas as pd

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# 🌊 배경 꾸미기 (바다 느낌 그라데이션)
page_bg = """
<style>
body {
    background: linear-gradient(to bottom, #b3ecff, #ffffff);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 🧭 제목
st.markdown("""
<h1 style='text-align: center; color: #0077b6;'>🌊 2025 해수욕장 방문자 예측 시스템</h1>
""", unsafe_allow_html=True)

st.markdown("")

# 🏖️ 해수욕장 선택
selected_beach = st.selectbox("🏖️ 해수욕장을 선택하세요", df["해수욕장이름"].unique())

# 📅 개장일/폐장일 구하기
beach_df = df[df["해수욕장이름"] == selected_beach]
open_date = beach_df["해수욕장일일일자"].min()
close_date = beach_df["해수욕장일일일자"].max()
open_str = open_date.strftime("%Y년 %m월 %d일")
close_str = close_date.strftime("%Y년 %m월 %d일")

# 🔔 예상 운영 기간 표시
st.markdown(f"""
<div style="margin-bottom: 1rem; font-size: 15px; color: #004080;">
🔔 <b>{selected_beach}</b>의 예상 운영 기간은 <b>{open_str}</b>부터 <b>{close_str}</b>까지입니다.
</div>
""", unsafe_allow_html=True)

# 📆 날짜 선택
selected_date = st.date_input("📅 방문할 날짜를 선택하세요 (6월 1일 ~ 8월 31일 사이)", 
                              min_value=open_date, max_value=close_date)

# 🔍 예측 결과 확인
result = beach_df[beach_df["해수욕장일일일자"] == pd.to_datetime(selected_date)]

if not result.empty:
    visitors = int(result["예상방문자수"].values[0])
    congestion = result["예상혼잡도"].values[0]

    # 혼잡도 색상
    if congestion == "여유":
        color = "#38b000"
    elif congestion == "보통":
        color = "#ffcc00"
    else:
        color = "#d00000"

    # 🎯 예측 결과 박스
    st.markdown(f"""
    <div style="padding: 1.2rem; border-radius: 10px; background-color: #f0f8ff; margin-top: 20px;">
        <h3 style="color: #0077b6;">📍 {selected_beach}의 {selected_date.strftime('%m월 %d일')} 예측</h3>
        <p style="font-size: 18px;">👥 예상 방문자 수: <b>{visitors:,}명</b></p>
        <p style="font-size: 18px;">🚦 예상 혼잡도: <b style="color: {color};">{congestion}</b></p>
    </div>
    """, unsafe_allow_html=True)

else:
    # 📛 데이터 없을 때 안내
    st.markdown("""
    <div style="padding: 1rem; background-color: #fff3cd; border-radius: 8px; color: #856404; font-size: 16px;">
    ⚠️ 선택한 날짜의 예측 데이터가 없습니다. 다른 날짜를 선택해주세요.
    </div>
    """, unsafe_allow_html=True)
