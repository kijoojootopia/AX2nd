# 로또
# random 모듈 이용해서 1~45 중 중복 없는 번호 6개를 뽑고
# 자료 구조 list => 중복 O / set => 중복 X : set 이용
# 자료 구조 set, 버튼을 누르면 5세트 한 번에 생성
# datetime 로 생성 시간 
# 숫자 중복 안됨, 정렬 작은 수, 색깔
# 로또v1
# fhEh
import streamlit as st
import random
from datetime import datetime
# datetime
st.title('🎱로또 번호 자동 생성기')
st.caption('버튼을 누르면 1~45 사이의 중복 없는 번호 6개 세트를 5개 만들어집니다.')
    
# 일을 다 마치면 숫자들을 네모 상자 목록(list)에 담아서 돌려줄 거야!"라는 뜻
def lotto_one_set() -> list : 
        """ 1~45에서 중복 없이 번호 6개 뽑아 정렬된 리스트로 반환"""

        number = set[int]()

        while len(number) <6 :
            number.add(random.randint(1,45)) # 1이상 45이하 정수 하나 뽑기
        return sorted(number)

st.markdown('---')
# 버튼 만들기 (버튼->if문)
if st.button("🍀5세트 번호 생성하기", key="widget_button"):
    # 생성시각 만들기
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"생성시각 : **{now_str}**")

    # 번호 대역별 색상 이모지 매핑 함수
    def get_ball_emoji(num: int) -> str:
        if num <= 10:
            return f"🟡 {num:02d}"  # 1 ~ 10: 노란 공
        elif num <= 20:
            return f"🔵 {num:02d}"  # 11 ~ 20: 파란 공
        elif num <= 30:
            return f"🔴 {num:02d}"  # 21 ~ 30: 빨간 공
        else:
            return f"⚪ {num:02d}"  # 31 ~ 45: 회색(흰색) 공

    # 반복문 생성

    for set_index in range(1,6): # 1~5: range 이상, 미만
        lotto_num = lotto_one_set() #리스트로 나온 함숫값=lotto_num
        # 각 숫자에 이모지를 붙이고 공백으로 연결
        #   for i in a: 리스트 a에 있는 원소를 하나씩 꺼내서 변수 i에 담는다.
        formatted_balls = "  ".join([get_ball_emoji(n) for n in lotto_num])
        # 번호 
        st.write(f"**{set_index}세트** : {formatted_balls}")
else:
    st.info("위 버튼을 누르면 행운의 로또 번호 5세트가 생성됩니다.")



