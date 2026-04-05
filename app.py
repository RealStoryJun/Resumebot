<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>최준영 AI 비서</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-color: #ffffff;
            --chat-bg: #f9fafb;
            --primary: #4b8bfc;
            --text-color: #1f2937;
            --border-color: #e5e7eb;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body, html { 
            margin: 0; padding: 0; height: 100%; 
            font-family: 'Pretendard', -apple-system, sans-serif; background-color: var(--bg-color);
            color: var(--text-color); overflow: hidden;
        }

        .main-wrapper {
            display: flex; flex-direction: column; height: 100vh;
            max-width: 600px; margin: 0 auto; position: relative;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }

        /* 헤더 (app.py 디자인 적용) */
        .header {
            padding: 20px 20px 15px; border-bottom: 1px solid var(--border-color);
            background: white; text-align: center; z-index: 10;
        }
        .header h1 { margin: 0 0 5px 0; font-size: 22px; font-weight: 800; color: #111827; }
        .header p { margin: 0; font-size: 14px; color: #6b7280; }
        .status-dot { color: #10b981; font-size: 11px; }

        /* 대화창 영역 */
        .chat-view { flex: 1; overflow-y: auto; padding: 0; scroll-behavior: smooth; background: var(--bg-color); }

        /* 초기 퀵 버튼 영역 */
        .suggestion-area { padding: 30px 20px; text-align: center; }
        .suggestion-grid {
            display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 15px;
        }
        .suggestion-btn {
            border-radius: 20px; border: 1px solid var(--border-color); background-color: white;
            color: #374151; font-weight: 500; font-size: 13.5px; padding: 8px 16px;
            cursor: pointer; transition: all 0.2s; font-family: inherit;
        }
        .suggestion-btn:hover { background-color: var(--primary); color: white; border-color: var(--primary); }

        .divider { display: flex; align-items: center; margin: 20px 20px; }
        .divider::before, .divider::after { content: ''; flex: 1; border-bottom: 1px solid var(--border-color); }
        .divider span { padding: 0 15px; color: #9ca3af; font-size: 12px; font-weight: 500; }

        /* 메시지 버블 */
        .msg-row { padding: 20px; display: flex; flex-direction: column; gap: 8px; }
        .msg-row.assistant { background-color: var(--chat-bg); border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); }
        
        .msg-header { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: 15px; margin-bottom: 4px; }
        .msg-text { font-size: 14.5px; line-height: 1.6; word-break: break-word; color: #374151; }
        
        /* 🚨 마크다운 표(Table) 완벽 렌더링 스타일 */
        .msg-text table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13.5px; }
        .msg-text th, .msg-text td { border: 1px solid var(--border-color); padding: 10px; text-align: left; }
        .msg-text th { background-color: #f3f4f6; font-weight: 600; }
        .msg-text a { color: var(--primary); text-decoration: none; font-weight: 500; }
        .msg-text a:hover { text-decoration: underline; }
        .msg-text p { margin: 0 0 10px 0; }
        .msg-text p:last-child { margin-bottom: 0; }
        .msg-text ul, .msg-text ol { margin: 10px 0; padding-left: 20px; }

        /* 하단 고정 입력창 */
        .bottom-nav { padding: 15px 20px; background: white; border-top: 1px solid var(--border-color); padding-bottom: max(15px, env(safe-area-inset-bottom)); }
        .input-group {
            display: flex; background: #f3f4f6; border-radius: 24px; padding: 5px 5px 5px 15px; align-items: center;
        }
        .input-group input {
            flex: 1; border: none; background: transparent; font-size: 14.5px; outline: none; font-family: inherit;
        }
        .send-btn {
            background: var(--primary); color: white; border: none; border-radius: 50%;
            width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
            cursor: pointer; font-size: 16px; transition: background 0.2s;
        }
        .send-btn:disabled { background: #9ca3af; cursor: not-allowed; }

        .back-link {
            font-size: 12px; color: #6b7280; display: inline-block; margin-top: 12px;
            padding: 4px 12px; border-radius: 15px; border: 1px solid #d1d5db; background: #ffffff;
            cursor: pointer; user-select: none; width: fit-content;
        }
        .back-link:hover { background-color: #f3f4f6; }

        #streamLoading { display: none; text-align: center; color: var(--primary); font-size: 13px; font-weight: 500; padding: 15px; background: #f0f8ff; margin: 10px 20px; border-radius: 10px; }
    </style>
</head>
<body>

<div class="main-wrapper">
    <div class="header">
        <h1>🤖 최준영 AI 면접 비서</h1>
        <p><span class="status-dot">●</span> 온라인 · 13년 경력 시니어 IT 리더</p>
    </div>

    <div class="chat-view" id="chatView">
        
        <div id="initialScreen">
            <div class="suggestion-area">
                <div class="suggestion-grid">
                    <button class="suggestion-btn" onclick="askQuick('btn1')">📄 증빙자료 링크</button>
                    <button class="suggestion-btn" onclick="askQuick('btn2')">🚀 핵심 프로젝트</button>
                    <button class="suggestion-btn" onclick="askQuick('btn3')">💰 연봉·강점</button>
                    <button class="suggestion-btn" onclick="askQuick('btn4')">🛠️ 기술 스택</button>
                    <button class="suggestion-btn" onclick="askQuick('btn5')">🏆 차별화 포인트</button>
                </div>
            </div>
            <div class="divider"><span>대화 시작</span></div>
        </div>

        <div id="chatFlow">
            <div class="msg-row assistant">
                <div class="msg-header">🤖 AI 비서</div>
                <div class="msg-text">안녕하세요👋<br><br>시니어 IT 리더 최준영의 AI 면접 비서입니다.<br><br>경력, 프로젝트 성과, 기술 역량 등 궁금한 점은 무엇이든 물어보세요. 위 버튼을 활용하시면 더 편리합니다.</div>
            </div>
        </div>
        <div id="streamLoading">⏳ AI가 데이터를 심층 분석 중입니다...</div>
    </div>

    <div class="bottom-nav">
        <form class="input-group" id="chatForm" onsubmit="handleUserSubmit(event)">
            <input type="text" id="queryInput" placeholder="궁금한 점을 직접 질문하세요" autocomplete="off">
            <button type="submit" class="send-btn" id="sendBtn">↑</button>
        </form>
    </div>
</div>

<script>
    // 마크다운 파서 줄바꿈 설정 (Streamlit과 동일하게)
    marked.setOptions({ breaks: true });

    // 워커 주소 연결
    const WORKER_URL = "https://resumebot.god8night.workers.dev";
    let systemPrompt = "";
    let messages = [];

    // 📂 app.py와 동일하게 resume.md 로드
    async function initSystem() {
        try {
            const res = await fetch('resume.md');
            const resumeContent = await res.text();
            systemPrompt = `너는 IT 인프라 및 정보보안 직무에 지원하는 13년 3차 시니어 IT 전문가 '최준영'을 대변하는 AI 면접 비서야.
아래 제공된 나의 이력서 데이터를 완벽히 숙지하고, 채용 담당자의 질문에 전문적이고 자신감 있게 답변해.

--- 이력서 데이터 ---
${resumeContent}
------------------`;
        } catch (e) { console.error("이력서 로드 실패"); }
    }
    initSystem();

    // 📝 app.py의 hardcoded_responses 데이터 완벽 이식
    const quickData = {
        "btn1": { q: "이력서, 자기소개서, 포트폴리오 및 모든 증빙자료 링크를 표 형태로 깔끔하게 정리해 줘.", a: "지원자 최준영의 핵심 증빙자료 및 포트폴리오 링크를 안내해 드립니다.\n\n| 문서/프로젝트 | 다운로드 및 접속 링크 |\n|---|---|\n| 📄 **웹 이력서 (Main)** | [https://realstoryjun.dothome.co.kr/resume](https://realstoryjun.dothome.co.kr/resume) |\n| 📊 **이력서 (PDF)** | [최준영_이력서 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/resume.pdf) |\n| 📝 **자기소개서 (PDF)** | [최준영_자기소개서 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Selfintroduction.pdf) |\n| 🎨 **포트폴리오 (PDF)** | [최준영_포트폴리오 다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Portfolio.pdf) |\n| 🚀 **웹앱 (바리가자)** | [https://www.barigaja.co.kr/](https://www.barigaja.co.kr/) |\n| 🧠 **SaaS (Fasttrack2)** | [https://realstoryjun.dothome.co.kr/fasttrack2](https://realstoryjun.dothome.co.kr/fasttrack2) |" },
        "btn2": { q: "10G 고도화 및 ERP 도입 등 주요 인프라 구축 성과를 요약해 줘.", a: "✅ **에이치아이티(주) (2021.06 ~ 2025.05) 주요 성과**\n\n1. **인프라 고도화 (SLA 99.99%)**\n- 10G 광랜(SFP+) 3차 네트워크 고도화 및 Cisco L3 기반 VLAN 최적화\n- DB 서버 OS(Nvme)/Data 분리 구성 및 3중 자동 백업 체계 구축\n\n2. **정보보안 및 규정 확립**\n- 24년 SEMES 보안 평가 53개 항목 82.78점 획득 (전년 대비 상향)\n- 불법 SW 설치 원천 차단(화이트리스트) 및 방화벽 통제권한 자체 제어\n\n3. **전사 시스템(ERP) PM**\n- 영림원 ERP 전사 도입 총괄 및 다우오피스 그룹웨어 연동 구축\n- 전화교환기 자가 수리 등 핸즈온 트러블슈팅을 통한 즉각적인 현장 문제 해결" },
        "btn3": { q: "희망 연봉 수준과 13년 경력의 시니어로서 가지는 독보적인 강점이 뭐야?", a: "💰 **희망 연봉: 7,000 ~ 8,000만 원**\n\n이전 직장(에이치아이티)에서 주거 임차료 지원을 포함해 6,200만 원+알파의 처우를 받았으며, 13년간 꾸준히 몸값을 증명해 왔습니다. 단순한 관리형 리더가 아닌, 인프라 설계부터 보안, 최근의 AI 자동화 파이프라인까지 직접 구축하는 실무형 시니어로서 기업의 비용 절감에 즉각 기여할 수 있는 금액입니다.\n\n🏆 **독보적 강점: 토크 컨버터 (Talk Converter)**\n복잡한 인프라 트래픽이나 보안 로그 데이터를 디자인 툴(영상, 인포그래픽)로 시각화하여 비전문 경영진의 빠른 의사결정을 돕습니다. 아무리 좋은 기술도 표현할 수 없으면 쓸모가 없다는 신념 아래, 기술과 비즈니스를 잇는 역할을 수행합니다." },
        "btn4": { q: "주로 다루는 인프라, 보안, 그리고 AI 관련 기술 스택을 정리해 줘.", a: "🛠️ **핵심 기술 스택 요약**\n\n- **Infra / Network:** Cisco L3/L4 스위치, 10G SFP+ 광네트워크 구성, VLAN 최적화, 3중 백업(HA/DR) 아키텍처, 닷홈/Cloudflare 서버리스 환경 설정\n- **Security:** UTM L7 방화벽 튜닝, WAF, 망분리, Kaspersky ADV, SEMES 보안 컴플라이언스 대응, ERP NAC 적용\n- **AI / LLM:** 로컬 LLM(Qwen 3.5 70B 등) 기반 대용량 문서 분류 파이프라인 구축, RAG 환경 최적화, Vibe Coding 프롬프트 엔지니어링\n- **Design / Dev:** After Effects, Figma (IT 데이터 시각화), HTML/CSS, Python 기반 스크립팅 및 서비스 자동화" },
        "btn5": { q: "단순한 엔지니어를 넘어 디자인과 AI를 융합하는 본인만의 차별화된 역량을 설명해 줘.", a: "💡 **인프라 + 디자인 + AI = 1인 에이전시급 문제 해결력**\n\n1. **주경야독의 끈기:** 1학년 때부터 IDC 센터의 굉음 속에서 5년간 서버 구축 실무를 익혔습니다. 이후 타 부서와의 소통 한계를 극복하고자 '영상애니메이션 디자인'을 전공하며 주경야독했습니다.\n2. **시작한 일은 끝맺는다:** 바쁜 현업으로 늦어졌지만, 26년 8월 실무 논문으로 졸업을 마무리합니다.\n3. **비즈니스 가치 창출:** 인프라를 안정적으로 구축하는 데 그치지 않고, 그 데이터를 디자인으로 시각화하며, 최근에는 AI(로컬 LLM)를 활용해 대용량 로그를 자동 분류하는 SaaS(Fasttrack2)까지 직접 개발합니다. 인력이 부족한 조직에서도 홀로 프로젝트의 A to Z를 이끌 수 있습니다." }
    };

    function scrollChat() {
        const view = document.getElementById('chatView');
        view.scrollTo({ top: view.scrollHeight, behavior: 'smooth' });
    }

    function addBackLink(container, index) {
        const up = document.createElement('div');
        up.className = 'back-link';
        up.innerText = '↑ 질문 위치로 이동';
        up.onclick = () => document.getElementById(`idx-${index}`).scrollIntoView({behavior: 'smooth', block: 'start'});
        container.appendChild(up);
    }

    function appendBubble(role, content, index = null) {
        // 대화 시작 시 초기 메뉴 숨김 (app.py 구조 반영)
        document.getElementById('initialScreen').style.display = 'none';
        
        const flow = document.getElementById('chatFlow');
        const row = document.createElement('div');
        row.className = `msg-row ${role}`;
        if(index) row.id = `idx-${index}`;

        const header = document.createElement('div');
        header.className = 'msg-header';
        header.innerHTML = role === 'user' ? '👤 면접관' : '🤖 AI 비서';

        const textDiv = document.createElement('div');
        textDiv.className = 'msg-text';
        
        // 🚨 일반 메시지는 렌더링 시점에 바로 마크다운 변환
        textDiv.innerHTML = role === 'user' ? content.replace(/\n/g, '<br>') : marked.parse(content);

        row.appendChild(header);
        row.appendChild(textDiv);
        flow.appendChild(row);
        
        scrollChat();
        return { row: row, textDiv: textDiv };
    }

    function setInputState(disabled) {
        document.getElementById('queryInput').disabled = disabled;
        document.getElementById('sendBtn').disabled = disabled;
    }

    // 🤖 가짜 스트리밍 처리 (마크다운 실시간 변환)
    async function runFakeAi(answer, textDiv, index) {
        let current = "";
        const chunkSize = 3;
        for (let i = 0; i < answer.length; i += chunkSize) {
            current += answer.slice(i, i + chunkSize);
            // 스트리밍 중에도 마크다운 실시간 렌더링
            textDiv.innerHTML = marked.parse(current + " ▌");
            scrollChat();
            await new Promise(r => setTimeout(r, 15));
        }
        textDiv.innerHTML = marked.parse(answer);
        addBackLink(textDiv.parentNode, index);
        scrollChat();
    }

    async function askQuick(id) {
        if(document.getElementById('sendBtn').disabled) return;
        
        const data = quickData[id];
        const idx = messages.length + 1;
        
        appendBubble('user', data.q, idx);
        messages.push({role: "user", content: data.q});

        setInputState(true);
        
        const aiBubble = appendBubble('assistant', '', null);
        await runFakeAi(data.a, aiBubble.textDiv, idx);
        
        messages.push({role: "assistant", content: data.a});
        setInputState(false);
    }

    async function handleUserSubmit(e) {
        e.preventDefault();
        const input = document.getElementById('queryInput');
        const text = input.value.trim();
        if(!text || !systemPrompt) return;

        input.value = '';
        const idx = messages.length + 1;
        appendBubble('user', text, idx);
        
        if(messages.length === 0) messages.push({role: "system", content: systemPrompt});
        messages.push({role: "user", content: text});

        setInputState(true);
        const aiBubble = appendBubble('assistant', '');
        document.getElementById('streamLoading').style.display = 'block';
        scrollChat();

        try {
            const res = await fetch(WORKER_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: messages })
            });

            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let full = "";
            document.getElementById('streamLoading').style.display = 'none';

            while(true) {
                const { done, value } = await reader.read();
                if(done) break;
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');
                for(let line of lines) {
                    if(line.startsWith('data: ')) {
                        const dataStr = line.slice(6).trim();
                        if(dataStr === '[DONE]') continue;
                        try {
                            const parsed = JSON.parse(dataStr);
                            const content = parsed.choices[0].delta.content || "";
                            full += content;
                            // 진짜 AI 통신 중에도 마크다운 실시간 렌더링
                            aiBubble.textDiv.innerHTML = marked.parse(full + " ▌");
                            scrollChat();
                        } catch(e) {}
                    }
                }
            }
            aiBubble.textDiv.innerHTML = marked.parse(full);
            addBackLink(aiBubble.textDiv.parentNode, idx);
            messages.push({role: "assistant", content: full});
            scrollChat();
        } catch(e) { 
            document.getElementById('streamLoading').style.display = 'none';
            aiBubble.textDiv.innerHTML = "🚦 서버 연결에 실패했습니다. 다시 시도해주세요."; 
        } finally {
            setInputState(false);
        }
    }
</script>
</body>
</html>
