import pandas as pd
import streamlit as st

st.title("💄 이커머스 데이터 필터링 ＆ 결측치 정리")
st.caption('나이/성별 조건으로 필터링해보고, 결측치를 제거해 새 csv로 저장합니다.')

csv_path = ('..\common\ecommerce_customer_behavior_dataset.csv')

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error('❌파일을 찾을 수 없습니다.')
else:
    st.metric('원본 데이터 행 개수',f'{len(df)}행')
    st.markdown('---')
    st.subheader('1) 나이 35세 이상 고객')

    over_35 = df[df['Age']>=35]
    st.write(f'나이 35세 이상 승객 수 : **{len(over_35)}**명')
    st.dataframe(over_35[['Customer_ID','Gender','Age']].head())

    st.subheader('2) 성별 필터링 결과')
