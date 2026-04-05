import streamlit as st
from groq import Groq
import os
import re

# ==========================================
# 1. 페이지 설정 & 스크린샷 맞춤형 UI 디자인
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

st.markdown("""
<style>
    /* 🚀 하단 광고 배너 안전 영역(Safe Area) 확보 */
    [data-testid="stChatInput"] {
        padding-bottom: 80px !important; /* 광고창 높이에 맞춰 수치(80px)를 조절하세요 */
    }
    
    /* 채팅 내역이 입력창에 가려지지 않도록 메인 컨테이너 하단 여백도 같이 늘려줍니다 */
    .block-container {
        padding-bottom: 120px !important; 
    }

    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        font-size: 14px !important;
        color: #1f2937;
        scroll-behavior: smooth;
    }

    /* 배경색 및 여백 최적화 */
    .stApp {
        background-color: #f9fafb; /* 스크린샷과 유사한 아주 옅은 회색 배경 */
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 600px; /* 모바일/PC 통일감 있는 너비 */
    }

    /* 퀵 버튼 스타일 (스크린샷 완벽 구현) */
    div.stButton {
        margin-bottom: -5px; /* 버튼 사이 간격 좁히기 */
    }
    div.stButton > button:first-child {
        border-radius: 20px !important;
        border: 1px solid #e5e7eb !important;
        background-color: #ffffff !important;
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        padding: 0.35rem 1rem !important;
        width: fit-content !important; /* 글자 크기에 맞춰 너비 자동 조절 */
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        transition: all 0.2s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #4b8bfc !important;
        color: white !important;
        border-color: #4b8bfc !important;
    }

    /* 채팅 메시지 박스 (스크린샷 스타일) */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0.5rem 0 !important;
        border: none !important;
    }
    
    /* 메시지 내 아바타 크기 조절 */
    [data-testid="stChatMessage"] .st-emotion-cache-16idsys p {
        font-size: 1.5rem;
    }

    /* 질문으로 이동 링크 */
    .back-link {
        font-size: 12px;
        color: #6b7280;
        text-decoration: none;
        display: inline-block;
        margin-top: 8px;
        padding: 4px 10px;
        border-radius: 15px;
        border: 1px solid #d1d5db;
        background: #ffffff;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 
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
# 3. 채팅 세션 관리
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요👋\n\n시니어 IT 리더 최준영의 AI 면접 비서입니다.\n\n경력, 프로젝트 성과, 기술 역량 등 궁금한 점은 무엇이든 물어보세요. 위 버튼을 활용하시면 더 편리합니다."}
    ]

# ==========================================
# 4. 커스텀 헤더 및 퀵 메뉴 (스크린샷 디자인)
# ==========================================

# 1) 중앙 정렬 프로필
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 5px;">👨‍💻 최준영 AI 면접 비서</h2>
    <p style="font-size: 14px; color: #6b7280; margin: 0;">
        <span style="color: #10b981; font-size: 11px;">●</span> 온라인 · 13년 경력 시니어 IT 리더
    </p>
</div>
<hr style="border: none; border-top: 1px solid #f3f4f6; margin-bottom: 25px;">
""", unsafe_allow_html=True)

# 2) 좌측 정렬 둥근 버튼 5개
quick_q = None
if st.button("📄 증빙자료 링크"): quick_q = "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘."
if st.button("🚀 핵심 프로젝트"): quick_q = "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘."
if st.button("💰 연봉·강점"): quick_q = "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?"
if st.button("🛠️ 기술 스택"): quick_q = "주로 다루는 인프라, 보안, 그리고 AI 관련 기술 스택을 정리해 줘."
if st.button("🏆 차별화 포인트"): quick_q = "단순한 엔지니어를 넘어 디자인과 AI를 융합하는 본인만의 차별화된 역량을 설명해 줘."

# 3) '대화 시작' 구분선
st.markdown("""
<div style="display: flex; align-items: center; margin: 30px 0;">
    <div style="flex-grow: 1; height: 1px; background-color: #e5e7eb;"></div>
    <span style="padding: 0 15px; color: #9ca3af; font-size: 12px; font-weight: 500;">대화 시작</span>
    <div style="flex-grow: 1; height: 1px; background-color: #e5e7eb;"></div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 채팅 인터페이스
# ==========================================
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system": continue
    
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "👨‍💻"):
        if msg["role"] == "user":
            st.markdown(f'<div id="q-{i}"></div>', unsafe_allow_html=True)
            
        content = msg["content"].replace("\n", "  \n")
        st.markdown(content, unsafe_allow_html=True)
        
        if msg["role"] == "assistant" and i > 1:
            st.markdown(f'<a href="#q-{i-1}" class="back-link">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)

# 질문 입력 (가장 하단에 고정됨)
prompt = st.chat_input("궁금한 점을 질문하세요")
final_p = quick_q if quick_q else prompt

if final_p:
    st.session_state.messages.append({"role": "user", "content": final_p})
    st.rerun()

# AI 응답 생성
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="👨‍💻"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            temperature=0.3
        )
        raw = response.choices[0].message.content
        clean = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL).strip()
        
        st.markdown(clean.replace("\n", "  \n"), unsafe_allow_html=True)
        st.markdown(f'<a href="#q-{len(st.session_state.messages)-1}" class="back-link">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": clean})
        
        st.components.v1.html("""
            <script>
                var body = window.parent.document.querySelector(".main");
                body.scrollTop = body.scrollHeight;
            </script>
        """, height=0)
