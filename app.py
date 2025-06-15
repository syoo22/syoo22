import streamlit as st
import pandas as pd

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

# 제목
st.title("🏖️ 해수욕장 방문자 예측 시스템")
st.markdown("원하는 **해수욕장**과 **방문 날짜**를 선택하면, 예상 방문자수와 혼잡도를 알려드려요!")

# 해수욕장 선택
beach_names = df["해수욕장이름"].unique()
selected_beach = st.selectbox("해수욕장을 선택하세요", sorted(beach_names))

# 날짜 선택 (운영 기간 제한)
min_date = pd.to_datetime("2025-06-01")
max_date = pd.to_datetime("2025-08-31")
selected_date = st.date_input(
    "방문 날짜를 선택하세요 (2025년 6월 1일 ~ 8월 31일)",
    min_value=min_date,
    max_value=max_date
)

# 버튼 누르면 예측 결과 출력
if st.button("예측 결과 보기"):
    result = df[
        (df["해수욕장이름"] == selected_beach) &
        (df["해수욕장일일일자"] == pd.to_datetime(selected_date))
    ]

    if not result.empty:
        방문자수 = int(result["예상 방문자수"].values[0])
        혼잡도 = result["예상 혼잡도"].values[0]

        st.success(f"📅 {selected_date.strftime('%Y-%m-%d')} {selected_beach}의 예측 결과:")
        st.markdown(f"**👥 예상 방문자수**: {방문자수:,}명")
        st.markdown(f"**📌 예상 혼잡도**: {혼잡도}")
    else:
        st.warning("이 날짜에는 예측 데이터가 없어요. 다른 날짜를 선택해보세요.")
