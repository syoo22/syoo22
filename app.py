import streamlit as st
import pandas as pd

# 📦 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# 🎨 바다 느낌 배경 스타일 추가
page_bg = """
<style>
body {
    background: linear-gradient(to bottom right, #a2d4f4, #d1f0fa);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 📌 제목 및 안내
st.markdown("<h1 style='text-align: center;'>🏖️ 해수욕장 방문자 예측 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</p>", unsafe_allow_html=True)

# 🏝️ 해수욕장 선택
st.markdown("🔴 <b>해수욕장을 선택하세요</b>", unsafe_allow_html=True)
beach_names = sorted(df["해수욕장명"].unique())
selected_beach = st.selectbox("", beach_names)

# 📅 날짜 선택
st.markdown("🟣 <b>방문 날짜를 선택하세요</b>", unsafe_allow_html=True)
available_dates = df[df["해수욕장명"] == selected_beach]["해수욕장일일일자"].sort_values().unique()
min_date = pd.to_datetime(available_dates.min())
max_date = pd.to_datetime(available_dates.max())
selected_date = st.date_input("", value=min_date, min_value=min_date, max_value=max_date)

# 🔍 버튼
if st.button("🔍 예측 결과 보기"):
    filtered = df[(df["해수욕장명"] == selected_beach) & (df["해수욕장일일일자"] == pd.to_datetime(selected_date))]
    
    # 운영기간 출력
    beach_dates = df[df["해수욕장명"] == selected_beach]["해수욕장일일일자"]
    open_day = beach_dates.min().strftime("%Y-%m-%d")
    close_day = beach_dates.max().strftime("%Y-%m-%d")
    
    st.markdown(
        f"""
        <div style="margin-bottom: 20px; color:#333;">
        📅 <b>{selected_beach}</b>의 예상 운영 기간은 <b>{open_day}</b>부터 <b>{close_day}</b>까지입니다.
        </div>
        """, unsafe_allow_html=True)

    if not filtered.empty:
        row = filtered.iloc[0]
        visitor = f"{int(row['예상 방문자수']):,}명"
        level = row['예상 혼잡도']

        # 🎨 혼잡도 색상
        color = {
            "여유": "green",
            "보통": "orange",
            "혼잡": "red"
        }.get(level, "black")

        st.markdown(
            f"""
            <div style="background-color: #e9f7fc; padding: 20px; border-radius: 10px;">
                <h4>📅 {selected_date} <b>{selected_beach}</b>의 예측 결과</h4>
                <p>👥 <b>예상 방문자수:</b> {visitor}</p>
                <p style="color:{color};">📌 <b>예상 혼잡도:</b> {level}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color: #ffe0e0; padding: 20px; border-radius: 10px;">
                <p>😥 <b>선택한 날짜의 예측 데이터가 없습니다.</b><br>다른 날짜를 선택해주세요.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
