import streamlit as st
import json
import time
from pathlib import Path

# ─────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="나의 소비 성향 테스트",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #ffecd2 100%);
    }
    /* 카드 스타일 */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    /* 헤더 배지 */
    .student-badge {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 999px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    /* 퀴즈 번호 */
    .q-number {
        background: #fcb69f;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 8px;
    }
    /* 결과 박스 */
    .result-box {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    /* 진행 텍스트 */
    .progress-text {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 캐싱: 퀴즈 데이터 로딩
# JSON 파일은 앱 실행 내내 변하지 않으므로,
# 매 렌더링마다 파일 I/O를 반복하지 않도록
# @st.cache_data 로 결과를 캐싱합니다.
# ─────────────────────────────────────────────
@st.cache_data
def load_quiz_data() -> dict:
    """퀴즈 JSON 파일을 읽고 파싱합니다. 결과는 캐싱됩니다."""
    data_path = Path(__file__).parent / "data" / "quiz_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────
# 사용자 DB (미리 정의된 계정)
# ─────────────────────────────────────────────
USERS = {
    "poodlecho": {"password": "poodle0223", "name": "조혜승"},
    "박규동": {"password": "1234", "name": "박규동"},
    "guest": {"password": "1234", "name": "게스트"},
}


# ─────────────────────────────────────────────
# 세션 초기화
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "step": "home",        # home | quiz1 | quiz2 | result
        "answers": {},
        "q1_idx": 0,
        "q2_idx": 0,
        "login_error": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session()


# ─────────────────────────────────────────────
# 공통: 학번 / 이름 배지 (모든 화면 상단)
# ─────────────────────────────────────────────
def render_student_info():
    st.markdown(
        '<div class="student-badge">🎓 학번: 2023204105 &nbsp;|&nbsp; 이름: 조혜승</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 화면 1: 홈 (로그인)
# ─────────────────────────────────────────────
def render_home():
    render_student_info()

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0'>
            <div style='font-size:3rem'>🛍️</div>
            <h1 style='margin:0.3rem 0'>나의 소비 성향 테스트</h1>
            <p style='color:#888'>충동 vs 계획 &nbsp;✕&nbsp; 가성비 vs 감성</p>
            <p style='color:#aaa; font-size:0.9rem'>
                8개의 질문으로 알아보는 나의 소비 DNA 🧬
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🔑 로그인")

    with st.form("login_form"):
        username = st.text_input("아이디", placeholder="아이디를 입력하세요")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.display_name = USERS[username]["name"]
            st.session_state.step = "quiz1"
            st.session_state.login_error = ""
            st.rerun()
        else:
            st.session_state.login_error = "❌ 아이디 또는 비밀번호가 올바르지 않습니다."

    if st.session_state.login_error:
        st.error(st.session_state.login_error)

    st.markdown(
        "<p style='color:#bbb; font-size:0.8rem; text-align:center'>"
        "테스트 계정: <b>guest</b> / <b>1234</b></p>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 화면 2 & 3: 퀴즈
# ─────────────────────────────────────────────
def render_quiz(axis_key: str, next_step: str):
    quiz_data = load_quiz_data()
    axis = quiz_data[axis_key]
    questions = axis["questions"]

    # 현재 진행 중인 질문 인덱스
    idx_key = "q1_idx" if axis_key == "axis1" else "q2_idx"
    idx = st.session_state[idx_key]

    # 축 구분 헤더
    render_student_info()
    st.markdown("---")

    name = st.session_state.get("display_name", "")
    st.markdown(f"👋 **{name}님, 안녕하세요!**")
    st.markdown("")

    axis_num = "1" if axis_key == "axis1" else "2"
    axis_label = axis["label"]
    total_q = len(questions)
    global_idx = idx if axis_key == "axis1" else idx + 4
    total_global = 8

    st.markdown(
        f'<p class="progress-text">PART {axis_num} · {axis_label} &nbsp;|&nbsp; '
        f'전체 {global_idx + 1} / {total_global} 문항</p>',
        unsafe_allow_html=True,
    )
    st.progress((global_idx + 1) / total_global)

    q = questions[idx]
    st.markdown(f"### Q{global_idx + 1}. {q['question']}")

    st.markdown("")
    choice = st.radio(
        "선택하세요",
        options=list(q["options"].keys()),
        format_func=lambda k: f"**{k}** — {q['options'][k]}",
        index=None,
        label_visibility="collapsed",
    )

    col_left, col_right = st.columns([1, 1])
    with col_right:
        if st.button("다음 →", use_container_width=True, disabled=(choice is None)):
            st.session_state.answers[q["id"]] = q["score"][choice]
            if idx + 1 < total_q:
                st.session_state[idx_key] += 1
            else:
                st.session_state.step = next_step
            st.rerun()

    if choice is None:
        st.caption("⬆️ 답변을 선택해야 다음으로 넘어갈 수 있어요!")


# ─────────────────────────────────────────────
# 결과 계산
# ─────────────────────────────────────────────
def calculate_result(answers: dict, quiz_data: dict) -> str:
    axis1_scores = [answers.get(i) for i in range(1, 5)]
    axis2_scores = [answers.get(i) for i in range(5, 9)]

    plan_count = axis1_scores.count("plan")
    value_count = axis2_scores.count("value")

    axis1_type = "plan" if plan_count >= 2 else "impulse"
    axis2_type = "value" if value_count >= 2 else "emotional"

    return f"{axis1_type}_{axis2_type}"


# ─────────────────────────────────────────────
# 화면 4: 결과
# ─────────────────────────────────────────────
def render_result():
    quiz_data = load_quiz_data()
    result_key = calculate_result(st.session_state.answers, quiz_data)
    result = quiz_data["results"][result_key]

    render_student_info()
    st.markdown("---")

    name = st.session_state.get("display_name", "")
    st.markdown(f"👋 **{name}님의 소비 성향 결과예요!**")
    st.markdown("")

    st.markdown(
        f"""
        <div class="result-box" style="background: linear-gradient(135deg, {result['color']}, #555);">
            <div style='font-size:4rem'>{result['emoji']}</div>
            <h2 style='margin:0.5rem 0'>{result['title']}</h2>
            <p style='font-size:1.1rem; margin:0'>{result['description']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"> {result['detail']}")

    st.markdown("---")

    # 축별 성향 상세 표시
    axis1_scores = [st.session_state.answers.get(i) for i in range(1, 5)]
    axis2_scores = [st.session_state.answers.get(i) for i in range(5, 9)]
    plan_pct = axis1_scores.count("plan") / 4 * 100
    value_pct = axis2_scores.count("value") / 4 * 100

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📅 계획 성향**")
        st.progress(int(plan_pct))
        st.caption(f"계획 {int(plan_pct)}% · 충동 {int(100-plan_pct)}%")
    with col2:
        st.markdown("**💰 가성비 성향**")
        st.progress(int(value_pct))
        st.caption(f"가성비 {int(value_pct)}% · 감성 {int(100-value_pct)}%")

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#aaa; font-size:0.85rem'>"
        "결과가 마음에 안 드시나요? 다시 도전해보세요! 😄</p>",
        unsafe_allow_html=True,
    )

    if st.button("🔄 다시 테스트하기", use_container_width=True):
        # 퀴즈 관련 상태만 초기화 (로그인 유지)
        st.session_state.step = "quiz1"
        st.session_state.answers = {}
        st.session_state.q1_idx = 0
        st.session_state.q2_idx = 0
        st.rerun()

    if st.button("🚪 로그아웃", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ─────────────────────────────────────────────
# 라우터
# ─────────────────────────────────────────────
def main():
    step = st.session_state.step

    if not st.session_state.logged_in or step == "home":
        render_home()
    elif step == "quiz1":
        render_quiz("axis1", next_step="quiz2")
    elif step == "quiz2":
        render_quiz("axis2", next_step="result")
    elif step == "result":
        render_result()


if __name__ == "__main__":
    main()
