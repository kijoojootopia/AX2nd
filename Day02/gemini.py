import streamlit as st
import random
from datetime import datetime

st.title('🎱 로또 번호 자동 생성기')
st.caption('버튼을 누르면 1~45 사이의 중복 없는 번호 6개 세트를 5개 만들어줍니다.')

# 1. 번호 대역별 색상 이모지 매핑 함수
def get_ball_emoji(num: int) -> str:
    if num <= 10:
        return f"🟡 {num:02d}"  # 1 ~ 10: 노란 공
    elif num <= 20:
        return f"🔵 {num:02d}"  # 11 ~ 20: 파란 공
    elif num <= 30:
        return f"🔴 {num:02d}"  # 21 ~ 30: 빨간 공
    elif num <= 40:
        return f"⚪ {num:02d}"  # 31 ~ 40: 회색(흰색) 공
    else:
        return f"🟢 {num:02d}"  # 41 ~ 45: 초록 공

# 2. 로또 1세트(6개) 생성 함수
def lotto_one_set() -> list:
    """1~45에서 중복 없이 번호 6개 뽑아 정렬된 리스트로 반환"""
    number = set()  # set[int]() 대신 set() 사용
    while len(number) < 6:
        number.add(random.randint(1, 45))
    return sorted(number)

st.markdown('---')

# 3. 버튼 클릭 이벤트 처리
if st.button("🍀 5세트 번호 생성하기", key="widget_button"):
    # 생성 시각 표시
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"생성시각 : **{now_str}**")
    
    # 5세트 반복 출력
    for set_index in range(1, 6):
        lotto_num = lotto_one_set()
        # 각 숫자에 이모지를 붙이고 공백으로 연결
        formatted_balls = "  ".join([get_ball_emoji(n) for n in lotto_num])
        st.write(f"**{set_index}세트** : {formatted_balls}")
else:
    st.info("위 버튼을 누르면 행운의 로또 번호 5세트가 생성됩니다.")