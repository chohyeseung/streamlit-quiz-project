# 🛍️ 나의 소비 성향 테스트

> 충동 vs 계획 × 가성비 vs 감성 — 2축으로 알아보는 나의 소비 DNA

**학번:** 2023204105  
**이름:** 조혜승

---

## 📋 프로젝트 소개

8개의 질문으로 나의 소비 성향을 두 축으로 분석합니다.

- **축 1:** 충동구매 ↔ 계획구매
- **축 2:** 가성비 소비 ↔ 감성 소비

결과는 4가지 유형 중 하나로 나옵니다:

| 유형 | 설명 |
|------|------|
| 💼 알뜰살뜰 엑셀 인간 | 계획형 + 가성비형 |
| 🌷 철저한 낭만주의자 | 계획형 + 감성소비형 |
| 🏹 할인 사냥꾼 | 충동구매형 + 가성비형 |
| 🎨 기분파 예술가 | 충동구매형 + 감성소비형 |

---

## 🚀 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/poodlecho/streamlit-quiz-project.git
cd streamlit-quiz-project
```

### 2. 가상환경 생성 (선택)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 이 자동으로 열립니다.

---

## 🔑 로그인 계정

| 아이디 | 비밀번호 |
|--------|---------|
| poodlecho | poodle0223 |
| guest | 1234 |

---

## 📁 프로젝트 구조

```
streamlit-quiz-project/
├── app.py                  # 메인 실행 파일
├── data/
│   └── quiz_data.json      # 퀴즈 문항 및 결과 데이터
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ 주요 기능

- **로그인 기능:** 사전 정의된 계정으로 로그인, 성공/실패 처리
- **캐싱 기능:** `@st.cache_data`로 quiz_data.json 파일 읽기를 캐싱 — 매 렌더링마다 파일 I/O 반복을 방지
- **퀴즈 기능:** 8문항 순차 진행, 선택 후 다음 이동, 최종 결과 및 성향 비율 표시
