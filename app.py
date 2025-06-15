import streamlit as st
import pandas as pd

# ✅ 스타일
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

    @media screen and (max-width: 600px) {
        .title {
            font-size: 26px;
        }
        .subtitle {
            font-size: 14px;
        }
        .result-card {
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 제목
st.markdown("<div class='title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</div>", unsafe_allow_html=True)

# ✅ 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 입력 받기
beaches = sorted(df["해수욕장이름"].unique())
selected_beach = st.selectbox("📍 해수욕장을 선택하세요", beaches)

min_date = pd.to_datetime("2025-06-01")
max_date = pd.to_datetime("2025-08-31")
selected_date = st.date_input("📅 방문 날짜를 선택하세요", min_value=min_date, max_value=max_date)

if st.button("🔍 예측 결과 보기"):
    result = df[
        (df["해수욕장이름"] == selected_beach) &
        (df["해수욕장일일일자"] == pd.to_datetime(selected_date))
    ]

    if not result.empty:
        count = int(result["예상 방문자수"].values[0])
        congestion = result["예상 혼잡도"].values[0]

        color_map = {"여유": "#4CAF50", "보통": "#FFC107", "혼잡": "#F44336"}
        color = color_map.get(congestion, "#333")

        # 개장일~폐장일 구하기
        beach_data = df[df["해수욕장이름"] == selected_beach]
        open_day = beach_data["해수욕장일일일자"].min().strftime('%Y-%m-%d')
        close_day = beach_data["해수욕장일일일자"].max().strftime('%Y-%m-%d')

        st.markdown(f"""
        <div class="result-card">
            <h4 style="color:#0072C6;">📍 {selected_beach}의 예상 운영 기간은 {open_day} ~ {close_day} 입니다</h4>
            <p style="font-size:17px;">👥 <b>예상 방문자수:</b> {count:,}명</p>
            <p style="font-size:17px;">📌 <b style="color:{color};">예상 혼잡도: {congestion}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("선택한 날짜의 예측 데이터가 없습니다. 다른 날짜를 선택해주세요.")

# ✅ 지도 삽입 (iframe)
st.markdown("## 🗺️ 전체 해수욕장 예측 혼잡도 지도")
with open("2025_해수욕장_예상혼잡도지도_최종버전.html", "r", encoding="utf-8") as f:
    map_html = f.read()
st.components.v1.html(map_html, height=600, scrolling=True)
