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

    /* ── 메인 컨테이너 ── */
    .block-container {
        max-width: 720px !important;
        padding: 0 1.5rem 7rem !important;
        margin: 0 auto;
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
        padding: 6px 14px !important;
        height: auto !important;
        line-height: 1.4 !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 1px 3px rgba(59, 91, 219, 0.08) !important;
        white-space: nowrap !important;
        cursor: pointer !important;
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

    /* ── 채팅 입력창 ── */
    .stChatInput {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 720px !important;
        background: #f7f8fc !important;
        padding: 12px 1.5rem 16px !important;
        border-top: 1px solid #e8eaf0 !important;
        z-index: 999 !important;
    }
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

    /* ── Streamlit 기본 요소 숨기기 ── */
    #MainMenu, footer, header, [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0 !important;
    }
    [data-testid="stDecoration"] { display: none !important; }

    /* ── 컬럼 간격 ── */
    [data-testid="column"] {
        padding: 0 4px !important;
    }

    /* ── 로딩 스피너 숨기기 ── */
    .stSpinner { display: none !important; }

    /* ── 반응형 ── */
    @media (max-width: 600px) {
        .block-container { padding: 0 1rem 7rem !important; }
        .stChatInput { padding: 10px 1rem 14px !important; }
        div.stButton > button { font-size: 11.5px !important; padding: 5px 11px !important; }
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
# 6. 퀵 질문 버튼 (버그 수정 완료)
# ==========================================
QUICK_QUESTIONS = {
    "📄 증빙자료 링크": "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘.",
    "🚀 핵심 프로젝트": "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘.",
    "💰 연봉·강점": "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?",
    "🛠️ 기술 스택": "보유한 기술 스택과 자격증을 상세히 알려줘.",
    "🏆 차별화 포인트": "다른 지원자 대비 최준영만의 차별화된 경쟁력을 설명해 줘.",
}

cols = st.columns(len(QUICK_QUESTIONS))
quick_q = None
for col, (label, question) in zip(cols, QUICK_QUESTIONS.items()):
    if col.button(label, use_container_width=False):
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
