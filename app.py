import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl

# ✅ 한글 폰트 설정
mpl.rcParams['font.family'] = 'NanumGothic'

# ✅ 페이지 설정
st.set_page_config(page_title="해수욕장 방문자 예측 시스템", layout="wide")

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
        .title { font-size: 26px; }
        .subtitle { font-size: 14px; }
        .result-card { padding: 15px; }
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 제목
st.markdown("<div class='title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</div>", unsafe_allow_html=True)

# ✅ 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 해수욕장 선택
beach_names = sorted(df["해수욕장이름"].unique())
selected_beach = st.selectbox("📍 해수욕장을 선택하세요", beach_names)

# ✅ 운영 기간 안내
beach_df = df[df["해수욕장이름"] == selected_beach]
if not beach_df.empty:
    open_date = beach_df["해수욕장일일일자"].min().strftime('%Y-%m-%d')
    close_date = beach_df["해수욕장일일일자"].max().strftime('%Y-%m-%d')
    st.markdown(f"🧾 <b>{selected_beach}</b>의 예상 운영 기간은 <b>{open_date}</b>부터 <b>{close_date}</b>까지입니다.", unsafe_allow_html=True)

# ✅ 날짜 선택
min_date = pd.to_datetime("2025-06-01")
max_date = pd.to_datetime("2025-08-31")
selected_date = st.date_input("🔮 방문 날짜를 선택하세요", min_value=min_date, max_value=max_date)

# ✅ 예측 결과 카드
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

        st.markdown(f"""
        <div class="result-card">
            <h4 style="color:#0072C6;">📅 {selected_date.strftime('%Y-%m-%d')} {selected_beach}의 예측 결과</h4>
            <p style="font-size:17px;">👥 <b>예상 방문자수:</b> {count:,}명</p>
            <p style="font-size:17px;">📌 <b style="color:{color};">예상 혼잡도: {congestion}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("❗ 선택한 날짜의 예측 데이터가 없습니다. 다른 날짜를 선택해주세요.")

    # ✅ 방문자수 추이 그래프
    st.markdown("---")
    st.markdown(f"### 📊 {selected_beach}의 6~8월 방문자수 추이")
    beach_trend = df[df["해수욕장이름"] == selected_beach].sort_values("해수욕장일일일자")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(beach_trend["해수욕장일일일자"], beach_trend["예상 방문자수"], marker='o', linewidth=2, color="#0072C6")
    ax.set_title(f"{selected_beach} 방문자수 추이 (2025.06 ~ 08)", fontsize=14)
    ax.set_xlabel("날짜")
    ax.set_ylabel("예상 방문자수")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(True)
    st.pyplot(fig)

# ✅ 혼잡도 지도
st.markdown("---")
st.markdown("### 🗺️ 해수욕장 전체 예측 혼잡도 지도")
with open("2025_해수욕장_예상혼잡도지도_최종버전.html", "r", encoding="utf-8") as f:
    html_data = f.read()
    st.components.v1.html(html_data, height=600, scrolling=True)
