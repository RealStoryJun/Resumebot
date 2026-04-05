import streamlit as st
from groq import Groq

# 1. Groq 클라이언트 초기화
# (실제 배포 시에는 st.secrets에 키를 숨겨서 안전하게 관리합니다)
client = Groq(api_key="여기에_발급받은_GROQ_API_KEY_입력")

# 2. 내 이력서 컨텍스트 (시스템 프롬프트에 주입)
RESUME_CONTEXT = """
너는 IT 인프라/보안 직무에 지원하는 최준영의 AI 면접 비서야.
아래 정보를 바탕으로 채용 담당자의 질문에 전문적이고 친절하게 답변해줘.
모르는 내용은 지어내지 말고, 실제 면접에서 확인해달라고 유도해.

[이력서/포트폴리오 내용]
(여기에 도트홈 웹사이트에 있는 이력서 텍스트를 통째로 복사해서 붙여넣으세요)
"""

st.title("👨‍💻 지원자 최준영의 AI 챗봇 비서")
st.write("제 이력서와 포트폴리오에 대해 무엇이든 물어보세요!")

# 3. 채팅 기록 초기화 및 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": RESUME_CONTEXT},
        {"role": "assistant", "content": "안녕하세요! IT 인프라 담당자 최준영의 AI 비서입니다. 직무 경험이나 프로젝트에 대해 어떤 점이 궁금하신가요?"}
    ]

# 4. 이전 채팅 기록 화면에 출력 (시스템 프롬프트는 화면에서 숨김)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. 채용 담당자의 입력 처리
if prompt := st.chat_input("예: 주로 다뤄본 서버나 네트워크 장비는 무엇인가요?"):
    
    # 질문을 화면에 띄우고 기록에 추가
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Groq API 호출 (Gemma 모델 구동)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            # Groq에서 지원하는 최신 Gemma 오픈 모델 지정 (예: gemma-7b-it 등)
            model="gemma-7b-it", 
            messages=st.session_state.messages,
            temperature=0.3, # 면접용이므로 엉뚱한 소리를 하지 않도록 창의성(온도)을 낮춤
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # 답변을 기록에 추가
        st.session_state.messages.append({"role": "assistant", "content": answer})
