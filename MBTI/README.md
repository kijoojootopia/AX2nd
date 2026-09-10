# 🧭 Trade Job Fit Assessment (무역 직무 MBTI)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-2d5a27?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.28+-1e3d1b?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Theme-Dark%20Green-1b4332?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-40916c?style=flat-square"/>
</div>

<br/>

<div style="font-family: '온글잎 콘콘체', sans-serif; color: #1b4332; line-height: 1.8;">

> **Trade MBTI (무역 직무 적합도 진단)** 는 무역 분야 취업 준비생 및 실무자를 위해 기획된 Streamlit 기반 인터랙티브 직무 적합도 진단 웹 애플리케이션입니다.  
> 20개의 핵심 진단 문항을 통해 개인의 성향과 역량을 정량적으로 분석하고, 가장 높은 일치도를 보이는 **6대 무역 직무**를 매칭하여 최적의 커리어 패스를 제안합니다.

</div>

---

## 📌 목차 (Table of Contents)

- [1. 프로젝트 개요](#-1-프로젝트-개요)
- [2. 6대 핵심 무역 직무 정의](#-2-6대-핵심-무역-직무-정의)
- [3. 진단 문항 체계 (20문항)](#-3-진단-문항-체계-20문항)
- [4. 알고리즘 및 집계 로직](#-4-알고리즘-및-집계-로직)
- [5. 화면 구성 및 UI/UX 가이드](#-5-화면-구성-및-uiux-가이드)
- [6. 설치 및 실행 방법](#-6-설치-및-실행-방법)
- [7. 프로젝트 디렉토리 구조](#-7-프로젝트-디렉토리-구조)

---

## 🎯 1. 프로젝트 개요

- **프로젝트명**: Trade Job Fit Assessment (무역 직무 MBTI 진단기)
- **개발 환경**: Python, Streamlit, Plotly, Pandas
- **디자인 테마**: 다크 그린 (Dark Green, `#1B4332`, `#2D6A4F`, `#081C15`)
- **지정 폰트**: 온글잎 콘콘체 (`Ownglyph-Konkonche.ttf`)
- **진단 방식**: 5점 리커트 척도 (1: 전혀 아니다 ~ 5: 매우 그렇다), 총 20문항

---

## 💼 2. 6대 핵심 무역 직무 정의

무역 밸류체인 전반을 포괄하는 핵심 6대 직무를 기반으로 진단합니다.

| 직무명 | 영문 표기 | 핵심 미션 및 주요 역할 | 추천 성향 키워드 |
| :--- | :--- | :--- | :--- |
| **해외영업** | Overseas Sales | 글로벌 신규 바이어 발굴, 가격 협상, 해외 전시회 참가, 수출 계약 체결 | 도전성, 설득력, 대인관계, 성과지향 |
| **무역영업관리** | Trade Operations | 수출입 선적 서류(B/L, C/I, P/L) 작성, L/C 검토, 납기 모니터링, 고객 CS | 꼼꼼함, 정확성, 프로세스 준수, 안정성 |
| **물류/포워딩** | Logistics & Forwarding | 해상·항공 운송 루트 수배, 운임(Freight) 네고, 스케줄 조율, 입출고 관리 | 위기대처, 멀티태스킹, 상황판단, 효율추구 |
| **통관/관세** | Customs & Compliance | HS Code 품목 분류, FTA 원산지 판정 및 증명서 발급, 수입 요건 및 관세 환급 | 준법정신, 규정분석, 원칙주의, 전문성 |
| **무역금융/외환** | Trade Finance & FX | 신용장(L/C) 매입 및 개설, 외환 환리스크 관리(헤징), 무역보험 및 대금 회수 | 수리적 사고, 리스크 헷지, 시장분석, 신중함 |
| **소싱/구매** | Overseas Procurement | 해외 원자재/공급업체 발굴, 공급 단가 네고, 공정 품질 검수, 공급망 안정화 | 분석력, 협상력, 품질감별, 끈기 |

---

## 📝 3. 진단 문항 체계 (20문항)

각 직무별 3~4개 핵심 역량 문항으로 구성되어 있으며, 5점 리커트 척도로 응답합니다.

### 🔹 해외영업 (Overseas Sales - 4문항)
* **Q01.** 처음 보는 외국인 바이어나 고객에게 먼저 다가가 말을 건네는 것이 부담스럽지 않다.
* **Q02.** 목표 실적(매출)에 대한 압박이 있더라도, 성과를 냈을 때의 인센티브와 성취감이 더 크다.
* **Q03.** 기존에 정해진 틀을 따르기보다 새로운 해외 시장이나 거래처를 개척하는 일에 흥미를 느낀다.
* **Q04.** 단가 협상이나 조건 조율 시 상대방의 심리를 파악하고 설득하는 대화에 자신이 있다.

### 🔹 무역영업관리/수출입업무 (Trade Operations - 3문항)
* **Q05.** 서류의 오탈자나 숫자 하나(금액, 수량 등)의 오류도 꼼꼼하게 찾아내는 편이다.
* **Q06.** 복잡한 규정이나 매뉴얼, 체크리스트에 따라 단계별로 일을 처리할 때 안정감을 느낀다.
* **Q07.** 계약 체결 이후 납기일까지의 전체 일정을 조율하고 챙기는 서포트 역할에 보람을 느낀다.

### 🔹 물류/포워딩 (Logistics & Forwarding - 3문항)
* **Q08.** 예상치 못한 배편 지연, 결항 등 돌발 상황이 발생해도 빠르게 대안(우회 경로)을 찾아 해결한다.
* **Q09.** 선사, 항공사, 창고 등 다양한 이해관계자 사이에서 일정과 단가를 실시간 조율하는 멀티태스킹이 편하다.
* **Q10.** 지리와 지도, 글로벌 운송 경로를 살펴보며 효율적인 이동 동선을 짜는 것을 좋아한다.

### 🔹 통관/관세 (Customs & Compliance - 3문항)
* **Q11.** 법률 조항, 품목 분류표, 협정문 등 전문적이고 학술적인 문서를 분석하는 데 거부감이 없다.
* **Q12.** "이 정도면 대충 넘어가도 되겠지"라는 식의 타협을 싫어하며 원칙과 컴플라이언스를 철저히 지킨다.
* **Q13.** 제품의 세부 스펙과 재질을 파악해 정확한 카테고리(HS코드)로 분류하는 일에 흥미가 있다.

### 🔹 무역금융/외환 (Trade Finance & FX - 3문항)
* **Q14.** 환율 변동이나 금리 뉴스, 글로벌 거시경제 흐름을 주기적으로 챙겨보는 편이다.
* **Q15.** 이익을 극대화하는 것보다 발생 가능한 금융 리스크와 대금 회수 위험을 사전에 차단하는 것이 더 중요하다.
* **Q16.** 재무제표, 결제 조건(T/T, L/C, D/A, D/P 등), 숫자 데이터 분석에 거부감이 없다.

### 🔹 소싱/구매 (Overseas Procurement - 4문항)
* **Q17.** 최저가 제품을 찾기 위해 여러 플랫폼과 공급처를 끈질기게 비교·분석하는 과정이 재미있다.
* **Q18.** 판매자(공급처)와의 가격 네고에서 밀리지 않고 우리가 원하는 마진율을 방어할 수 있다.
* **Q19.** 제품의 샘플 상태나 생산 공정의 품질 결함을 날카롭게 잡아내는 눈썰미가 있다.
* **Q20.** 완제품을 파는 것보다 경쟁력 있는 원자재나 좋은 부품을 발굴해 조달하는 것에 매력을 느낀다.

---

## ⚙️ 4. 알고리즘 및 집계 로직

문항 수가 직무별로 3문항(15점 만점) 또는 4문항(20점 만점)으로 상이하므로, 공정한 비교를 위해 **100점 환산 백분율(Score Percentage)** 공식을 적용합니다.

$$	ext{환산 점수}(\%) = \left( rac{	ext{해당 직무 응답 점수 합계} - 	ext{최소 가능 점수}}{	ext{최대 가능 점수} - 	ext{최소 가능 점수}} ight) 	imes 100$$

* **1순위 (Primary Fit)**: 백분율 최고 득점 직무
* **2순위 (Secondary Fit)**: 차순위 득점 직무 (복합 직무 시너지 분석)
* **밸런스 시각화**: Plotly Radar Chart(방사형 레이더 차트)로 6각형 역량 분포 출력

---

## 🎨 5. 화면 구성 및 UI/UX 가이드

### 🌿 컬러 팔레트 (Dark Green Theme)
| 용도 | 색상 코드 | 프리뷰 |
| :--- | :--- | :--- |
| **Primary Accent** | `#1B4332` | 다크 포레스트 그린 (헤더, 주요 버튼, 강조) |
| **Secondary Accent** | `#2D6A4F` | 미디엄 그린 (차트 라인, 서브 헤딩) |
| **Card Background** | `#E8F5E9` | 소프트 민트 그린 (문항 컨테이너, 카드 박스) |
| **Background** | `#F9FBF9` | 오프화이트/페일 그린 (전체 배경) |
| **Text Dark** | `#081C15` | 딥 흑록색 (본문 기본 텍스트) |

### 🖋️ 폰트 설정 (Streamlit CSS 커스텀)
프로젝트 내 `assets/fonts/Ownglyph-Konkonche.ttf` 폰트를 앱 전체에 적용합니다.

```css
@font-face {
    font-family: 'Ownglyph-Konkonche';
    src: url('assets/fonts/Ownglyph-Konkonche.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
    font-family: 'Ownglyph-Konkonche', sans-serif !important;
}
```

---

## 🚀 6. 설치 및 실행 방법

### 1) 저장소 클론 및 가상환경 설정
```bash
git clone https://github.com/your-username/trade-job-mbti.git
cd trade-job-mbti
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2) 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 3) 폰트 파일 배치
`Ownglyph-Konkonche.ttf` 파일을 `assets/fonts/` 폴더 내에 배치합니다.

### 4) Streamlit 앱 실행
```bash
streamlit run app.py
```

---

## 📁 7. 프로젝트 디렉토리 구조

```text
trade-job-mbti/
├── assets/
│   └── fonts/
│       └── Ownglyph-Konkonche.ttf    # 지정 폰트 (온글잎 콘콘체)
├── .streamlit/
│   └── config.toml                    # 다크그린 테마 기본 설정
├── app.py                             # Streamlit 메인 실행 스크립트
├── questions.py                       # 20문항 데이터 및 가중치 매핑
├── logic.py                           # 점수 집계 및 MBTI 유형 도출 로직
├── requirements.txt                   # 의존성 라이브러리 목록
└── README.md                          # 프로젝트 문서
```

---
<div align="center">
  <sub>Developed for Global Trade Career Exploration · Designed with Dark Green Palette</sub>
</div>
