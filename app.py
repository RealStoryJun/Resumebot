import streamlit as st
from groq import Groq
import os
import re

# ==========================================
# 1. 페이지 설정 & 프로페셔널 UI 디자인 (컴팩트 & 모던)
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

st.markdown("""
<style>
    /* 1. 전체 톤앤매너 및 폰트 밀도 (70% 수준) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 13.5px !important;
        color: #333;
        scroll-behavior: smooth;
    }

    /* 2. 메인 컨테이너 여백 최적화 (스크린샷의 빈 여백 해결) */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important; /* 하단 입력창 공간 확보 */
        max-width: 650px;
    }

    /* 3. 메시지 버블 디자인 (심미성 강화) */
    [data-testid="stChatMessage"] {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 18px;
        padding: 0.8rem 1.1rem !important;
        margin-bottom: 0.6rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    
    /* 유저 메시지 배경 살짝 다르게 */
    [data-testid="stChatMessage"][data-testid="stChatMessage-user"] {
        background-color: #f8f9fa;
    }

    /* 4. 퀵 버튼 (칩 스타일) */
    div.stButton > button:first-child {
        font-size: 12px !important;
        font-weight: 500;
        background-color: #ffffff;
        color: #4b8bfc;
        border: 1.5px solid #4b8bfc;
        border-radius: 25px !important;
        padding: 6px 12px !important;
        transition: 0.2s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #4b8bfc;
        color: #ffffff;
    }

    /* 5. 질문 위치로 이동 버튼 (세련된 링크 형태) */
    .back-link {
        font-size: 11px;
        color: #888;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-top: 5px;
        padding: 4px 8px;
        border-radius: 4px;
        background: #f1f3f5;
    }

    /* 6. 입력창 위치 고정 및 가독성 */
    [data-testid="stChatInput"] {
        padding-bottom: 1.5rem;
    }
    
    /* 불필요한 요소 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (기존 로직 유지)
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
        {"role": "assistant", "content": "반갑습니다. 시니어 IT 리더 최준영의 AI 비서입니다. 무엇을 도와드릴까요?"}
    ]

# ==========================================
# 4. 헤더 및 퀵 메뉴 (링크 일괄 제공 포함)
# ==========================================
st.title("👨‍💻 최준영 AI 면접 비서")

c1, c2, c3 = st.columns(3)
quick_q = None
if c1.button("📄 증빙자료 일괄 확인"):
    quick_q = "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘."
if c2.button("🚀 핵심 프로젝트 성과"):
    quick_q = "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘."
if c3.button("💰 연봉 조건 및 역량"):
    quick_question = "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?"

# ==========================================
# 5. 채팅 인터페이스
# ==========================================
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system": continue
    
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "👨‍💻"):
        if msg["role"] == "user":
            st.markdown(f'<div id="q-{i}"></div>', unsafe_allow_html=True)
            
        # 줄바꿈 유지 출력
        content = msg["content"].replace("\n", "  \n")
        st.markdown(content, unsafe_allow_html=True)
        
        if msg["role"] == "assistant" and i > 1:
            st.markdown(f'<a href="#q-{i-1}" class="back-link">↑ 질문으로 돌아가기</a>', unsafe_allow_html=True)

# 질문 입력
prompt = st.chat_input("질문을 입력하세요")
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
        st.markdown(f'<a href="#q-{len(st.session_state.messages)-1}" class="back-link">↑ 질문으로 돌아가기</a>', unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": clean})
        
        # 하단 자동 스크롤
        st.components.v1.html("""
            <script>
                var body = window.parent.document.querySelector(".main");
                body.scrollTop = body.scrollHeight;
            </script>
        """, height=0)
