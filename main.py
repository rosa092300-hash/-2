import streamlit as st
import math
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="다기능 계산기 및 세계 인구 분석", layout="wide")
st.title("다기능 계산기 및 세계 인구 분석")

# --- 사이드바 메뉴 ---
st.sidebar.header("메뉴 선택")
menu = st.sidebar.selectbox(
    "기능 선택",
    [
        "사칙연산 ( + , - , * , / )",
        "나머지 연산",
        "지수 연산",
        "로그 연산",
        "연도별 세계 인구 분석",
    ]
)

# ----------------------------- 계산기 기능 -----------------------------
if menu == "사칙연산 ( + , - , * , / )":
    st.subheader("사칙연산")
    a = st.number_input("첫 번째 숫자 (a)를 입력하세요:", value=0.0, format="%f")
    b = st.number_input("두 번째 숫자 (b)를 입력하세요:", value=0.0, format="%f")
    op = st.selectbox("연산자를 선택하세요", ["+", "-", "*", "/"]) 
    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("0으로 나눌 수 없습니다.")
            result = a / b
        st.success(f"결과: {result}")
    except ZeroDivisionError:
        st.error("오류: 0으로 나눌 수 없습니다.")
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")

elif menu == "나머지 연산":
    st.subheader("나머지 연산 (a % b)")
    use_ints = st.checkbox("입력을 정수로 처리하기 (소수 입력 시 내림 처리)", value=True)
    a_raw = st.number_input("피제수 (a)를 입력하세요:", value=0.0, format="%f")
    b_raw = st.number_input("제수 (b)를 입력하세요:", value=1.0, format="%f")
    try:
        if b_raw == 0:
            raise ZeroDivisionError("0으로 나머지를 구할 수 없습니다.")
        if use_ints:
            a = int(math.floor(a_raw))
            b = int(math.floor(b_raw))
            result = a % b
            st.info(f"정수 처리된 값: a={a}, b={b}")
        else:
            a = a_raw
            b = b_raw
            result = a % b
        st.success(f"결과: {result}")
    except ZeroDivisionError:
        st.error("오류: 0으로 나눌 수 없습니다.")
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")

elif menu == "지수 연산":
    st.subheader("지수 연산 (a^b)")
    a = st.number_input("밑 (a)를 입력하세요:", value=0.0, format="%f")
    b = st.number_input("지수 (b)를 입력하세요:", value=0.0, format="%f")
    try:
        if abs(b) > 1e6:
            st.warning("지수 값이 너무 커서 계산 중 오류가 발생할 수 있습니다.")
        result = a ** b
        st.success(f"결과: {result}")
    except OverflowError:
        st.error("오류: 계산 결과가 너무 커서 처리할 수 없습니다.")
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")

elif menu == "로그 연산":
    st.subheader("로그 연산")
    a = st.number_input("로그 값 (a)를 입력하세요 (a > 0):", value=1.0, format="%f")
    base_option = st.selectbox("로그의 밑 선택:", ["자연로그 (e)", "상용로그 (10)", "사용자 지정"])
    if base_option == "사용자 지정":
        base = st.number_input("밑을 입력하세요 (0보다 크고 1이 아니어야 함):", value=math.e, format="%f")
    elif base_option == "상용로그 (10)":
        base = 10.0
    else:
        base = math.e

    try:
        if a <= 0:
            raise ValueError("로그의 입력 값은 0보다 커야 합니다.")
        if base <= 0 or base == 1:
            raise ValueError("로그의 밑은 0보다 크고 1이 아니어야 합니다.")
        result = math.log(a, base)
        st.success(f"결과: 밑 {base} 로그 {a} = {result}")
    except ValueError as ve:
        st.error(f"오류: {ve}")
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")

# ----------------------------- 세계 인구 분석 기능 -----------------------------
elif menu == "연도별 세계 인구 분석":
    st.subheader("연도별 세계 인구 분석")
    st.write("1970~2010년(10년 단위) 및 2015, 2020, 2022년의 국가별 인구를 시각화합니다.")

    # 데이터 파일 불러오기 (사용자는 world_population.csv 업로드 필요)
    uploaded = st.file_uploader("세계 인구 데이터 CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)

        # 국가/연도/인구 컬럼이 필요함
        st.write("데이터 미리보기")
        st.dataframe(df.head())

        year = st.selectbox("연도를 선택하세요", [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022])

        if "Country" in df.columns and str(year) in df.columns:
            df_year = df[["Country", str(year)]].rename(columns={str(year): "Population"})

            st.write(f"### 🌍 {year}년 세계 인구 지도")

            fig = px.choropleth(
                df_year,
                locations="Country",
                locationmode="country names",
                color="Population",
                hover_name="Country",
                color_continuous_scale="Viridis",
                title=f"{year}년 세계 인구",
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("데이터에 'Country' 또는 선택한 연도가 포함되어 있지 않습니다.")
    else:
        st.info("CSV
