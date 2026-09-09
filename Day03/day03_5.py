# 인코딩 자동 감지 + 한글 폰트 막대 그래프
# 여러 인코딩('utf-8-sig,', 'cp949','euc-kr') 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실 등급 별 생존율 막대 그래프 생성 후 그림으로 저장 chart.png
# 실행 방법 : streamlit run day03_5.py

import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

st.title('📊인코딩 자동 감지 + 한글 폰트 막대 그래프 (Titanic 연습)')
st.caption('여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다.')

csv_path = os.path.join(os.path.dirname(__file__),"titanic_cleansed.csv")
# 직접 가져오기: csv_path = 'titanic_cleansed.csv'
font_path = os.path.join(os.path.dirname(__file__), "Eulyoo1945-Regular.otf")


# 인코딩 방법 - 함수 호출
def read_csv_with_auto_encoding(file_path):
    """
    utf-8-sig, cp949, euc-kr 순서대로 인코딩을 시도하여 
    CSV 파일을 안전하게 읽어오는 함수
    """
    encodings = ['utf-8-sig', 'cp949', 'euc-kr']
    
    for enc in encodings:
        try:
            # 지정된 인코딩으로 읽기 시도
            df = pd.read_csv(file_path, encoding=enc)
            st.write(f"성공: '{enc}' 인코딩으로 파일을 읽었습니다.")
            return df
        except UnicodeDecodeError:
            # 디코딩 에러가 나면 다음 인코딩으로 넘어감
            st.write(f"실패: '{enc}' 인코딩으로 읽기 실패, 다음 인코딩 시도...")
        except Exception as e:
            # 인코딩 외의 다른 에러(파일 경로 오류 등)는 바로 에러 발생시킴
            raise e
            
    # 모든 인코딩 시도가 실패할 경우
    raise UnicodeError("모든 인코딩 방식('utf-8-sig', 'cp949', 'euc-kr')으로도 파일을 읽을 수 없습니다.")


# 인코딩 자동 감지로 csv 읽기
st.subheader('1) 인코딩 자동 감지')
df = read_csv_with_auto_encoding(csv_path)

st.markdown('---')
# 객실등급(Pclass)별 생존율 집계
pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
# 엑셀 부분합처럼 정렬
# mean -> 그룹별 평균
st.dataframe((pclass_survival_rate *100).round(1).rename("생존율(%)"))

# df_df = st.dataframe((pclass_survival_rate * 100.round(1).rename('생존율(%)')
# st.write(df_df)

# 사망=0, 생존=1 등급 별 평균: Survived
# 생존 등급별 평균을 내면
# 그대로가 생존 비율이 된다. 생존/전체 30

# 차트그리기
st.markdown('---')
st.subheader('3) 객실 등급 별 생존율 막대 그래프')
try :
    # try: 맞을 때 실행 / 폰트 파일이 없으면 except문
    font_prop = font_manager.FontProperties(fname=font_path)
    # matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정
    # 전역(Global) 변수 / 지역(Local)변수
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    st.write('음유1945 폰트를 적용했습니다.')
except FileNotFoundError:
    st.warning('폰트 파일을 찾을 수 없습니다.')

# fig: 도화지 / ax: 그림 영역
fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate *100).plot(kind='bar', color='#006400', ax = ax)
ax.set_title('객실 등급별 생존율')
ax.set_xlabel('객실등급(Pclass)')
ax.set_ylabel('생존율(%)')

st.pyplot(fig)
# st.pyplot: 그래프를 스트림릿에 뿌리기

# 그림파일(PNG)로 저장(내보내기)
output_png = os.path.join(os.path.dirname(__file__), 'chart.png')
fig.savefig(output_png)
st.success('그림파일 저장 성공')