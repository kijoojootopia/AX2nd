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

# 상위 폴더(..)의 .env 파일 로드
parent_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(parent_dir, "..", ".env")
load_dotenv(dotenv_path=env_path)

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

st.set_page_config(page_title="날씨 & 환율 대시보드", layout="wide")

st.title("날씨 및 환율 대시보드")
st.caption("서울과 전 세계 도시의 날씨 및 현지 환율, 주요 4대 통화 환율을 실시간으로 확인하세요.")

if not WEATHER_API_KEY:
    st.error("OpenWeather API 키를 찾을 수 없습니다. .env 파일을 확인해 주세요.")
    st.stop()

# 국가 코드 -> 통화 코드 및 한글 통화명 매핑 테이블
COUNTRY_CURRENCY_MAP = {
    "KR": ("KRW", "대한민국 원 (KRW)"),
    "US": ("USD", "미국 달러 (USD)"),
    "JP": ("JPY", "일본 엔 (JPY)"),
    "CN": ("CNY", "중국 위안 (CNY)"),
    "GB": ("GBP", "영국 파운드 (GBP)"),
    "EU": ("EUR", "유로 (EUR)"),
    # 유로존 주요 국가
    "FR": ("EUR", "유로 (EUR)"), "DE": ("EUR", "유로 (EUR)"), "IT": ("EUR", "유로 (EUR)"),
    "ES": ("EUR", "유로 (EUR)"), "NL": ("EUR", "유로 (EUR)"), "BE": ("EUR", "유로 (EUR)"),
    "AT": ("EUR", "유로 (EUR)"), "PT": ("EUR", "유로 (EUR)"), "GR": ("EUR", "유로 (EUR)"),
    "IE": ("EUR", "유로 (EUR)"), "FI": ("EUR", "유로 (EUR)"),
    # 기타 주요국
    "AU": ("AUD", "호주 달러 (AUD)"),
    "CA": ("CAD", "캐나다 달러 (CAD)"),
    "CH": ("CHF", "스위스 프랑 (CHF)"),
    "HK": ("HKD", "홍콩 달러 (HKD)"),
    "SG": ("SGD", "싱가포르 달러 (SGD)"),
    "TW": ("TWD", "대만 달러 (TWD)"),
    "TH": ("THB", "태국 바트 (THB)"),
    "VN": ("VND", "베트남 동 (VND)"),
    "PH": ("PHP", "필리핀 페소 (PHP)"),
    "MY": ("MYR", "말레이시아 링깃 (MYR)"),
    "NZ": ("NZD", "뉴질랜드 달러 (NZD)"),
    "TR": ("TRY", "튀르키예 리라 (TRY)"),
    "BR": ("BRL", "브라질 헤알 (BRL)"),
    "IN": ("INR", "인도 루피 (INR)"),
    "MX": ("MXN", "멕시코 페소 (MXN)"),
}

# ----------------- 환율 캐싱 함수 -----------------
@st.cache_data(ttl=3600)
def get_exchange_rates():
    """USD 기준 환율 목록 조회 (1시간 캐싱)"""
    if not EXCHANGE_API_KEY:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get("result") == "success":
            return data.get("conversion_rates", {})
    except requests.exceptions.RequestException:
        pass
    return None

RATES_USD = get_exchange_rates()

def calculate_to_krw(currency_code):
    """지정한 통화 1단위당 원화(KRW) 환율 계산"""
    if not RATES_USD or currency_code not in RATES_USD:
        return None
    krw_rate = RATES_USD.get("KRW", 0)
    target_rate = RATES_USD.get(currency_code, 0)
    if target_rate <= 0:
        return None
    return krw_rate / target_rate

# ----------------- 날씨 조회 함수 (한글/영문 지원) -----------------
def fetch_weather_data(query_city):
    """Geocoding API를 통해 한글/영문 도시명 좌표를 찾고 날씨 정보 획득"""
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": query_city, "limit": 1, "appid": WEATHER_API_KEY}
    
    try:
        geo_res = requests.get(geo_url, params=geo_params, timeout=5)
        geo_data = geo_res.json()
        
        if not geo_data:
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            w_params = {"q": query_city, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}
            w_res = requests.get(weather_url, params=w_params, timeout=5)
            return w_res.status_code, w_res.json(), query_city
            
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        korean_name = geo_data[0].get("local_names", {}).get("ko", geo_data[0]["name"])
        
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        w_params = {"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}
        w_res = requests.get(weather_url, params=w_params, timeout=5)
        return w_res.status_code, w_res.json(), korean_name

    except requests.exceptions.RequestException as e:
        return None, str(e), query_city

# ----------------- 개별 도시 카드 렌더링 -----------------
def display_city_card(header_title, search_keyword):
    status_code, data, resolved_name = fetch_weather_data(search_keyword)

    with st.container(border=True):
        st.subheader(header_title)

        if status_code == 200:
            country_code = data["sys"].get("country", "")
            weather_desc = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            st.markdown(f"### {resolved_name} ({country_code})")

            col_icon, col_desc = st.columns([1, 2])
            with col_icon:
                st.image(f"https://openweathermap.org/img/wn/{icon_code}@2x.png", width=80)
            with col_desc:
                st.write(f"**현재 상태:** {weather_desc}")

            m1, m2 = st.columns(2)
            m1.metric(label="현재 기온", value=f"{temp}°C")
            m2.metric(label="체감 기온", value=f"{feels_like}°C")

            m3, m4 = st.columns(2)
            m3.metric(label="습도", value=f"{humidity}%")
            m4.metric(label="풍속", value=f"{wind_speed} m/s")

            # 현지 통화 환율 영역
            st.divider()
            st.markdown("##### 현지 통화 환율")

            if not EXCHANGE_API_KEY:
                st.caption(".env에 환율 API 키가 설정되지 않았습니다.")
            elif country_code == "KR":
                st.info("기준 통화 국가(대한민국 원화 KRW)입니다.")
            else:
                currency_info = COUNTRY_CURRENCY_MAP.get(country_code)
                if currency_info:
                    curr_code, curr_name = currency_info
                    krw_val = calculate_to_krw(curr_code)

                    if krw_val:
                        if curr_code in ["JPY", "VND"]:
                            st.metric(
                                label=f"{curr_name} (100 {curr_code})",
                                value=f"{krw_val * 100:,.2f} 원"
                            )
                        else:
                            st.metric(
                                label=f"{curr_name} (1 {curr_code})",
                                value=f"{krw_val:,.2f} 원"
                            )
                    else:
                        st.caption(f"{curr_code} 환율 데이터를 불러올 수 없습니다.")
                else:
                    st.caption(f"해당 국가({country_code})의 통화 매핑 정보가 등록되어 있지 않습니다.")

        elif status_code == 404:
            st.error(f"'{search_keyword}' 도시를 찾을 수 없습니다. 검색어를 확인해 주세요.")
        else:
            msg = data.get("message", "알 수 없는 오류") if isinstance(data, dict) else data
            st.error(f"오류가 발생했습니다: {msg}")

# ----------------- 사이드바 설정 -----------------
with st.sidebar:
    st.header("도시 검색")
    target_city = st.text_input(
        "비교할 도시 입력 (한글/영문)",
        value="도쿄",
        placeholder="예: 도쿄, 파리, 런던, 뉴욕, 베이징"
    ).strip()

# ----------------- 1. 도시별 날씨 및 현지 환율 비교 -----------------
col_seoul, col_compare = st.columns(2)

with col_seoul:
    display_city_card("기준 도시: 서울", "서울")

with col_compare:
    if target_city:
        display_city_card(f"비교 도시: {target_city}", target_city)
    else:
        st.info("사이드바에서 비교할 도시를 입력해 주세요.")

# ----------------- 2. 주요 4대 통화 기본 환율 섹션 -----------------
st.write("")
st.subheader("주요 통화 실시간 환율 (대 원화 KRW)")

if not EXCHANGE_API_KEY:
    st.warning("환율 API 키(EXCHANGERATE_API_KEY)가 .env 파일에 등록되어 있지 않습니다.")
elif not RATES_USD:
    st.error("환율 서버와 연결할 수 없거나 데이터를 가져오지 못했습니다.")
else:
    usd_val = calculate_to_krw("USD")
    jpy_val = calculate_to_krw("JPY")
    eur_val = calculate_to_krw("EUR")
    cny_val = calculate_to_krw("CNY")

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        if usd_val:
            c1.metric(label="미국 USD (1 달러)", value=f"{usd_val:,.2f} 원")
        if jpy_val:
            c2.metric(label="일본 JPY (100 엔)", value=f"{jpy_val * 100:,.2f} 원")
        if eur_val:
            c3.metric(label="유럽 EUR (1 유로)", value=f"{eur_val:,.2f} 원")
        if cny_val:
            c4.metric(label="중국 CNY (1 위안)", value=f"{cny_val:,.2f} 원")