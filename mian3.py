import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="종로구 동별 고령화율", layout="wide")

@st.cache_data(show_spinner="데이터를 불러오는 중입니다...")
def load_data():
    df = pd.read_csv(
        "202606_202606_jumindeungrogingugitahyeonhwang-goryeong-inguhyeonhwang-_weolgan.csv",
        encoding="cp949"
    )
    return df

def main():
    st.title("서울특별시 종로구 동별 고령화율 (2026년 6월)")

    df = load_data()

    # 종로구 관련 행만
    jongno = df[df["행정구역"].str.startswith("서울특별시 종로구 ")].copy()

    # 종로구 전체 행 제거 (괄호 바로 앞에서 끝나는 패턴)
    jongno_dong = jongno[~jongno["행정구역"].str.match(r"서울특별시 종로구 \\(")].copy()

    # 동 이름만 추출
    jongno_dong["동이름"] = jongno_dong["행정구역"].str.replace(r"\\(.*\\)", "", regex=True).str.strip()

    # 숫자 변환
    for col in ["2026년06월_전체", "2026년06월_65세이상전체"]:
        jongno_dong[col] = pd.to_numeric(
            jongno_dong[col].astype(str).str.replace(",", ""),
            errors="coerce"
        )

    # 고령화율 계산
    jongno_dong["고령화율_%"] = jongno_dong["2026년06월_65세이상전체"] / jongno_dong["2026년06월_전체"] * 100

    # 정렬 (고령화율 높은 순)
    jongno_dong = jongno_dong.sort_values("고령화율_%", ascending=False)

    st.subheader("동별 고령화율(65세 이상 비율)")

    fig = px.bar(
        jongno_dong,
        x="동이름",
        y="고령화율_%",
        labels={"동이름": "동 이름", "고령화율_%": "65세 이상 비율(%)"},
        title="서울특별시 종로구 동별 65세 이상 인구 비율",
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="65세 이상 인구 비율(%)",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("데이터 테이블")
    st.dataframe(
        jongno_dong[["동이름", "2026년06월_전체", "2026년06월_65세이상전체", "고령화율_%"]],
        use_container_width=True
    )

    st.info("고령화율 상위 동은 외상·응급의료·지역사회 돌봄에서 우선 개입 대상 동네로 볼 수 있습니다.")

if __name__ == "__main__":
    main()
