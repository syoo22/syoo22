import streamlit as st
import pandas as pd

# ✅ 스타일 (배경 + 제목 꾸미기)
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #a0eafc, #ffffff);
    }
    .main-title {
        font-size: 40px;
        text-align: center;
        font-weight: bold;
        color: #003366;
    }
    .sub-title {
        font-size: 16px;
        text-align: center;
        color: #004080;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ 페이지 타이틀
st.markdown("<div class='main-title'>🏖️ 해수욕장 방문자 예측 시스템</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>원하는 <b>해수욕장</b>과 <b>방문 날짜</b>를 선택하면, 예측 방문자수와 혼잡도를 알려드려요!</div>", unsafe_allow_html=True)

# ✅ 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# ✅ 선택박스
beach_names = df["해수욕장이름"].unique()
selected_beach = st.selectbox("🌊 해수욕장을 선택하세요", sorted(beach_names))

min_date = pd.to_datetime("2025-06-01")
max_date = pd.to_datetime("2025-08-31")
selected_date = st.date_input("📅 방문 날짜를 선택하세요 (2025년 6월 1일 ~ 8월 31일)", min_value=min_date, max_value=max_date)

# ✅ 버튼 클릭 시 결과 출력
if st.button("🔍 예측 결과 보기"):
    result = df[
        (df["해수욕장이름"] == selected_beach) &
        (df["해수욕장일일일자"] == pd.to_datetime(selected_date))
    ]

    if not result.empty:
        방문자수 = int(result["예상 방문자수"].values[0])
        혼잡도 = result["예상 혼잡도"].values[0]

        # ✅ 혼잡도 색상 지정
        if 혼잡도 == "여유":
            혼잡색 = "#4CAF50"
        elif 혼잡도 == "보통":
            혼잡색 = "#FFC107"
        else:
            혼잡색 = "#F44336"

        # ✅ 결과 카드 형태 출력
        st.markdown(f"""
        <div style="background-color:#e0f7fa;padding:20px 30px;border-radius:10px;margin-top:20px;">
            <h4 style='color:#0072C6;'>📅 {selected_date.strftime('%Y-%m-%d')} {selected_beach}의 예측 결과</h4>
            <p style='font-size:18px;'>👥 <b>예상 방문자수:</b> {방문자수:,}명</p>
            <p style='font-size:18px;'>📌 <b style='color:{혼잡색};'>예상 혼잡도: {혼잡도}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("이 날짜에는 예측 데이터가 없어요. 다른 날짜를 선택해보세요.")
