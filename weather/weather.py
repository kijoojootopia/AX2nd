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

# 상위 폴더(..)의 .env 파일 경로 지정
parent_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(parent_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 반응형 및 넓은 화면 구성을 위해 layout을 "wide"로 설정
st.set_page_config(page_title="날씨 비교 대시보드", layout="wide")

st.title("날씨 비교 대시보드")
st.caption("서울의 현재 날씨와 다른 도시의 날씨를 실시간으로 비교합니다.")

if not API_KEY:
    st.error("API 키를 찾을 수 없습니다. 상위 폴더의 .env 파일을 확인해 주세요.")
    st.stop()

# 날씨 데이터를 가져오는 함수
def get_weather(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

# 날씨 정보를 카드 형태로 렌더링하는 함수
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
            st.error("유효하지 않은 API 키입니다. 키 설정을 점검해 주세요.")
        else:
            msg = data.get("message", "알 수 없는 오류") if isinstance(data, dict) else data
            st.error(f"오류가 발생했습니다: {msg}")

# 비교 대상 도시 입력 영역
with st.sidebar:
    st.header("도시 검색")
    target_city = st.text_input(
        "비교할 도시 이름 (영문)",
        value="Tokyo",
        placeholder="예: Tokyo, New York, Paris"
    ).strip()

# 2개 컬럼을 사용한 비교 레이아웃
col_seoul, col_compare = st.columns(2)

with col_seoul:
    display_weather_card("기준 도시: 서울", "Seoul")

with col_compare:
    if target_city:
        display_weather_card(f"비교 도시: {target_city.title()}", target_city)
    else:
        st.info("사이드바에서 비교할 도시를 입력해 주세요.")