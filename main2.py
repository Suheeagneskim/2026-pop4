import pandas as pd

df = pd.read_csv(
    "202606_202606_jumindeungrogingugitahyeonhwang-goryeong-inguhyeonhwang-_weolgan.csv",
    encoding="cp949"
)

# 1) '서울특별시 종로구 '로 시작하는 행만 선택 (종로구 전체 + 각 동)
jongno = df[df["행정구역"].str.startswith("서울특별시 종로구 ")].copy()

# 2) 종로구 전체(행정구역이 '서울특별시 종로구 (코드)'인 행)는 제외하고 동만 남기기
jongno_dong = jongno[~jongno["행정구역"].str.match(r"서울특별시 종로구 \\(")].copy()

# 3) 행정구역에서 동 이름만 깔끔하게 추출 (괄호에 들어 있는 코드 제거)
jongno_dong["동이름"] = jongno_dong["행정구역"].str.replace(r"\\(.*\\)", "", regex=True).str.strip()

# 4) 문자열 숫자에서 콤마 제거 후 숫자로 변환
for col in ["2026년06월_전체", "2026년06월_65세이상전체"]:
    jongno_dong[col] = pd.to_numeric(
        jongno_dong[col].astype(str).str.replace(",", ""),
        errors="coerce"
    )

# 5) 고령화율(%) 계산
jongno_dong["고령화율_%"] = jongno_dong["2026년06월_65세이상전체"] / jongno_dong["2026년06월_전체"] * 100

print(jongno_dong[["동이름", "2026년06월_전체", "2026년06월_65세이상전체", "고령화율_%"]].head())
