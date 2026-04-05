import streamlit as st
from groq import Groq
import os

# ==========================================
# 1. 페이지 기본 설정 & 디자인 커스텀 (CSS)
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

# 스트림릿 기본 메뉴 숨기기 및 세련된 폰트/버튼 스타일 적용
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 버튼 스타일 디자인 */
    div.stButton > button:first-child {
        background-color: #f0f2f6;
        color: #0f1116;
        border: 1px solid #dcdcdc;
        border-radius: 20px;
        font-size: 14px;
        padding: 5px 15px;
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
# 2. 데이터 로드 및 초기화
# ==========================================
@st.cache_data
def load_resume_data():
    file_path = "resume.md"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "이력서 데이터를 불러올 수 없습니다."

resume_text = load_resume_data()

# API 클라이언트 (Secrets 사용)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 3. 화면 헤더 및 예상 질문 (퀵버튼)
# ==========================================
st.title("👨‍💻 IT 인프라/보안 리더 최준영 AI")
st.write("제 이력과 포트폴리오에 대해 무엇이든 물어보세요! (아래 버튼을 누르면 바로 질문할 수 있습니다)")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요! 13년 차 시니어 IT 전문가 최준영의 AI 비서입니다. 인프라 아키텍처, 정보보안, ERP 도입 등 궁금하신 점을 말씀해 주세요."}
    ]

# 예상 질문 버튼 레이아웃 (3열)
col1, col2, col3 = st.columns(3)
quick_question = None

if col1.button("🚀 주요 인프라/망분리 성과는?"):
    quick_question = "가장 자신 있는 주요 인프라 구축 및 망분리 성과에 대해 설명해 줘."
if col2.button("🛡️ 정보보안 및 평가 점수는?"):
    quick_question = "SEMES 정보보안 평가 대응 및 보안 구축 경험을 알려줘."
if col3.button("💰 희망 연봉과 그 근거는?"):
    quick_question = "희망하는 연봉 수준과 그렇게 생각하는 근거를 논리적으로 설명해 줘."

# ==========================================
# 4. 채팅 UI 및 로직
# ==========================================
# 이전 채팅 기록 화면에 출력 (아바타 아이콘 적용)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="👨‍💻"):
            st.markdown(msg["content"])

# 사용자 입력 처리 (직접 타이핑 OR 퀵버튼 클릭)
prompt = st.chat_input("질문을 입력해 주세요 (예: 10G 네트워크 구축 경험 알려줘)")
final_prompt = quick_question if quick_question else prompt

if final_prompt:
    # 1. 사용자 질문 출력
    with st.chat_message("user", avatar="👤"):
        st.markdown(final_prompt)
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # 2. AI 답변 생성 (한국어에 강한 Qwen 모델 추천)
    with st.chat_message("assistant", avatar="👨‍💻"):
        response = client.chat.completions.create(
            model="qwen/qwen3-32b", 
            messages=st.session_state.messages,
            temperature=0.3,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # 3. 답변 기록 저장
        st.session_state.messages.append({"role": "assistant", "content": answer})
