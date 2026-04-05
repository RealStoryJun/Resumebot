import streamlit as st
from groq import Groq
import os
import re

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="최준영 AI 비서",
    page_icon="👨‍💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 전체 CSS - ChatGPT 스타일 (완전 검증된 선택자)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600&display=swap');

    /* ── 전역 기본값 ── */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif !important;
        font-size: 14px;
        color: #1a1a2e;
    }

    /* ── 배경 ── */
    .stApp {
        background: #f7f8fc;
    }

    /* ── 헤더 영역 ── */
    .app-header {
        text-align: center;
        padding: 2rem 0 1.2rem;
        border-bottom: 1px solid #e8eaf0;
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
        margin: 0 !important;
        letter-spacing: -0.3px;
    }
    .app-header p {
        color: #6b7280 !important;
        font-size: 13px !important;
        margin: 6px 0 0 !important;
    }
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── 퀵 버튼 칩 ── */
    .quick-chips {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
        justify-content: center;
    }
    
    div.stButton > button {
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        background: #ffffff !important;
        color: #3b5bdb !important;
        border: 1.5px solid #d0d9ff !important;
        border-radius: 999px !important;
        padding: 6px 10px !important;
        height: auto !important;
        line-height: 1.4 !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 1px 3px rgba(59, 91, 219, 0.08) !important;
        white-space: nowrap !important;
        cursor: pointer !important;
        width: 100% !important;        /* 컨테이너 가득 채우기 */
        margin-bottom: 6px !important; /* 행 간격 */
    }
    div.stButton > button:hover {
        background: #3b5bdb !important;
        color: #ffffff !important;
        border-color: #3b5bdb !important;
        box-shadow: 0 3px 10px rgba(59, 91, 219, 0.25) !important;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* ── 채팅 메시지 공통 ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.2rem 0 !important;
        margin-bottom: 0 !important;
        gap: 10px !important;
    }

    /* ── 사용자 메시지 버블 ── */
    [data-testid="stChatMessage"][aria-label*="user"] .stMarkdown,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
        background: #3b5bdb;
        color: #ffffff !important;
        border-radius: 18px 18px 4px 18px;
        padding: 10px 16px !important;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(59, 91, 219, 0.2);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p,
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown * {
        color: #ffffff !important;
    }

    /* ── AI 메시지 버블 ── */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
        background: #ffffff;
        color: #1a1a2e !important;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px !important;
        max-width: 90%;
        margin-right: auto;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
        border: 1px solid #eaecf0;
        line-height: 1.7;
    }

    /* ── 아바타 아이콘 크기 ── */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        width: 32px !important;
        height: 32px !important;
        font-size: 16px !important;
        border-radius: 50% !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #3b5bdb, #7c3aed) !important;
    }
    [data-testid="chatAvatarIcon-user"] {
        background: #e8eaf6 !important;
    }

    /* ── 채팅 입력창 내부 스타일 ── */
    .stChatInput > div {
        background: #ffffff !important;
        border: 1.5px solid #dde1ef !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stChatInput > div:focus-within {
        border-color: #3b5bdb !important;
        box-shadow: 0 0 0 3px rgba(59, 91, 219, 0.12) !important;
    }
    .stChatInput textarea {
        font-family: 'Noto Sans KR', sans-serif !important;
        font-size: 14px !important;
        color: #1a1a2e !important;
        padding: 12px 16px !important;
    }
    .stChatInput textarea::placeholder {
        color: #9ca3af !important;
    }

    /* ── 구분선 ── */
    .msg-divider {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1rem 0;
        color: #c8ccd8;
        font-size: 11px;
    }
    .msg-divider::before, .msg-divider::after {
        content: '';
        flex: 1;
        border-top: 1px solid #e8eaf0;
    }

    /* ── 타이핑 인디케이터 ── */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 12px 16px;
        background: #ffffff;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #eaecf0;
        width: fit-content;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
    .typing-indicator span {
        width: 7px; height: 7px;
        background: #9ca3af;
        border-radius: 50%;
        animation: bounce 1.2s infinite;
    }
    .typing-indicator span:nth-child(2) { animation-delay: 0.15s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-6px); opacity: 1; }
    }

    /* ── Streamlit 크롬 전부 숨기기 ── */
    #MainMenu,
    footer,
    header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"],
    .stDeployButton,
    .viewerBadge_container__1QSob,
    [title="Manage app"],
    [title="View app in Streamlit Community Cloud"],
    iframe[title="streamlit_cloud_status_icon"],
    .streamlit-footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        pointer-events: none !important;
    }

    /* ── 채팅 입력창 - 모바일 safe-area 대응 ── */
    .stChatInput {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 720px !important;
        background: #f7f8fc !important;
        /* iOS Safari 하단 home indicator 여백 자동 확보 */
        padding: 10px 1.5rem calc(14px + env(safe-area-inset-bottom, 0px)) !important;
        border-top: 1px solid #e8eaf0 !important;
        z-index: 900 !important;
    }

    /* ── 플로팅 네비게이션 버튼 (좌측 고정) ── */
    .float-nav {
        position: fixed !important;
        left: 14px !important;
        bottom: calc(130px + env(safe-area-inset-bottom, 0px)) !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 9px !important;
        z-index: 9999 !important;
    }
    .fab {
        width: 42px !important;
        height: 42px !important;
        border-radius: 50% !important;
        border: none !important;
        background: #ffffff !important;
        color: #3b5bdb !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.13), 0 0 0 1.5px #dde1ef !important;
        font-size: 17px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.18s ease !important;
        -webkit-tap-highlight-color: transparent !important;
    }
    .fab:hover, .fab:active {
        transform: scale(1.12) !important;
        box-shadow: 0 4px 16px rgba(59,91,219,0.22) !important;
    }
    .fab-ai {
        background: linear-gradient(135deg, #3b5bdb, #7c3aed) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 10px rgba(59,91,219,0.3) !important;
    }

    /* ── 본문 하단 여백 (입력창 + 브라우저 네비바 확보) ── */
    .block-container {
        max-width: 720px !important;
        /* 12rem = ~168px: 입력창 70px + 브라우저바 49px + 여유분 */
        padding: 0 1.5rem calc(12rem + env(safe-area-inset-bottom, 0px)) !important;
        margin: 0 auto;
    }

    /* ── 컬럼 간격 최소화 (버튼 그리드) ── */
    [data-testid="column"] {
        padding: 0 3px !important;
        min-width: 0 !important;   /* 모바일 찌그러짐 방지 */
    }

    /* ── 버튼 텍스트 말줄임 방지 ── */
    div.stButton > button span {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: block !important;
    }

    /* ── 로딩 스피너 숨기기 ── */
    .stSpinner { display: none !important; }

    /* ── 반응형 (모바일) ── */
    @media (max-width: 600px) {
        .block-container {
            padding: 0 0.8rem calc(13rem + env(safe-area-inset-bottom, 0px)) !important;
        }
        .stChatInput {
            padding: 8px 0.8rem calc(14px + env(safe-area-inset-bottom, 0px)) !important;
        }
        div.stButton > button {
            font-size: 11px !important;
            padding: 5px 6px !important;
            letter-spacing: -0.2px !important;
        }
        .float-nav { left: 8px !important; }
        .fab { width: 36px !important; height: 36px !important; font-size: 14px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 데이터 로드
# ==========================================
@st.cache_data
def load_resume_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "resume.md")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "데이터를 찾을 수 없습니다."

resume_text = load_resume_data()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 4. 세션 초기화
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {
            "role": "assistant",
            "content": "안녕하세요 👋\n\n**시니어 IT 리더 최준영**의 AI 면접 비서입니다.\n\n경력, 프로젝트 성과, 기술 역량 등 궁금한 점을 무엇이든 물어보세요. 아래 빠른 질문 버튼을 활용하셔도 됩니다."
        }
    ]

# ==========================================
# 5. 헤더
# ==========================================
st.markdown("""
<div class="app-header">
    <h1>👨‍💻 최준영 AI 면접 비서</h1>
    <p><span class="status-dot"></span>온라인 · 13년 경력 시니어 IT 리더</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5-1. 플로팅 네비게이션 버튼 (좌측 고정, HTML only - script는 component로)
# ==========================================
st.markdown("""
<div class="float-nav" id="float-nav">
    <button class="fab" id="fab-top" title="최상단으로">⬆</button>
    <button class="fab fab-ai" id="fab-ai" title="마지막 AI 답변으로">🤖</button>
    <button class="fab" id="fab-bottom" title="최하단으로">⬇</button>
</div>
""", unsafe_allow_html=True)

# JS는 component iframe으로 주입 (window.parent로 부모 DOM 접근)
st.components.v1.html("""
<script>
(function attachFAB() {
    var pd = window.parent.document;

    function getScroll() {
        return pd.querySelector('[data-testid="stAppViewBlockContainer"]')
            || pd.querySelector('[data-testid="stVerticalBlock"]')
            || pd.querySelector('.main')
            || pd.documentElement;
    }

    function goTop() {
        var el = getScroll();
        el.scrollTo({ top: 0, behavior: 'smooth' });
        window.parent.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function goBottom() {
        var el = getScroll();
        el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
        window.parent.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }

    function goLastAI() {
        var msgs = pd.querySelectorAll('[data-testid="stChatMessage"]');
        var lastAI = null;
        for (var i = 0; i < msgs.length; i++) {
            if (msgs[i].querySelector('[data-testid="chatAvatarIcon-assistant"]')) {
                lastAI = msgs[i];
            }
        }
        if (lastAI) lastAI.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function tryBind() {
        var top = pd.getElementById('fab-top');
        var ai  = pd.getElementById('fab-ai');
        var bot = pd.getElementById('fab-bottom');
        if (!top || !ai || !bot) {
            setTimeout(tryBind, 300);
            return;
        }
        top.addEventListener('click', goTop);
        ai.addEventListener('click', goLastAI);
        bot.addEventListener('click', goBottom);
    }

    tryBind();
})();
</script>
""", height=0)

# ==========================================
# 6. 퀵 질문 버튼 (버그 수정 완료)
# ==========================================
QUICK_QUESTIONS = [
    ("📄 증빙자료",   "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘."),
    ("🚀 프로젝트",   "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘."),
    ("💰 연봉·강점",  "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?"),
    ("🛠️ 기술스택",  "보유한 기술 스택과 자격증을 상세히 알려줘."),
    ("🏆 차별화",     "다른 지원자 대비 최준영만의 차별화된 경쟁력을 설명해 줘."),
]

quick_q = None

# 1행: 3개
row1 = st.columns(3)
for i, col in enumerate(row1):
    label, question = QUICK_QUESTIONS[i]
    if col.button(label, use_container_width=True, key=f"qb_{i}"):
        quick_q = question

# 2행: 2개 (중앙 정렬용 padding 컬럼 포함)
_, c1, c2, _ = st.columns([0.5, 2, 2, 0.5])
for i, col in enumerate([c1, c2]):
    label, question = QUICK_QUESTIONS[3 + i]
    if col.button(label, use_container_width=True, key=f"qb_{3 + i}"):
        quick_q = question

# ==========================================
# 7. 채팅 메시지 렌더링
# ==========================================
st.markdown('<div class="msg-divider">대화 시작</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "👨‍💻"):
        st.markdown(msg["content"])

# ==========================================
# 8. 입력 처리 및 AI 응답
# ==========================================
prompt = st.chat_input("궁금한 점을 질문하세요...")
final_prompt = quick_q if quick_q else prompt

if final_prompt:
    # 사용자 메시지 저장 & 표시
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_prompt)

    # AI 응답 생성
    with st.chat_message("assistant", avatar="👨‍💻"):
        # 타이핑 인디케이터
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
        """, unsafe_allow_html=True)

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                temperature=0.3,
                stream=False
            )
            raw = response.choices[0].message.content
            # <think> 태그 제거
            clean = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        except Exception as e:
            clean = f"⚠️ 응답 생성 중 오류가 발생했습니다: {str(e)}"

        typing_placeholder.empty()
        st.markdown(clean)

    st.session_state.messages.append({"role": "assistant", "content": clean})

    # 자동 스크롤 (Streamlit 내 작동 방식)
    st.components.v1.html("""
        <script>
            setTimeout(() => {
                const main = window.parent.document.querySelector('[data-testid="stVerticalBlock"]');
                if (main) main.scrollTop = main.scrollHeight;
                window.parent.scrollTo(0, window.parent.document.body.scrollHeight);
            }, 100);
        </script>
    """, height=0)