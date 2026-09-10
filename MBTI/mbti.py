import base64
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------------------
# 1. Streamlit 기본 환경 및 레이아웃 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="무역 직무 적합도 진단기 (Trade MBTI)",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------
# 2. 다크그린 테마 및 온글잎 콘콘체 폰트 Base64 인라인 인젝션
# ----------------------------------------------------
FONT_PATH = "온글잎 콘콘체.ttf"

font_css = ""
if os.path.exists(FONT_PATH):
    with open(FONT_PATH, "rb") as f:
        font_data = base64.b64encode(f.read()).decode("utf-8")
    font_css = f"""
    @font-face {{
        font-family: 'Ownglyph-Konkonche';
        src: url('data:font/truetype;base64,{font_data}') format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    """
else:
    # 폰트 파일이 아직 배치되지 않았을 경우 웹 폰트 Fallback 적용
    font_css = """
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    """

custom_style = f"""
<style>
{font_css}

html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, div, span {{
    font-family: 'Ownglyph-Konkonche', 'Pretendard', sans-serif !important;
}}

/* 메인 배경 및 텍스트 컬러 (Dark Green Theme) */
.stApp {{
    background-color: #F9FBF9;
    color: #081C15;
}}

/* 상단 헤더 배너 컨테이너 */
.header-box {{
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
    padding: 2.2rem 1.8rem;
    border-radius: 16px;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 14px rgba(27, 67, 50, 0.2);
}}
.header-box h1 {{
    color: #FFFFFF !important;
    font-size: 2.1rem;
    margin-bottom: 0.5rem;
}}
.header-box p {{
    color: #D8F3DC !important;
    font-size: 1.05rem;
    margin: 0;
}}

/* 문항 카드 컨테이너 */
.question-card {{
    background-color: #FFFFFF;
    border: 1px solid #D8F3DC;
    border-left: 5px solid #2D6A4F;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(27, 67, 50, 0.05);
}}
.question-title {{
    font-size: 1.08rem;
    font-weight: 600;
    color: #1B4332;
    margin-bottom: 0.8rem;
}}

/* 결과 박스 스타일 */
.result-card {{
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 1.8rem;
    border: 1.5px solid #2D6A4F;
    margin-top: 1.5rem;
    box-shadow: 0 4px 16px rgba(27, 67, 50, 0.1);
}}
.result-badge {{
    display: inline-block;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    background-color: #E8F5E9;
    color: #1B4332;
    font-weight: bold;
    font-size: 0.9rem;
    margin-bottom: 0.6rem;
}}
.job-title {{
    font-size: 1.8rem;
    font-weight: 700;
    color: #1B4332;
    margin-bottom: 0.3rem;
}}

/* 제출 버튼 스타일 */
div.stButton > button {{
    background-color: #1B4332 !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100%;
    box-shadow: 0 4px 10px rgba(27, 67, 50, 0.25);
    transition: all 0.2s ease-in-out;
}}
div.stButton > button:hover {{
    background-color: #2D6A4F !important;
    box-shadow: 0 6px 14px rgba(45, 106, 79, 0.35);
}}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# ----------------------------------------------------
# 3. 6대 직무 메타데이터 및 20개 진단 문항
# ----------------------------------------------------
JOBS_INFO = {
    "해외영업": {
        "en": "Overseas Sales",
        "keywords": ["도전성", "설득력", "대인관계", "성과지향"],
        "desc": "글로벌 신규 바이어 발굴, 가격 협상, 해외 전시회 참가 및 수출 계약 체결을 전담합니다.",
        "skills": "외국어 커뮤니케이션 능력, 협상력, 시장 탐색 센스, 적극적 영업 마인드",
    },
    "무역영업관리": {
        "en": "Trade Operations",
        "keywords": ["꼼꼼함", "정확성", "프로세스 준수", "안정성"],
        "desc": "수출입 선적 서류(B/L, C/I, P/L) 작성, L/C 검토, 납기 모니터링 및 바이어 CS를 담당합니다.",
        "skills": "서류 작성 및 검토 역량, 꼼꼼한 일정 관리, 대내외 커뮤니케이션, 무역 서식 이해도",
    },
    "물류/포워딩": {
        "en": "Logistics & Forwarding",
        "keywords": ["위기대처", "멀티태스킹", "상황판단", "효율추구"],
        "desc": "해상·항공 운송 루트 수배, 운임(Freight) 네고, 선적 스케줄 조율 및 입출고 관리를 총괄합니다.",
        "skills": "운송 루트 설계 역량, 운임 원가 분석력, 돌발 변수 대처력, 신속한 상황 판단",
    },
    "통관/관세": {
        "en": "Customs & Compliance",
        "keywords": ["준법정신", "규정분석", "원칙주의", "전문성"],
        "desc": "HS Code 품목 분류, FTA 원산지 판정 및 증명서 발급, 수출입 요건 충족 및 관세 환급을 담당합니다.",
        "skills": "관세법 및 무역 관계 법령 해석력, HS코드 분류 전문성, 꼼꼼한 증빙 관리",
    },
    "무역금융/외환": {
        "en": "Trade Finance & FX",
        "keywords": ["수리적 사고", "리스크 헷지", "시장분석", "신중함"],
        "desc": "신용장(L/C) 매입 및 개설, 외환 환리스크 관리(헤징), 무역보험 및 대금 회수를 체계적으로 관리합니다.",
        "skills": "거시경제 및 외환 지표 분석력, 재무 수치 분석, 금융 결제 규정(UCP600 등) 이해",
    },
    "소싱/구매": {
        "en": "Overseas Procurement",
        "keywords": ["분석력", "협상력", "품질감별", "끈기"],
        "desc": "해외 원자재 및 경쟁력 있는 공급업체 발굴, 단가 네고, 공정 품질 검수 및 공급망 안정화를 수행합니다.",
        "skills": "공급선 발굴 능력, 단가 협상력, 원가 분석력, 품질 검수 안목",
    },
}

QUESTIONS = [
    {"id": 1, "job": "해외영업", "text": "처음 보는 외국인 바이어나 고객에게 먼저 다가가 말을 건네는 것이 부담스럽지 않다."},
    {"id": 2, "job": "해외영업", "text": "목표 실적(매출)에 대한 압박이 있더라도, 성과를 냈을 때의 인센티브와 성취감이 더 크다."},
    {"id": 3, "job": "해외영업", "text": "기존에 정해진 틀을 따르기보다 새로운 해외 시장이나 거래처를 개척하는 일에 흥미를 느낀다."},
    {"id": 4, "job": "해외영업", "text": "단가 협상이나 조건 조율 시 상대방의 심리를 파악하고 설득하는 대화에 자신이 있다."},
    {"id": 5, "job": "무역영업관리", "text": "서류의 오탈자나 숫자 하나(금액, 수량 등)의 오류도 꼼꼼하게 찾아내는 편이다."},
    {"id": 6, "job": "무역영업관리", "text": "복잡한 규정이나 매뉴얼, 체크리스트에 따라 단계별로 일을 처리할 때 안정감을 느낀다."},
    {"id": 7, "job": "무역영업관리", "text": "계약 체결 이후 납기일까지의 전체 일정을 조율하고 챙기는 서포트 역할에 보람을 느낀다."},
    {"id": 8, "job": "물류/포워딩", "text": "예상치 못한 배편 지연, 결항 등 돌발 상황이 발생해도 빠르게 대안(우회 경로)을 찾아 해결한다."},
    {"id": 9, "job": "물류/포워딩", "text": "선사, 항공사, 창고 등 다양한 이해관계자 사이에서 일정과 단가를 실시간 조율하는 멀티태스킹이 편하다."},
    {"id": 10, "job": "물류/포워딩", "text": "지리와 지도, 글로벌 운송 경로를 살펴보며 효율적인 이동 동선을 짜는 것을 좋아한다."},
    {"id": 11, "job": "통관/관세", "text": "법률 조항, 품목 분류표, 협정문 등 전문적이고 학술적인 문서를 분석하는 데 거부감이 없다."},
    {"id": 12, "job": "통관/관세", "text": "'이 정도면 대충 넘어가도 되겠지'라는 식의 타협을 싫어하며 원칙과 컴플라이언스를 철저히 지킨다."},
    {"id": 13, "job": "통관/관세", "text": "제품의 세부 스펙과 재질을 파악해 정확한 카테고리(HS코드)로 분류하는 일에 흥미가 있다."},
    {"id": 14, "job": "무역금융/외환", "text": "환율 변동이나 금리 뉴스, 글로벌 거시경제 흐름을 주기적으로 챙겨보는 편이다."},
    {"id": 15, "job": "무역금융/외환", "text": "이익을 극대화하는 것보다 발생 가능한 금융 리스크와 대금 회수 위험을 사전에 차단하는 것이 더 중요하다."},
    {"id": 16, "job": "무역금융/외환", "text": "재무제표, 결제 조건(T/T, L/C, D/A, D/P 등), 숫자 데이터 분석에 거부감이 없다."},
    {"id": 17, "job": "소싱/구매", "text": "최저가 제품을 찾기 위해 여러 플랫폼과 공급처를 끈질기게 비교·분석하는 과정이 재미있다."},
    {"id": 18, "job": "소싱/구매", "text": "판매자(공급처)와의 가격 네고에서 밀리지 않고 우리가 원하는 마진율을 방어할 수 있다."},
    {"id": 19, "job": "소싱/구매", "text": "제품의 샘플 상태나 생산 공정의 품질 결함을 날카롭게 잡아내는 눈썰미가 있다."},
    {"id": 20, "job": "소싱/구매", "text": "완제품을 파는 것보다 경쟁력 있는 원자재나 좋은 부품을 발굴해 조달하는 것에 매력을 느낀다."},
]

SCALE_OPTIONS = [
    (1, "1: 전혀 아니다"),
    (2, "2: 대체로 아니다"),
    (3, "3: 보통이다"),
    (4, "4: 대체로 그렇다"),
    (5, "5: 매우 그렇다"),
]

# ----------------------------------------------------
# 4. 헤더 영역 구성
# ----------------------------------------------------
st.markdown(
    """
    <div class="header-box">
        <h1>무역 MBTI 검사</h1>
        <p>무역 6대 직무 적합도 진단기 · 20개 문항으로 찾는 나의 무역 커리어</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    본 진단은 글로벌 무역 밸류체인을 구성하는 **6대 핵심 직무(해외영업, 무역영업관리, 물류/포워딩, 통관/관세, 무역금융/외환, 소싱/구매)** 중  
    주인님의 업무 성향과 강점에 가장 부합하는 최적의 직무를 도출해 드립니다. 솔직하게 체크해 주십시오.
    """
)

# ----------------------------------------------------
# 5. 진단 폼 (20개 문항 렌더링)
# ----------------------------------------------------
with st.form("mbti_form"):
    answers = {}
    for item in QUESTIONS:
        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-title">Q{item['id']:02d}. {item['text']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        selected_val = st.radio(
            label=f"Q{item['id']} 응답 선택",
            options=[opt[0] for opt in SCALE_OPTIONS],
            format_func=lambda x: dict(SCALE_OPTIONS)[x],
            index=2,  # 기본값: 보통이다(3점)
            horizontal=True,
            key=f"q_{item['id']}",
            label_visibility="collapsed",
        )
        answers[item["id"]] = selected_val

    submit_button = st.form_submit_button(label="진단 결과 확인하기")

# ----------------------------------------------------
# 6. 결과 산출 및 시각화 (백분율 환산 알고리즘)
# ----------------------------------------------------
if submit_button:
    # 직무별 원점수 및 문항 수 집계
    raw_scores = {job: 0 for job in JOBS_INFO}
    question_counts = {job: 0 for job in JOBS_INFO}

    for item in QUESTIONS:
        job = item["job"]
        raw_scores[job] += answers[item["id"]]
        question_counts[job] += 1

    # 100점 환산 백분율 공식 적용
    converted_scores = {}
    for job in JOBS_INFO:
        min_possible = question_counts[job] * 1
        max_possible = question_counts[job] * 5
        score_pct = ((raw_scores[job] - min_possible) / (max_possible - min_possible)) * 100
        converted_scores[job] = round(score_pct, 1)

    # 득점 순위 정렬
    sorted_jobs = sorted(converted_scores.items(), key=lambda x: x[1], reverse=True)
    first_job, first_score = sorted_jobs[0]
    second_job, second_score = sorted_jobs[1]

    st.markdown("---")
    st.subheader("📊 직무 적합도 종합 진단 결과")

    # 1순위 추천 직무 카드
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-badge">1순위 최적 추천 직무 (적합도 {first_score}%)</div>
            <div class="job-title">{first_job} ({JOBS_INFO[first_job]['en']})</div>
            <p style="color: #2D6A4F; font-size: 1.05rem; margin-top: 0.5rem;">
                <b>핵심 키워드:</b> {' · '.join(JOBS_INFO[first_job]['keywords'])}
            </p>
            <p style="margin-top: 0.8rem; line-height: 1.6; color: #081C15;">
                {JOBS_INFO[first_job]['desc']}
            </p>
            <p style="margin-top: 0.6rem; color: #555555; font-size: 0.95rem;">
                <b>요구 역량:</b> {JOBS_INFO[first_job]['skills']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2순위 서브 직무 카드
    st.markdown(
        f"""
        <div style="background-color: #F0F7F4; border-radius: 12px; padding: 1.2rem 1.4rem; margin-top: 1rem; border-left: 4px solid #2D6A4F;">
            <span style="font-weight: bold; color: #1B4332;">2순위 서브 시너지 직무:</span> 
            <b>{second_job} ({JOBS_INFO[second_job]['en']})</b> (적합도 {second_score}%)<br/>
            <span style="font-size: 0.95rem; color: #333333;">{JOBS_INFO[second_job]['desc']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------------------------------
    # 7. Radar Chart 시각화 (Plotly)
    # ----------------------------------------------------
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("#### 6대 직무 역량 밸런스 차트")

    categories = list(converted_scores.keys())
    values = list(converted_scores.values())

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            fillcolor="rgba(45, 106, 79, 0.35)",
            line=dict(color="#1B4332", width=2.5),
            marker=dict(size=6, color="#1B4332"),
            name="적합도 (%)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color="#1B4332"),
                gridcolor="#E0E0E0",
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="#1B4332", family="Ownglyph-Konkonche, sans-serif"),
                gridcolor="#D8F3DC",
            ),
            bgcolor="#FAFAFA",
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=30, b=30),
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # 8. 점수 상세 비교 테이블
    # ----------------------------------------------------
    score_df = pd.DataFrame(
        [
            {
                "순위": f"{idx + 1}위",
                "직무명": job,
                "영문명": JOBS_INFO[job]["en"],
                "적합도 점수": f"{score}%",
                "원점수": f"{raw_scores[job]} / {question_counts[job] * 5}점",
            }
            for idx, (job, score) in enumerate(sorted_jobs)
        ]
    )
    st.dataframe(score_df, use_container_width=True, hide_index=True)