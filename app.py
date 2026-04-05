import streamlit as st
from groq import Groq
import os
import re
import time

# ==========================================
# 1. 페이지 설정 & 스크린샷 맞춤형 UI 디자인
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="👨‍💻", layout="centered")

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        font-size: 14px !important;
        color: #1f2937;
        scroll-behavior: smooth;
    }

    .stApp { background-color: #f9fafb; }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 120px !important; /* 하단 광고/입력창 안전 영역 */
        max-width: 600px; 
    }

    /* 퀵 버튼 스타일 */
    div.stButton { margin-bottom: -5px; }
    div.stButton > button:first-child {
        border-radius: 20px !important;
        border: 1px solid #e5e7eb !important;
        background-color: #ffffff !important;
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        padding: 0.35rem 1rem !important;
        width: fit-content !important; 
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        transition: all 0.2s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #4b8bfc !important;
        color: white !important;
        border-color: #4b8bfc !important;
    }

    /* 채팅 메시지 박스 */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0.5rem 0 !important;
        border: none !important;
    }
    
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
    
    /* 하단 입력창 고정 및 여백 */
    [data-testid="stChatInput"] {
        padding-bottom: 80px !important; 
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
# 4. 커스텀 헤더 및 퀵 메뉴 
# ==========================================
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 5px;">👨‍💻 최준영 AI 면접 비서</h2>
    <p style="font-size: 14px; color: #6b7280; margin: 0;">
        <span style="color: #10b981; font-size: 11px;">●</span> 온라인 · 13년 경력 시니어 IT 리더
    </p>
</div>
<hr style="border: none; border-top: 1px solid #f3f4f6; margin-bottom: 25px;">
""", unsafe_allow_html=True)

quick_q = None
if st.button("📄 증빙자료 링크"): quick_q = "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘."
if st.button("🚀 핵심 프로젝트"): quick_q = "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘."
if st.button("💰 연봉·강점"): quick_q = "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?"
if st.button("🛠️ 기술 스택"): quick_q = "주로 다루는 인프라, 보안, 그리고 AI 관련 기술 스택을 정리해 줘."
if st.button("🏆 차별화 포인트"): quick_q = "단순한 엔지니어를 넘어 디자인과 AI를 융합하는 본인만의 차별화된 역량을 설명해 줘."

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

# 질문 입력
prompt = st.chat_input("궁금한 점을 질문하세요")
final_p = quick_q if quick_q else prompt

if final_p:
    st.session_state.messages.append({"role": "user", "content": final_p})
    st.rerun()

# AI 응답 생성 (스트리밍 및 실시간 타이머 로직)
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="👨‍💻"):
        # UI 플레이스홀더(빈 공간) 미리 생성
        think_placeholder = st.empty()
        message_placeholder = st.empty()
        
        # 스트리밍 모드 활성화 (stream=True)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            temperature=0.3,
            stream=True
        )
        
        start_time = time.time()
        full_response = ""
        in_think_mode = False
        
        for chunk in response:
            token = chunk.choices[0].delta.content or ""
            full_response += token
            
            # AI가 <think> 태그 안에서 추론 중일 때
            if "<think>" in full_response and "</think>" not in full_response:
                in_think_mode = True
                elapsed = int(time.time() - start_time)
                # 초 단위로 움직이는 애니메이션 점(...) 구현
                dots = "." * ((int(time.time() * 2) % 3) + 1)
                
                # 실시간 로딩바 업데이트
                think_placeholder.markdown(
                    f"<div style='color: #8b5cf6; font-size: 13px; font-weight: 500; background: #ede9fe; padding: 6px 12px; border-radius: 8px; display: inline-block;'>"
                    f"🧠 AI가 이력서를 분석 중입니다{dots} ({elapsed}초 경과)</div>", 
                    unsafe_allow_html=True
                )
                
            # 추론이 끝나고 실제 답변이 나올 때
            elif "</think>" in full_response:
                if in_think_mode:
                    think_placeholder.empty() # 로딩바 숨기기
                    in_think_mode = False
                
                # </think> 이후의 텍스트만 추출해서 실시간 타이핑 효과 출력
                visible_text = full_response.split("</think>")[-1]
                # 실시간으로 화면이 자동 스크롤(추적)됨
                message_placeholder.markdown(visible_text.replace("\n", "  \n") + " ▌", unsafe_allow_html=True)
                
            else:
                # <think> 태그를 아예 사용하지 않는 모델의 경우
                visible_text = full_response
                message_placeholder.markdown(visible_text.replace("\n", "  \n") + " ▌", unsafe_allow_html=True)
        
        # 스트리밍 완료 후 최종 출력 (커서 ▌ 제거)
        final_clean_text = full_response.split("</think>")[-1] if "</think>" in full_response else full_response
        message_placeholder.markdown(final_clean_text.replace("\n", "  \n"), unsafe_allow_html=True)
        
        # 질문으로 이동 버튼 추가
        st.markdown(f'<a href="#q-{len(st.session_state.messages)-1}" class="back-link">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)
        
        # 세션에 최종 텍스트 저장
        st.session_state.messages.append({"role": "assistant", "content": final_clean_text})
        
        # 완전 완료 후 스크롤을 맨 밑에 고정
        st.components.v1.html("""
            <script>
                var body = window.parent.document.querySelector(".main");
                body.scrollTop = body.scrollHeight;
            </script>
        """, height=0)
