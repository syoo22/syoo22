import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ✅ 페이지 기본 설정
st.set_page_config(page_title="해수욕장 방문자 예측 시스템", layout="wide")

# ✅ 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #a2d4f7, #e0f7fa);
        font-family: 'Helvetica', sans-serif;
        padding: 0 5vw;
    }

    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #003366;
        margin-bottom: 0.2em;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #004080;
        margin-bottom: 1.5em;
    }

    .result-card {
        background-color: #ffffffdd;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 타이틀
st.markdown("<div class='title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>2025년 전국 해수욕장 예상 방문자수 및 혼잡도 시각화</div>", unsafe_allow_html=True)

# ✅ 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    return df

df = load_data()

# ✅ 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# ✅ 혼잡도 컬러 설정 함수
def get_color(congestion):
    if congestion == "높음":
        return "red"
    elif congestion == "중간":
        return "orange"
    else:
        return "green"

# ✅ 마커 추가
for _, row in df.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(f"""
        <b>{row["해수욕장명"]}</b><br>
        예상 방문자수: {int(row["예상방문자수"]):,}명<br>
        예상 혼잡도: {row["예상혼잡도"]}
        """, max_width=300),
        icon=folium.Icon(color=get_color(row["예상혼잡도"]))
    ).add_to(m)

# ✅ 지도 출력
st.subheader("🗺️ 전국 해수욕장 위치 및 예상 정보")
st_data = st_folium(m, width=900, height=600)
