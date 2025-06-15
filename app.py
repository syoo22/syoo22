import streamlit as st
import pandas as pd

# ✅ 바다 느낌 배경 및 전체 스타일 적용
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #a2d4f7, #e0f7fa);
        font-family: 'Helvetica', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #003366;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #004080;
        margin-top: 0;
    }
    .result-card {
        background-color: #ffffffdd;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 상단 제목
st.markdown("<div class='title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</div>", unsafe_allow_html=True)

# ✅ 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 사용자 입력
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

        # 혼잡도 색상 지정
        color_map = {"여유": "#4CAF50", "보통": "#FFC107", "혼잡": "#F44336"}
        color = color_map.get(congestion, "#333")

        # ✅ 결과 카드 스타일 적용
        st.markdown(f"""
        <div class="result-card">
            <h4 style="color:#0072C6;">📅 {selected_date.strftime('%Y-%m-%d')} {selected_beach}의 예측 결과</h4>
            <p style="font-size:18px;">👥 <b>예상 방문자수:</b> {count:,}명</p>
            <p style="font-size:18px;">📌 <b style="color:{color};">예상 혼잡도: {congestion}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("선택한 날짜의 데이터가 없습니다. 다시 선택해주세요.")
