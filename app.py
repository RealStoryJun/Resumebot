import streamlit as st
from groq import Groq
import os

# ==========================================
# 1. 페이지 설정 및 디자인 (기존과 동일)
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.stButton > button:first-child {
        background-color: #f0f2f6;
        color: #0f1116;
        border: 1px solid #dcdcdc;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 (경로 및 대소문자 수정)
# ==========================================
@st.cache_data
def load_resume_data():
    # 파일명을 소문자 resume.md로 통일하거나 실제 파일명과 맞추세요.
    file_path = os.path.join(os.path.dirname(__file__), "resume.md") 
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # 파일 로드 실패 시 화면에 경고 표시
        return "파일을 찾을 수 없습니다. 깃허브의 파일명과 코드의 파일명이 일치하는지 확인하세요."

resume_text = load_resume_data()

# API 클라이언트
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 3. 화면 UI 및 세션 초기화
# ==========================================
st.title("👨‍💻 IT 인프라/보안 리더 최준영 AI")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요! 13년 3개월 경력의 시니어 IT 전문가 최준영의 AI 비서입니다. 무엇이든 물어보세요!"}
    ]

# 퀵버튼 섹션 (생략 - 기존 코드 유지)

# ==========================================
# 4. 채팅 로직 (모델 변경: openai/gpt-oss-20b)
# ==========================================
# (채팅 기록 출력 부분 생략)

if prompt := st.chat_input("질문을 입력해 주세요"):
    # 사용자 메시지 추가 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # AI 답변 생성
    with st.chat_message("assistant", avatar="👨‍💻"):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # 요청하신 모델로 변경
            messages=st.session_state.messages,
            temperature=0.3,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
