import streamlit as st
import groq
from groq import Groq
import os
import time

# ==========================================
# 1. 페이지 설정 & UI 디자인
# ==========================================
st.set_page_config(page_title="최준영 AI 비서", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        font-size: 13.5px !important;
        color: #1f2937;
        scroll-behavior: smooth;
    }

    .stApp { background-color: #f9fafb; }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 10px !important; 
        max-width: 600px; 
    }

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

    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0.5rem 0 !important;
        border: none !important;
    }

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
    
    [data-testid="stChatInput"] {
        padding-bottom: 10px !important; 
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 데이터 로드 및 초기 설정
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": resume_text},
        {"role": "assistant", "content": "안녕하세요👋\n\n시니어 IT 리더 최준영의 AI 면접 비서입니다.\n\n경력, 프로젝트 성과, 기술 역량 등 궁금한 점은 무엇이든 물어보세요. 위 버튼을 활용하시면 더 편리합니다."}
    ]

# 캐싱된 하드코딩 응답을 저장할 세션 변수 초기화
if "pending_hardcoded" not in st.session_state:
    st.session_state.pending_hardcoded = None

# ==========================================
# 3. 사전 정의된 답변(캐싱 데이터) - 토큰 소모 0!
# ==========================================
hardcoded_responses = {
    "btn1": {
        "q": "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘.",
        "a": "지원자 최준영의 핵심 증빙자료 및 포트폴리오 링크를 안내해 드립니다.\n\n| 문서/프로젝트 | 다운로드 및 접속 링크 |\n|---|---|\n| 📄 **웹 이력서 (Main)** | [https://realstoryjun.dothome.co.kr/resume](https://realstoryjun.dothome.co.kr/resume) |\n| 📊 **이력서 (PDF)** | [최준영_이력서 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/resume.pdf) |\n| 📝 **자기소개서 (PDF)** | [최준영_자기소개서 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Selfintroduction.pdf) |\n| 🎨 **포트폴리오 (PDF)** | [최준영_포트폴리오 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Portfolio.pdf) |\n| 🚀 **웹앱 (바리가자)** | [https://www.barigaja.co.kr/](https://www.barigaja.co.kr/) |\n| 🧠 **SaaS (Fasttrack2)** | [https://realstoryjun.dothome.co.kr/fasttrack2](https://realstoryjun.dothome.co.kr/fasttrack2) |"
    },
    "btn2": {
        "q": "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘.",
        "a": "✅ **에이치아이티(주) (2021.06 ~ 2025.05) 주요 성과**\n\n1. **인프라 고도화 (SLA 99.99%)**\n- 10G 광랜(SFP+) 3차 네트워크 고도화 및 Cisco L3 기반 VLAN 최적화\n- DB 서버 OS(Nvme)/Data 분리 구성 및 3중 자동 백업 체계 구축\n\n2. **정보보안 및 규정 확립**\n- 24년 SEMES 보안 평가 53개 항목 82.78점 획득 (전년 대비 상향)\n- 불법 SW 설치 원천 차단(화이트리스트) 및 방화벽 통제권한 자체 제어\n\n3. **전사 시스템(ERP) PM**\n- 영림원 ERP 전사 도입 총괄 및 다우오피스 그룹웨어 연동 구축\n- 전화교환기 자가 수리 등 핸즈온 트러블슈팅을 통한 즉각적인 현장 문제 해결"
    },
    "btn3": {
        "q": "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?",
        "a": "💰 **희망 연봉: 7,000 ~ 8,000만 원**\n\n이전 직장(에이치아이티)에서 주거 임차료 지원을 포함해 6,200만 원+알파의 처우를 받았으며, 13년간 꾸준히 몸값을 증명해 왔습니다. 단순한 관리형 리더가 아닌, 인프라 설계부터 보안, 최근의 AI 자동화 파이프라인까지 직접 구축하는 실무형 시니어로서 기업의 비용 절감에 즉각 기여할 수 있는 금액입니다.\n\n🏆 **독보적 강점: 토크 컨버터 (Talk Converter)**\n복잡한 인프라 트래픽이나 보안 로그 데이터를 디자인 툴(영상, 인포그래픽)로 시각화하여 비전문 경영진의 빠른 의사결정을 돕습니다. 아무리 좋은 기술도 표현할 수 없으면 쓸모가 없다는 신념 아래, 기술과 비즈니스를 잇는 역할을 수행합니다."
    },
    "btn4": {
        "q": "주로 다루는 인프라, 보안, 그리고 AI 관련 기술 스택을 정리해 줘.",
        "a": "🛠️ **핵심 기술 스택 요약**\n\n- **Infra / Network:** Cisco L3/L4 스위치, 10G SFP+ 광네트워크 구성, VLAN 최적화, 3중 백업(HA/DR) 아키텍처, 닷홈/Cloudflare 서버리스 환경 설정\n- **Security:** UTM L7 방화벽 튜닝, WAF, 망분리, Kaspersky ADV, SEMES 보안 컴플라이언스 대응, ERP NAC 적용\n- **AI / LLM:** 로컬 LLM(Qwen 3.5 70B 등) 기반 대용량 문서 분류 파이프라인 구축, RAG 환경 최적화, Vibe Coding 프롬프트 엔지니어링\n- **Design / Dev:** After Effects, Figma (IT 데이터 시각화), HTML/CSS, Python 기반 스크립팅 및 서비스 자동화"
    },
    "btn5": {
        "q": "단순한 엔지니어를 넘어 디자인과 AI를 융합하는 본인만의 차별화된 역량을 설명해 줘.",
        "a": "💡 **인프라 + 디자인 + AI = 1인 에이전시급 문제 해결력**\n\n1. **주경야독의 끈기:** 1학년 때부터 IDC 센터의 굉음 속에서 5년간 서버 구축 실무를 익혔습니다. 이후 타 부서와의 소통 한계를 극복하고자 '영상애니메이션 디자인'을 전공하며 주경야독했습니다.\n2. **시작한 일은 끝맺는다:** 바쁜 현업으로 늦어졌지만, 26년 8월 실무 논문으로 졸업을 마무리합니다.\n3. **비즈니스 가치 창출:** 인프라를 안정적으로 구축하는 데 그치지 않고, 그 데이터를 디자인으로 시각화하며, 최근에는 AI(로컬 LLM)를 활용해 대용량 로그를 자동 분류하는 SaaS(Fasttrack2)까지 직접 개발합니다. 인력이 부족한 조직에서도 홀로 프로젝트의 A to Z를 이끌 수 있습니다."
    }
}

# ==========================================
# 4. 헤더 및 퀵 메뉴 구성
# ==========================================
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 5px;">🤖 최준영 AI 면접 비서</h2>
    <p style="font-size: 14px; color: #6b7280; margin: 0;">
        <span style="color: #10b981; font-size: 11px;">●</span> 온라인 · 13년 경력 시니어 IT 리더
    </p>
</div>
<hr style="border: none; border-top: 1px solid #f3f4f6; margin-bottom: 25px;">
""", unsafe_allow_html=True)

# 버튼 로직: 클릭 시 사용자 메시지 추가 및 하드코딩 응답 대기상태로 전환
def handle_quick_question(btn_key):
    st.session_state.messages.append({"role": "user", "content": hardcoded_responses[btn_key]["q"]})
    st.session_state.pending_hardcoded = hardcoded_responses[btn_key]["a"]
    st.rerun() # 리런하여 메인 루프에서 AI처럼 출력하도록 함

if st.button("📄 증빙자료 링크"): handle_quick_question("btn1")
if st.button("🚀 핵심 프로젝트"): handle_quick_question("btn2")
if st.button("💰 연봉·강점"): handle_quick_question("btn3")
if st.button("🛠️ 기술 스택"): handle_quick_question("btn4")
if st.button("🏆 차별화 포인트"): handle_quick_question("btn5")

st.markdown("""
<div style="display: flex; align-items: center; margin: 30px 0;">
    <div style="flex-grow: 1; height: 1px; background-color: #e5e7eb;"></div>
    <span style="padding: 0 15px; color: #9ca3af; font-size: 12px; font-weight: 500;">대화 시작</span>
    <div style="flex-grow: 1; height: 1px; background-color: #e5e7eb;"></div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. 채팅 내역 렌더링
# ==========================================
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system": continue
    # 사용자 이모지는 👤, AI 비서는 🤖
    avatar_emoji = "👤" if msg["role"] == "user" else "🤖"
    
    with st.chat_message(msg["role"], avatar=avatar_emoji):
        if msg["role"] == "user":
            st.markdown(f'<div id="q-{i}"></div>', unsafe_allow_html=True)
        content = msg["content"].replace("\n", "  \n")
        st.markdown(content, unsafe_allow_html=True)
        if msg["role"] == "assistant" and i > 1:
            st.markdown(f'<a href="#q-{i-1}" class="back-link">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)

# 하단 텍스트 입력창
if prompt := st.chat_input("궁금한 점을 직접 질문하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.pending_hardcoded = None # 직접 입력 시 캐싱 비활성화
    st.rerun()

# ==========================================
# 6. 통합 AI 응답 생성 (가짜 스트리밍 + 진짜 AI 결합)
# ==========================================
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        
        message_placeholder = st.empty()
        
        # 📌 케이스 A: 버튼을 눌렀을 때 (API 소모 없이 가짜 스트리밍 생성)
        if st.session_state.pending_hardcoded:
            full_response = ""
            target_text = st.session_state.pending_hardcoded
            
            # 글자를 3글자씩 쪼개서 진짜 AI가 타이핑하는 것처럼 연출
            chunk_size = 3
            for i in range(0, len(target_text), chunk_size):
                full_response += target_text[i:i+chunk_size]
                message_placeholder.markdown(full_response.replace("\n", "  \n") + " ▌", unsafe_allow_html=True)
                time.sleep(0.01) # 미세한 딜레이
                
            message_placeholder.markdown(full_response.replace("\n", "  \n"), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.pending_hardcoded = None # 처리 완료 후 비우기
            
        # 📌 케이스 B: 직접 타자를 쳤을 때 (진짜 LLM 호출)
        else:
            loading_placeholder = st.empty()
            loading_placeholder.markdown(
                "<div style='text-align: center; color: #4b8bfc; font-size: 13px; font-weight: 500; padding: 15px; border-radius: 10px; background-color: #f0f8ff; margin-bottom: 10px;'>"
                "⏳ AI가 데이터를 심층 분석 중입니다...</div>", 
                unsafe_allow_html=True
            )
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=st.session_state.messages,
                    temperature=0.3,
                    stream=True
                )
                
                full_response = ""
                first_chunk_received = False
                
                for chunk in response:
                    if not first_chunk_received:
                        loading_placeholder.empty()
                        first_chunk_received = True
                        
                    token = chunk.choices[0].delta.content or ""
                    full_response += token
                    message_placeholder.markdown(full_response.replace("\n", "  \n") + " ▌", unsafe_allow_html=True)
                
                message_placeholder.markdown(full_response.replace("\n", "  \n"), unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except groq.RateLimitError:
                loading_placeholder.empty()
                st.warning("🚦 **서버 요청 제한 안내**\n\n현재 대기열이 많습니다. 1분 뒤 다시 시도해 주세요.")
                st.session_state.messages.pop() 
                
            except Exception as e:
                loading_placeholder.empty()
                st.error("알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
                st.session_state.messages.pop()
        
        # 완료 후 돌아가기 링크 추가
        st.markdown(f'<a href="#q-{len(st.session_state.messages)-1}" class="back-link">↑ 질문 위치로 이동</a>', unsafe_allow_html=True)

# ==========================================
# 7. 자동 스크롤 자바스크립트 (어떤 방식이든 무조건 하단 고정)
# ==========================================
st.components.v1.html("""
    <script>
        const scrollToBottom = () => {
            const chatContainer = window.parent.document.querySelector('.main');
            if (chatContainer) {
                chatContainer.scrollTo({
                    top: chatContainer.scrollHeight,
                    behavior: 'smooth'
                });
            }
        };
        scrollToBottom();
        setTimeout(scrollToBottom, 100); 
        setTimeout(scrollToBottom, 300); 
    </script>
""", height=0)
