import streamlit as st
from groq import Groq
import os
import re

# ==========================================
# 1. 페이지 설정 & 컴팩트 UI 디자인 (60-70% 스케일)
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

# CSS를 통한 상세 UI 제어
st.markdown("""
<style>
    /* 전체 폰트 및 밀도 압축 (약 65% 수준) */
    html, body, [class*="css"] {
        font-size: 13px !important;
        scroll-behavior: smooth; /* 부드러운 스크롤 */
    }
    
    /* 상하단 여백 최소화 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important; /* 하단 입력창 여백 */
        max-width: 720px;
    }

    /* 문단 간격 최적화 */
    .stMarkdown p, .stMarkdown li {
        line-height: 1.4 !important;
        margin-bottom: 4px !important;
    }

    /* 퀵 버튼 디자인 */
    div.stButton > button:first-child {
        font-size: 11px !important;
        padding: 5px 10px !important;
        border-radius: 12px !important;
        border: 1px solid #4b8bfc;
        background-color: #f0f2f6;
        height: auto;
        width: 100%;
    }
    
    /* 채팅 메시지 박스 최적화 */
    [data-testid="stChatMessage"] {
        padding: 0.5rem 0.8rem !important;
        margin-bottom: 0.4rem !important;
        border-radius: 10px;
    }

    /* 답변 내 '질문으로 이동' 버튼 스타일 */
    .back-to-top {
        font-size: 11px;
        color: #4b8bfc;
        text-decoration: none;
        display: inline-block;
        margin-top: 8px;
        border: 1px solid #4b8bfc;
        padding: 2px 8px;
        border-radius: 5px;
    }
    
    /* 메뉴 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 및 경로 최적화
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
# 3. 세션 초기화 및 첫인사
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요! 13년 차 시니어 IT 전문가 최준영의 AI 비서입니다. 무엇을 도와드릴까요?"}
    ]

# ==========================================
# 4. 화면 헤더 및 퀵 버튼 (예상 질문)
# ==========================================
st.title("👨‍💻 최준영 AI 면접 비서")

col1, col2, col3 = st.columns(3)
quick_question = None

if col1.button("📄 모든 이력서/포트폴리오 링크"):
    quick_question = "지원자의 이력서, 자기소개서, 포트폴리오 및 각종 증빙자료 다운로드 링크를 일괄적으로 깔끔하게 정리해 줘."
if col2.button("🚀 주요 인프라/보안 성과"):
    quick_question = "10G 네트워크 고도화 및 SEMES 보안평가 대응 등 핵심 성과를 요약해 줘."
if col3.button("💰 연봉 조건 및 경쟁력"):
    quick_question = "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?"

# ==========================================
# 5. 채팅 인터페이스 & 로직
# ==========================================

# 대화 기록 출력
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system": continue
    
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "👨‍💻"):
        # 질문 시작 지점에 앵커(ID) 설정
        if msg["role"] == "user":
            st.markdown(f'<div id="question-{i}"></div>', unsafe_allow_html=True)
            
        st.markdown(msg["content"])
        
        # 답변 끝에 '질문으로 돌아가기' 버튼 추가
        if msg["role"] == "assistant" and i > 0:
            st.markdown(f'<a href="#question-{i-1}" class="back-to-top">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)

# 사용자 입력 처리
prompt = st.chat_input("질문을 입력하세요")
final_prompt = quick_question if quick_question else prompt

if final_prompt:
    # 사용자 질문 출력
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.rerun() # 화면 갱신을 통해 즉시 질문이 보이게 함

# AI 답변 생성 (마지막 메시지가 사용자일 때만 실행)
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="👨‍💻"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            temperature=0.3
        )
        raw_answer = response.choices[0].message.content
        clean_answer = re.sub(r'<think>.*?</think>', '', raw_answer, flags=re.DOTALL).strip()
        
        st.markdown(clean_answer)
        # 답변 하단에 돌아가기 버튼 (현재 인덱스 기준)
        q_idx = len(st.session_state.messages) - 1
        st.markdown(f'<a href="#question-{q_idx}" class="back-to-top">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": clean_answer})
        
        # 자동 스크롤 유도 (Streamlit 기본 동작 보완)
        st.components.v1.html("<script>window.scrollTo(0, document.body.scrollHeight);</script>", height=0)
