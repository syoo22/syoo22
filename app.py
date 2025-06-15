import streamlit as st
import pandas as pd

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("2025_해수욕장_예측결과.csv")
    df["해수욕장일일일자"] = pd.to_datetime(df["해수욕장일일일자"])
    return df

df = load_data()

st.title("🏖️ 해수욕장 방문자 예측 시스템")
st.markdown("원하는 **해수욕장**과 **방문 날짜**를 선택하면, 예상 방문자수와 혼잡도를 알려드려요!")

# 해수욕장명 목록 추출
beach_names = sorted(df["해수욕장이름"].unique())
selected_beach = st.selectbox("해수욕장을 선택하세요", beach_names)

# 날짜 선택 (데이터 범위에 맞게 설정)
min_date = df["해수욕장일일일자"].min()
max_date = df["해수욕장일일일자"].max()
selected_date = st.date_input("방문 날짜를 선택하세요", min_value=min_date, max_value=max_date)

# 검색 버튼
if st.button("예측 결과 보기"):
    result = df[(df["해수욕장이름"] == selected_beach) & (df["해수욕장일일일자"] == pd.to_datetime(selected_date))]

    if not result.empty:
        visitors = int(result.iloc[0]["예상 방문자수"])
        congestion = result.iloc[0]["예상 혼잡도"]
        st.success(f"📅 {selected_date} {selected_beach}의 예측 결과:")
        st.markdown(f"👥 **예상 방문자수:** {visitors:,}명")
        st.markdown(f"🌡️ **예상 혼잡도:** **{congestion}**")
    else:
        st.warning("해당 해수욕장의 해당 날짜에 대한 예측 데이터가 없습니다.")
