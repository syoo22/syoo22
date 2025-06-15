import streamlit as st
import pandas as pd

# ✅ 페이지 기본 설정
st.set_page_config(page_title="해수욕장 방문자 예측 시스템", layout="wide")

# ✅ 배경 및 스타일 설정
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

# ✅ 타이틀
st.markdown("<div class='title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>해수욕장과 날짜를 선택하면 예상 방문자수와 혼잡도를 알려드려요!</div>", unsafe_allow_html=True)

# ✅ 데이터 로딩 함수 (예측 데이터)
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 해수욕장 선택
beach_names = sorted(df["해수욕장명"].unique())
selected_beach = st.selectbox("📍 해수욕장을 선택하세요", beach_names)

# ✅ 예상 운영 기간 표시
beach_df = df[df["해수욕장명"] == selected_beach]
if not beach_df.empty:
    open_date = beach_df["해수욕장일일일자"].min().strftime('%Y-%m-%d')
    close_date = beach_df["해수욕장일일일자"].max().strftime('%Y-%m-%d')
    st.markdown(f"🧾 <b>{selected_beach}</b>의 예상 운영 기간은 <b>{open_date}</b>부터 <b>{close_date}</b>까지입니다.", unsafe_allow_html=True)

# ✅ 방문 날짜 입력
min_date = pd.to_datetime("2025-06-01")
max_date = pd.to_datetime("2025-08-31")
selected_date = st.date_input("🔮 방문 날짜를 선택하세요", min_value=min_date, max_value=max_date)

# ✅ 예측 결과 출력
if st.button("🔍 예측 결과 보기"):
    result = df[
        (df["해수욕장명"] == selected_beach) &
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

# ✅ 과거 방문자수 평균 추세 그래프
@st.cache_data
def load_past_data():
    past = pd.read_csv("해양수산부_해수욕장일일이용객수_정보.csv")
    past["이용일자"] = pd.to_datetime(past["이용일자"])  # ✅ 정확한 컬럼명
    past["월일"] = past["이용일자"].dt.strftime("%m-%d")
    return past

past_df = load_past_data()
past_beach_df = past_df[past_df["해수욕장명"] == selected_beach]

if not past_beach_df.empty:
    avg_by_day = (
        past_beach_df.groupby("월일")["이용객수"]
        .mean()
        .reset_index()
        .rename(columns={"이용객수": "평균이용객수"})
    )
    avg_by_day["날짜"] = pd.to_datetime("2025-" + avg_by_day["월일"], format="%Y-%m-%d")

    import altair as alt
    past_chart = (
        alt.Chart(avg_by_day)
        .mark_line(point=True)
        .encode(
            x=alt.X("날짜:T", title="날짜"),
            y=alt.Y("평균이용객수:Q", title="과거 평균 이용객 수"),
            tooltip=["날짜:T", "평균이용객수:Q"]
        )
        .properties(
            width=700,
            height=300,
            title=f"📊 {selected_beach}의 과거 일자별 평균 방문자수 추세"
        )
    )

    st.markdown("### ⏳ 과거 평균 방문자수 추세")
    st.altair_chart(past_chart, use_container_width=True)
else:
    st.info(f"📭 과거 '{selected_beach}' 데이터가 없어 추세 그래프를 그릴 수 없습니다.")

# ✅ HTML 지도 시각화
st.markdown("---")
st.markdown("### 🗺️ 해수욕장 전체 예측 혼잡도 지도")
with open("2025_해수욕장_예상혼잡도지도_최종버전.html", "r", encoding="utf-8") as f:
    html_data = f.read()
    st.components.v1.html(html_data, height=600, scrolling=True)
