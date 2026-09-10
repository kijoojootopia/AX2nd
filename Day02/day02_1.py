import streamlit as st
import pandas as pd
import os

# 데이터 가져오기 (다른 경로에서 가져올 경우)
csv_path = os.path.join(os.path.dirname(__file__), "..", "common", "raw_trade_data.csv")
# 같은 경로에서 데이터 가져올 경우
# csv_path = os.path.join(os.path.dirname(__file__), "raw_trade_data.csv")

# 환율샘플 데이터
# 딕셔너리로 표 만들기
exchange_data = {
    '통화' : ['USD','EUR','JPY(100엔)','CNY'],
    '환율(KRW)' : [1399,1503,930,191],
    '전일대비' : [5200,3100,1000,400],
 }
# 마지막 항목 뒤에 쉼표를 붙여도(Trailing Comma) 정상 동작하며, 
# 나중에 항목을 추가하거나 수정할 때 편리해서 자주 사용됩니다.

# 판다스를 이용하여 엑셀 데이터 처럼 만들기
df_exchange = pd.DataFrame(exchange_data)


st.title('💱 오늘의 환율 대시보드')
st.caption('아래 데이터는 실제 환율이 아닌 실습용 샘플 데이터입니다.')
st.subheader('1) 환율 표 보기')
# 특수문자 쓰는 법 : 자음(ㅁ) + 한자 키보드 / 이모지 : win + .
st.write('▶ st.dataframe (상호작용 가능한 표)')

# dataframe/DataFrame streamlit/pandas
# 표 창 너비 옵션 true 기본값(생략)
st.dataframe(df_exchange, use_container_width=True)

st.write('▶ st.table (정적인 표)')
st.table(df_exchange)
st.markdown("---")

st.subheader('2) 주요 환율 카드(st.metric)')

# st.metric(라벨, 현재값, 증감값)
col1, col2, col3 =st.columns(3) # 3컬럼으로 나누기 정의

with col1:
    st.metric(label='USD/KRW', value='1450.5', delta="+5.2")
with col2:
    st.metric(label='EUR/KRW', value='1503.2', delta="-3.1")
with col3:
    st.metric(label='JPY(100엔)/KRW', value='930.8', delta="+1.0")
    
st.markdown("---")
st.subheader('3) 환율 표 보기')
st.write('공용 데이터 파일 raw_trade_data.csv를 읽어온 상위 5행입니다.')

# pandas 읽어와야함
df_trade_raw = pd.read_csv(csv_path, encoding='UTF-8')
st.dataframe(df_trade_raw.head(5), use_container_width=True)
