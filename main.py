import pandas as pd

df = pd.read_csv(
    "202606_202606_jumindeungrogingugitahyeonhwang-goryeong-inguhyeonhwang-_weolgan.csv",
    encoding="cp949"
)

print(df.columns)
print(df.head())
