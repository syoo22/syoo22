import streamlit as st
import pandas as pd

# ✅ 배경 꾸미기 (바다 느낌 그라데이션)
page_bg = """
<style>
body {
    background: linear-gradient(to bottom, #a2d4f4, #d5f0ff);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ✅ 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 제목 및 설명
st.markdown("<h1 style='text-align: center;'>🏖️ 해수욕장 방문자 예측 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</p>", unsafe_allow_html=True)

# ✅ 입력값 선택
st.markdown("### 🔴 해수욕장을 선택하세요")
beach_names = sorted(df["해수욕장명"].unique())
selected_beach = st.selectbox("", beach_names)

st.markdown("### 🟣 방문 날짜를 선택하세요")
selected_date = st.date_input("", pd.to_datetime("2025-06-01"))

# ✅ 운영기간 추출 및 안내 문구 표시
beach_data = df[df["해수욕장명"] == selected_beach]
start_date = beach_data["해수욕장일일일자"].min()
end_date = beach_data["해수욕장일일일자"].max()

st.markdown(
    f"<p style='margin-top: 10px;'>📅 <b>{selected_beach}</b>의 예상 운영 기간은 <b>{start_date.strftime('%Y-%m-%d')}</b>부터 <b>{end_date.strftime('%Y-%m-%d')}</b>까지입니다.</p>",
    unsafe_allow_html=True,
)

# ✅ 버튼
if st.button("🔍 예측 결과 보기"):

    filtered = beach_data[beach_data["해수욕장일일일자"] == pd.to_datetime(selected_date)]

    if not filtered.empty:
        row = filtered.iloc[0]
        visitors = int(row["예상 방문자수"])
        congestion = row["예상 혼잡도"]

        st.markdown(
            f"""
            <div style="background-color:#eaf8ff;padding:20px;border-radius:10px;margin-top:20px;">
                <h4>📅 {selected_date.strftime('%Y-%m-%d')} <b>{selected_beach}</b>의 예측 결과</h4>
                <p>👥 <b>예상 방문자수:</b> {visitors:,}명</p>
                <p>📌 <b>예상 혼잡도:</b> <span style="color:{'green' if congestion=='여유' else 'orange' if congestion=='보통' else 'red'}">{congestion}</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background-color:#fff0f0;padding:15px;border-radius:10px;margin-top:20px;">
                <b>선택한 날짜의 예측 데이터가 없습니다.</b><br>다른 날짜를 선택해주세요.
            </div>
            """,
            unsafe_allow_html=True,
        )
