초등학생도 바로 이해할 수 있도록 코드 한 줄마다 쉬운 설명을 주석(`#`)으로 달아두었습니다.

```python
# 1. 인터넷 화면(웹사이트)을 예쁘게 꾸며주는 도구 상자 'streamlit'을 가져와서 'st'라고 부를게!
import streamlit as st

# 2. 엑셀 표처럼 데이터를 착착 정리해주는 도구 상자 'pandas'를 가져와서 'pd'라고 부를게!
import pandas as pd

# 3. 컴퓨터 안의 파일 위치(길 찾기)를 도와주는 내비게이션 도구 상자 'os'를 가져올게!
import os

# 4. 내 컴퓨터 안에 숨겨진 CSV 파일(엑셀 같은 문서)이 어디 있는지 길을 찾아서 'csv_path'라는 이름표에 적어둬!
csv_path = os.path.join(os.path.dirname(__file__), "..", "common", "raw_trade_data.csv")

# 5. [다른 길 메모] 만약 파이썬 파일이랑 같은 방(폴더)에 있다면 이렇게 길을 찾을 수도 있어!
# csv_path = os.path.join(os.path.dirname(__file__), "raw_trade_data.csv")

# 6. 통화 이름, 가격, 어제보다 얼마나 변했는지를 이름표-내용 짝꿍(딕셔너리)으로 묶어둔 상자야!
exchange_data = {
    '통화' : ['USD','EUR','JPY(100엔)','CNY'],       # 나라별 돈 이름 목록
    '환율(KRW)' : [1399,1503,930,191],                # 우리나라 돈으로 얼마인지 적은 목록
    '전일대비' : [5200,3100,1000,400],                # 어제보다 얼마나 달라졌는지 적은 목록
}

# 7. 판다스 도구로 위 딕셔너리를 진짜 엑셀 네모 칸 표(데이터프레임)로 변신시켜서 'df_exchange'에 담아!
df_exchange = pd.DataFrame(exchange_data)

# 8. 인터넷 신문 맨 위에 가장 크고 굵은 왕 제목을 달아줘!
st.title('💱 오늘의 환율 대시보드')

# 9. 왕 제목 바로 아래에 작고 귀여운 글씨로 "진짜 돈 아니고 연습용이에요!" 하고 깨알 설명을 달아줘!
st.caption('아래 데이터는 실제 환율이 아닌 실습용 샘플 데이터입니다.')

# 10. 첫 번째 코너 시작을 알리는 중간 크기의 소제목을 써줘!
st.subheader('1) 환율 표 보기')

# 11. 화면에 일반 안내 글씨를 또박또박 적어줘!
st.write('▶ st.dataframe (상호작용 가능한 표)')

# 12. 마우스로 클릭해서 정렬하거나 크기를 조절할 수 있는 '움직이는 레고 표'를 화면 가득 넓게 띄워줘!
st.dataframe(df_exchange, use_container_width=True)

# 13. 이번엔 다른 스타일의 표를 보여주겠다고 글씨를 써줘!
st.write('▶ st.table (정적인 표)')

# 14. 움직이지 않고 사진처럼 얌전하게 딱 고정된 '기본 표'를 화면에 보여줘!
st.table(df_exchange)

# 15. 색연필로 자를 대고 선을 쫙 그어서 위 코너와 아래 코너를 깔끔하게 나눠줘!
st.markdown("---")

# 16. 두 번째 코너인 "중요 환율 모아보기" 소제목을 써줘!
st.subheader('2) 주요 환율 카드(st.metric)')

# 17. 도화지를 나란히 3칸(왼쪽 방, 가운데 방, 오른쪽 방)으로 똑같이 쪼개줘!
col1, col2, col3 = st.columns(3)

# 18. [첫 번째 방] 미국 달러(USD) 가격표를 달고, 어제보다 5.2 올랐다고 초록색 화살표를 띄워줘!
with col1:
    st.metric(label='USD/KRW', value='1450.5', delta="+5.2")

# 19. [두 번째 방] 유럽 유로(EUR) 가격표를 달고, 어제보다 3.1 떨어졌다고 빨간색 화살표를 띄워줘!
with col2:
    st.metric(label='EUR/KRW', value='1503.2', delta="-3.1")

# 20. [세 번째 방] 일본 엔화(JPY) 가격표를 달고, 어제보다 1.0 올랐다고 초록색 화살표를 띄워줘!
with col3:
    st.metric(label='JPY(100엔)/KRW', value='930.8', delta="+1.0")

# 21. 내용을 또 구분하기 위해 긴 줄을 쫙 그어줘!
st.markdown("---")

# 22. 세 번째 코너 소제목을 적어줘!
st.subheader('3) 환율 표 보기')

# 23. 컴퓨터 파일에서 꺼내온 진짜 데이터라고 설명 글을 적어줘!
st.write('공용 데이터 파일 raw_trade_data.csv를 읽어온 상위 5행입니다.')

# 24. 아까 찾아둔 길(csv_path)로 가서 엑셀 문서를 판다스로 쏙 읽어와 'df_trade_raw'에 담아!
df_trade_raw = pd.read_csv(csv_path, encoding='UTF-8')

# 25. 너무 기니까 맨 위에서 딱 5 줄(.head(5))만 잘라내서, 화면 가득 시원하게 표로 보여줘!
st.dataframe(df_trade_raw.head(5), use_container_width=True)

```