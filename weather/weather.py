# 날씨 API 실습
# OpenWeatherMap 현재 날씨 API로 특정 도시의 날씨를 가져와 출력한다.
# 사전 준비 OpenWeatherMap API 발급
# .env는 외부에 만들어놓은 환경변수
# pip install requests python-dotenv
#.env 파일을 생성하고 이곳에  OPENWEATHER_API_KEY=발급받은_API_키 (깃ignore로 안올라감)
# .env.example OPENWEATHER_API_KEY=your_key (올라감)
# 받고 나면 .env.example을 .env로 파일명, your_key에 내 API 바꾸기

import os
import requests
import streamlit as st
from dotenv import load_dotenv  #env 끌고 오는 설정

# 로컬 환경 .env 파일 로드
parent_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(parent_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

# 배포 환경(Streamlit Secrets)과 로컬(.env) 호환
WEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY"))
EXCHANGE_API_KEY = st.secrets.get("EXCHANGERATE_API_KEY", os.getenv("EXCHANGERATE_API_KEY"))

st.set_page_config(page_title="날씨 & 환율 대시보드", layout="wide")

st.title("날씨 및 환율 대시보드")
st.caption("서울과 전 세계 도시의 실시간 날씨 및 주요 환율 정보를 한눈에 비교합니다.")

if not WEATHER_API_KEY:
    st.error("OpenWeather API 키를 찾을 수 없습니다. 설정(.env 또는 Secrets)을 확인해 주세요.")
    st.stop()

# ----------------- 날씨 관련 함수 -----------------
def get_weather(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

def display_weather_card(title, city_query):
    status_code, data = get_weather(city_query)

    with st.container(border=True):
        st.subheader(title)

        if status_code == 200:
            weather_desc = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            city_display = f"{data['name']}, {data['sys']['country']}"

            st.markdown(f"### {city_display}")
            
            col_icon, col_desc = st.columns([1, 2])
            with col_icon:
                icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, width=80)
            with col_desc:
                st.write(f"**상태:** {weather_desc}")

            m1, m2 = st.columns(2)
            m1.metric(label="현재 기온", value=f"{temp}°C")
            m2.metric(label="체감 기온", value=f"{feels_like}°C")

            m3, m4 = st.columns(2)
            m3.metric(label="습도", value=f"{humidity}%")
            m4.metric(label="풍속", value=f"{wind_speed} m/s")

        elif status_code == 404:
            st.error(f"'{city_query}' 도시를 찾을 수 없습니다. 영문 철자를 확인해 주세요.")
        elif status_code == 401:
            st.error("유효하지 않은 날씨 API 키입니다.")
        else:
            msg = data.get("message", "알 수 없는 오류") if isinstance(data, dict) else data
            st.error(f"오류가 발생했습니다: {msg}")

# ----------------- 환율 관련 함수 -----------------
@st.cache_data(ttl=3600)  # 환율 정보는 1시간 캐싱하여 API 호출 절약
def get_exchange_rates(base_currency):
    if not EXCHANGE_API_KEY:
        return None, "환율 API 키가 설정되지 않았습니다."
    
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rates", {}), None
        else:
            return None, data.get("error-type", "알 수 없는 환율 API 오류")
    except requests.exceptions.RequestException as e:
        return None, str(e)

# ----------------- 사이드바 -----------------
with st.sidebar:
    st.header("설정")
    target_city = st.text_input(
        "비교할 도시 이름 (영문)",
        value="Tokyo",
        placeholder="예: Tokyo, New York, Paris"
    ).strip()

# ----------------- 1. 날씨 정보 섹션 -----------------
st.write("### 1. 실시간 날씨 비교")
col_seoul, col_compare = st.columns(2)

with col_seoul:
    display_weather_card("기준 도시: 서울", "Seoul")

with col_compare:
    if target_city:
        display_weather_card(f"비교 도시: {target_city.title()}", target_city)
    else:
        st.info("사이드바에서 비교할 도시를 입력해 주세요.")

# ----------------- 2. 환율 정보 섹션 -----------------
st.write("### 2. 주요 환율 정보")

if not EXCHANGE_API_KEY:
    st.warning("환율 API 키가 등록되지 않아 환율 정보를 표시할 수 없습니다.")
else:
    # 기준 통화 USD 기반 데이터 가져오기
    rates_usd, err = get_exchange_rates("USD")

    if err:
        st.error(f"환율 정보를 가져오는 중 오류가 발생했습니다: {err}")
    elif rates_usd:
        krw_rate = rates_usd.get("KRW", 0)
        jpy_rate = rates_usd.get("JPY", 0)
        eur_rate = rates_usd.get("EUR", 0)
        cny_rate = rates_usd.get("CNY", 0)

        # 100엔당 원화, 1유로당 원화 계산
        jpy_to_krw = (krw_rate / jpy_rate * 100) if jpy_rate else 0
        eur_to_krw = (krw_rate / eur_rate) if eur_rate else 0
        cny_to_krw = (krw_rate / cny_rate) if cny_rate else 0

        with st.container(border=True):
            st.markdown("#### 원화(KRW) 기준 주요 통화 환율")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric(label="미국 USD / KRW", value=f"{krw_rate:,.2f} 원")
            r2.metric(label="일본 JPY(100엔) / KRW", value=f"{jpy_to_krw:,.2f} 원")
            r3.metric(label="유럽 EUR / KRW", value=f"{eur_to_krw:,.2f} 원")
            r4.metric(label="중국 CNY / KRW", value=f"{cny_to_krw:,.2f} 원")