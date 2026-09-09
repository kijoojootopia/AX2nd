# raw_trade_data.csv 파일 활용
# HS CODE가  85로 시작하는 (반도체류) 
# + 국가명 미국 또는 베트남 + 수출금액 0 보다 큰 수 (실제 수출실적이 있는)
# 다중 조건으로 필터링 한 뒤, 수출 금액 상위 10건 화면에 보여주고 report.csv로 저장
# streamlit 사용 streamlit run day04_1.py

import os
import pandas as pd
import streamlit as st

# 기본 파일 경로 설정 (데이터를 불러올 원본 경로와 저장할 결과 파일 경로)
default_csv_path = r'C:\Users\user\AX2nd\common\raw_trade_data.csv'
report_output_path = 'report.csv'

def load_and_filter_data(csv_path = default_csv_path):
    '''
    무역 데이터를 불러와서 특정 조건에 맞게 필터링한 뒤,
수출금액 기준 내림차순으로 정렬하여 상위 10개의 데이터를 반환하는 함수입니다.
    '''

# 지정된 경로에 CSV 파일이 실제로 존재하는지 확인합니다.
    if not os.path.exists(csv_path):
        raise FileNotFoundError (f'csv 파일을 찾을 수 없습니다: {csv_path}')

    # Pandas를 사용하여 CSV 파일을 데이터프레임(표 형태)으로 읽어옵니다.
    df = pd.read_csv(csv_path)

# 조건 1: HScode가 '85'로 시작하는 데이터 (반도체류)
# 데이터를 정확히 비교하기 위해 문자열(str)로 변환하고 양옆의 공백을 제거(strip)합니다.
    df['hs_code_str'] = df['hs_code'].astype(str).str.strip()
    cond_hscode = df['hs_code_str'].str.startswith('85')

# 조건 2: 국가명이 '미국'이거나 '베트남'인 데이터
    cond_country = df['국가명'].isin(['미국', '베트남'])

# 조건 3: 수출금액이 0보다 큰 데이터 (유효한 수출 건만 추출)
    cond_amount = df['수출금액'] > 0

# 위에서 만든 3가지 조건을 모두 만족(&)하는 데이터만 필터링합니다.
    filtered_df = df[cond_hscode & cond_country & cond_amount]

# 수출금액을 기준으로 내림차순(ascending=False, 큰 값이 위로 오게) 정렬한 후, 상위 10개(head)만 추출합니다.
    top_10 = filtered_df.sort_values(by='수출금액', ascending=False).head(10)

# 필터링을 위해 임시로 만들었던 'hs_code_str' 열은 이제 필요 없으므로 삭제합니다.
    top_10 = top_10.drop(columns=['hs_code_str'])

    return top_10

def main():
# 현재 코드가 Streamlit(웹 대시보드) 환경에서 실행 중인지,
# 아니면 일반 터미널 환경에서 실행 중인지 확인합니다.
    try:
    is_streamlit = st.runtime.exists()
    except (ImportError, AttributeError):
is_streamlit = False