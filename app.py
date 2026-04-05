import streamlit as st
from groq import Groq
import os
import re

# ==========================================
# 1. 페이지 기본 설정 & 디자인 커스텀 (CSS)
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

# 스트림릿 기본 UI 숨기기 및 세련된 버튼 스타일 적용
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 퀵 질문 버튼 스타일 */
    div.stButton > button:first-child {
        background-color: #f0f2f6;
        color: #0f1116;
        border: 1px solid #dcdcdc;
        border-radius: 20px;
        font-size: 13px;
        padding: 8px 16px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #4b8bfc;
        color: white;
        border-color: #4b8bfc;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 및 경로 최적화
# ==========================================
@st.cache_data
def load_resume_data():
    # 실행 파일 기준 절대 경로로 resume.md 참조 (대소문자 주의: resume.md)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "resume.md")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "지원자의 이력 데이터를 찾을 수 없습니다. 파일명을 확인해 주세요."

resume_text = load_resume_data()

# Groq API 클라이언트 초기화
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 3. 화면 헤더 및 예상 질문 (퀵버튼)
# ==========================================
st.title("👨‍💻 IT 인프라·보안 리더 최준영 AI")
st.write("13년 차 시니어 전문가 최준영의 이력과 역량에 대해 무엇이든 물어보세요.")

# 세션 상태 초기화 (시스템 프롬프트 주입)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요! 최준영의 AI 비서입니다. 인프라 구축 성과, 정보보안 대응력, 또는 희망 연봉에 대해 궁금하신 점이 있으신가요?"}
    ]

# 예상 질문 버튼 레이아웃 (3열 배치)
col1, col2, col3 = st.columns(3)
quick_question = None

if col1.button("🚀 주요 인프라 성과는?"):
    quick_question = "가장 자신 있는 주요 인프라 구축 및 망분리 성과에 대해 설명해 줘."
if col2.button("🛡️ 정보보안 대응 역량은?"):
    quick_question = "SEMES 정보보안 평가 대응 및 보안 체계 고도화 경험을 알려줘."
if col3.button("💰 연봉 조건과 채용 근거는?"):
    quick_question = "희망하는 연봉 수준과 13년 차 시니어로서의 채용 가치를 설명해 줘."

# ==========================================
# 4. 채팅 UI 및 핵심 로직
# ==========================================

# 이전 대화 기록 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="👨‍💻"):
            st.markdown(msg["content"])

# 사용자 입력 처리 (직접 입력 또는 퀵버튼)
prompt = st.chat_input("질문을 입력해 주세요")
final_prompt = quick_question if quick_question else prompt

if final_prompt:
    # 사용자 질문 화면 출력 및 저장
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_prompt)
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # AI 답변 생성
    with st.chat_message("assistant", avatar="👨‍💻"):
        try:
            # API 호출
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b", 
                messages=st.session_state.messages,
                temperature=0.3,
                max_tokens=1024
            )
            
            # 답변 파싱 및 <think> 태그 제거
            raw_answer = response.choices[0].message.content
            clean_answer = re.sub(r'<think>.*?</think>', '', raw_answer, flags=re.DOTALL).strip()
            
            # 최종 답변 출력 및 저장
            st.markdown(clean_answer)
            st.session_state.messages.append({"role": "assistant", "content": clean_answer})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
