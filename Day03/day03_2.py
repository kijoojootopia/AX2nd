"""
k-pop 데이터셋 기초 탐색
pandas  head/tail/shape/info/columns 를 사용해서 
데이터셋의 기본 정보를 화면에 순서대로 보여주는 streamlit 앱이다.
실행방법 : streamlit run day03_2.py 
"""

import io #input,output 약자
import pandas as pd
import streamlit as st

st.title("💄 이커머스 데이터셋 기초 탐색 ")
st.caption('pandas의 head/tail/shape/info/columns로 데이터셋 기본 정보를 확인합니다.')

#파일 업로드 하는 방식으로
upload_file = st.file_uploader("csv 파일을 직접 업로드 할 수 있습니다(선택사항)", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)
else :
    st.error('❌ 파일을 찾을 수 없습니다.')
    st.info('같은 경로에 파일을 업로드하거나 csv파일을 폴더에 넣고 새로고침 하세요.')
    df = None

if df is not None :
    st.subheader('1)head(): 데이터 상위 5행 미리보기')
    st.dataframe(df.head(), use_container_width=True)
    st.subheader('2)tail(): 데이터 하위 5행 미리보기')
    st.dataframe(df.tail(), use_container_width=True) # 기본행 5개
    
    st.subheader('3)shape(): 행 개수, 열개수') # 매트릭 이용(열 나누기)
    col1, col2 = st.columns(2)
    with col1 :
        st.metric("행 개수", f'{df.shape[0]}개')
    with col2 :
        st.metric("열 개수", f'{df.shape[1]}개')
    
    st.subheader('4)columns(): 전체 열(컬럼) 이름 목록') #필드 명 확인
    # st.write(df.columns) : 표 형식으로 보임
    st.write(list[str](df.columns)) # 리스트 형식으로 읽기 / []생략 가능

    st.subheader('5)info(): 각 열의 자료형과 결측치(NaN)여부 요약')

    info_df = pd.DataFrame({
        "타입" : df.dtypes,
        "결측치 아닌 개수" : df.notna().sum(),
        "결측치 개수" : df.isna().sum(),
        })
    st.dataframe(info_df, use_container_width=True)
    st.success('기초 정보 확인이 끝났습니다.')