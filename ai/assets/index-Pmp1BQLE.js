const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/AdminDashboard-CUmVa0b3.js","assets/rolldown-runtime-DF2fYuay.js","assets/react--DbkYnXe.js","assets/api-u9t7NVm8.js","assets/markdown-DWUslIyz.js"])))=>i.map(i=>d[i]);
import{n as e}from"./rolldown-runtime-DF2fYuay.js";import{n as t,r as n,t as r}from"./react--DbkYnXe.js";import{a as i,i as a,n as o,r as s,t as c}from"./router-KRCrr5YT.js";import{a as l,c as u,o as d,s as f,t as p,u as m}from"./api-u9t7NVm8.js";(function(){let e=document.createElement(`link`).relList;if(e&&e.supports&&e.supports(`modulepreload`))return;for(let e of document.querySelectorAll(`link[rel="modulepreload"]`))n(e);new MutationObserver(e=>{for(let t of e)if(t.type===`childList`)for(let e of t.addedNodes)e.tagName===`LINK`&&e.rel===`modulepreload`&&n(e)}).observe(document,{childList:!0,subtree:!0});function t(e){let t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin===`use-credentials`?t.credentials=`include`:e.crossOrigin===`anonymous`?t.credentials=`omit`:t.credentials=`same-origin`,t}function n(e){if(e.ep)return;e.ep=!0;let n=t(e);fetch(e.href,n)}})();var h=e(n(),1),g=t(),_={btn6:{label:`📞 연락처`,q:`최준영 지원자의 연락처와 이메일을 알려줘.`,a:`📞 **연락처:** 010-2828-9832
📧 **이메일:** god8night@naver.com

단순한 면접 문의뿐만 아니라, 현재 귀사가 겪고 있는 인프라 병목 현상이나 정보보안/AI 도입 관련 기술적 고민이 있으시다면 언제든 편하게 연락 주십시오. 13년 3개월의 실무 노하우를 바탕으로 명쾌한 답변을 드리겠습니다.`},btn1:{label:`📄 증빙`,q:`이력서, 포트폴리오 및 증빙자료 링크를 정리해 줘.`,a:`지원자 최준영의 13년 경력 + 비개발자 신분으로 직접 운영 중인 **AI/DX 풀스택 플랫폼 4건**을 함께 검증할 수 있는 증빙 자료입니다.

| 분류 | 문서/프로젝트 | 링크 | 설명 |
|---|---|---|---|
| **🚀 라이브** | 금속업 SaaS ERP (B-mode) | [erp.realstoryjun.co.kr](https://erp.realstoryjun.co.kr) | Next.js 15 + Supabase, 26테이블/40마이그/5단계 RBAC 550룰 |
| **🚀 라이브** | 폴스타4 매뉴얼 AI Q&A | [psaimanual.realstoryjun.co.kr](https://psaimanual.realstoryjun.co.kr) | RAG(BGE+재정렬+HyDE) + Cloudflare D1 23테이블 |
| **🚀 라이브** | 바리가자 (라이딩 PWA) | [barigaja.co.kr](https://barigaja.co.kr) | Supabase Realtime + Edge Function 7개 + FCM V1 |
| **🚀 라이브** | AI 면접 비서 (이 시스템) | [realstoryjun.co.kr/ai](https://realstoryjun.co.kr/ai) | Cloudflare Workers + Groq Llama-4 + 60일 자동 GC |
| **웹** | 웹 이력서 (Main) | [바로가기](https://realstoryjun.dothome.co.kr/resume) | 직접 호스팅·세팅한 통합 이력서 |
| **문서** | 📊 경력기술서 PDF | [다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/resume.pdf) | 에이치아이티, 포스코ICT, 삼성SDI 주요 프로젝트 상세 |
| **문서** | 📝 자기소개서 PDF | [다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Selfintroduction.pdf) | 2005학번 엔지니어의 서사 + 디자인 융합 철학 |
| **문서** | 🎨 포트폴리오 PDF | [다운로드](https://realstoryjun.dothome.co.kr/uploads/resume/Portfolio.pdf) | 인프라 구조 + 보안 정책 시각화 결과물 |

각 라이브 플랫폼은 **OAuth/RBAC/RLS/AES/Rate Limiting까지 갖춘 프로덕션 아키텍처**입니다. 기술 검증이 필요한 항목은 위 도메인에서 실시간 확인 가능합니다.`},btn2:{label:`🚀 성과`,q:`주요 인프라 구축 및 보안 성과를 상세히 요약해 줘.`,a:`✅ **핵심 실무 성과 요약 (총 경력 13년 3개월)**

**1. 대규모 네트워크 및 시스템 고도화**
- 노후망(Cat.5/6) 직접 포설부터 100M → 1G → **10G 광랜(SFP+)** 으로의 전 구간 대역폭 고도화 완료
- **Cisco L3 기반 VLAN 최적화** 및 핵심 장비 RSTP 구성으로 네트워크 루핑 방지
- DB 서버 Data 분리 및 SATA SSD RAID 5 마이그레이션, NAS 스냅샷을 활용한 **데이터 3중 자동 백업** 체계 구축
- L4 스위치 도입을 통한 웹/DB 서버 이중화 및 로드밸런싱 구현

**2. 철저한 정보보안 및 컴플라이언스 대응**
- 2024년 **SEMES 협력업체 정보보안 평가 82.78점** 을 취득 (보안정책, 관리, 물리, IT 전 영역 51개 심화 항목 대응)
- UTM(VForce) 도입 및 L7 필터링 튜닝, WAF 구축, 망분리(Air-gap) 환경 설계
- Kaspersky EPP/DLP를 활용한 매체 제어(USB, MTP) 및 불법 소프트웨어 원천 차단(화이트리스트) 시스템 구축

**3. 전사 시스템(ERP) 기획 및 PM**
- 영림원 ERP 전략 도입 총괄 및 SEMES BOM 관련 자동화 시스템 개발
- 다우오피스 그룹웨어 연동을 통한 전산 자산 반출입, 라이선스 승인 등 사내 프로세스 전산화 완료`},btn3:{label:`🤖 강점`,q:`AI 활용 역량과 본인만의 독보적인 강점은?`,a:`🤖 **독보적 강점: AI를 '지휘'하는 의사결정자**

저는 코드를 처음부터 끝까지 짜는 개발자가 아닙니다. 그러나 어떤 도구를 어떻게 조합할지 결정하는 데에는 **13년의 인프라·보안 경험**이 작동합니다. 코드는 Claude Code 같은 도구로 빠르게 구현하지만, **어떤 구조를 선택할지 결정하는 것은 결국 사람의 몫**이고 그 결정의 품질이 시스템 수명을 좌우합니다.

**핵심 차별 요소**

- **사고 회로**: 비즈니스 요구 → 표준 준수(ANSI/ISO) → 보안 모델 → TCO(총 소유 비용) → Vendor Lock-in(특정 벤더 종속) 회피로 이어지는 의사결정 트리
- **DB 선정 사례**: AI 플랫폼 DB는 PostgreSQL(Supabase) — RLS(행 단위 보안)·OAuth 기본 제공이 결정 요인. Cloudflare D1(SQLite)은 운영 부담이 커 보조 캐시 한정
- **실증된 결과물**: 비개발자 신분으로 풀스택 AI 플랫폼 4건 라이브 운영 (폴스타4 RAG / 금속업 ERP 550룰 / 바리가자 Realtime / 본 챗봇)
- **자체 인프라 판단**: vLLM PagedAttention(KV 캐시 페이지 단위 관리) + Continuous Batching(연속 배치)으로 다중 사용자 추론, Q6 양자화 sweet spot으로 환각·VRAM 균형
- **운영 비용 감각**: "ChatGPT 청구서 1천만원 받기 전에 미리 자체 인프라로 전환"

시장 IT 책임자의 5% 미만이 가진 의사결정 회로 — 이것이 제 무기입니다.`},btn4:{label:`🛠️ 기술`,q:`현재 주력하고 있는 AI 및 주요 기술 스택을 알려줘.`,a:`🛠️ **핵심 AI 인프라 — "왜 이 결정을 내렸나"까지**

기업 내부의 데이터 보안을 유지하면서 AX/DX(AI 전환·디지털 전환)를 실현하는 **폐쇄망 로컬 LLM 환경 구축**에 특화. 단순 도구 나열이 아니라 **결정 기준**까지 함께 설명합니다.

**의사결정 사례별 기술 스택**

- **추론 엔진 — vLLM 채택**: PagedAttention(KV 캐시 페이지 단위 관리)으로 메모리 단편화 최소화, Continuous Batching으로 다중 사용자 동시 요청 처리. Ollama·llama.cpp는 단일 사용자 로컬용이라 5명+ 동시 추론에 부적합
- **양자화 — Q6 sweet spot**: Q4(저정밀)는 복잡 지시에 환각 발생, Q8(거의 무손실)은 VRAM 부담 큼. Q6가 메모리·정확도 균형점
- **RAG 파이프라인 — BGE 임베딩 + 재정렬 + HyDE(가설형 검색 보강)**: 약한 검색 케이스 정확도 개선. 폴스타4 매뉴얼 챗봇에서 라이브 운영 중
- **DB — Supabase(PostgreSQL)**: ANSI SQL:2008(국제 표준) 준수 + RLS·OAuth 기본 제공으로 운영 부담 ↓. D1(SQLite)은 보조 캐시 한정
- **하드웨어 사이징**: VRAM 32~96GB로 Qwen 70B+ 비전·MoE 모델 구동. 대학 H100 인프라 합법적 활용
- **인프라·보안 기반**: L3/L4 네트워크, 10G SFP+ 광랜, VMware, 데이터 3중 백업, 망분리, SEMES 컴플라이언스 — AI는 이 위에서만 안전하게 굴러갑니다

각 항목은 "왜 도입했나"를 설명할 수 있다는 것이 핵심입니다.`},btn5:{label:`🏆 차별점`,q:`다른 시니어 엔지니어와 차별화되는 점은 무엇인가요?`,a:`💡 **차별점: 구조를 파고드는 의사결정자**

"구조를 모르고 도입하면 운용할 수 없다." 이것이 제 13년의 결론입니다. "자동차를 운용하려면 엔진과 트레일까지 알아야 한다"는 사고 방식 — 단순 도입이 아니라 **표준·보안·TCO(총 소유 비용)·Vendor Lock-in(특정 벤더 종속)까지 따져 결정**하는 판단력. 시장 IT 책임자의 5% 미만이 가진 사고 회로입니다.

**기회 포착의 결단력**

- 2023년 ChatGPT 시대를 현업에서 체감 → AI 인프라 도입은 시간 문제로 인식
- 2025년 Claude Code 같은 도구 폭발 → 단순 활용을 넘는 **AI 인프라 오케스트레이션** 역량 필수임을 확신
- 안정적인 직장을 과감히 내려놓고 학업 복귀 → 대학 H100 인프라를 합법적으로 활용해 로컬 LLM 끝까지 빌드·테스트
- 졸업 요건은 팀 프로젝트 대신 **실무 + AI 인프라 이론을 집대성한 '논문'으로 협의 완료**

거대한 기술 흐름을 읽고 "잘못된 결정의 비용"을 최소화하는 판단력 — 이것이 귀사에 제공할 저의 가장 강력한 무기입니다. 2026년 8월, 완벽히 준비된 'AI 의사결정자'로서 다시 현장으로 나아갑니다.`},btn7:{label:`💰 연봉`,q:`희망 연봉이나 급여 조건은 어떻게 되시는지 궁금합니다.`,a:`💰 **희망 연봉: 9,000 ~ 10,000만원 (협의 가능)**

저의 **13년 3개월 인프라/보안 실무 노하우** + **풀스택 AI 플랫폼 4건 라이브 운영 실증** + **표준·TCO·Vendor Lock-in을 따지는 의사결정 회로**의 결합 가치는 시장에서 흔치 않은 **대체 불가능성**을 지닙니다.

* **가치 제안**: 단순한 시스템 관리자가 아닌, **구조를 모르고 도입하면 운용할 수 없다**는 원칙으로 사내 AX/DX를 안전하게 추진하는 책임자. ChatGPT 청구서 1천만원 받기 전에 자체 LLM 인프라로 전환할 수 있는 판단력 보유.
* **희망 직무**: CISO 후보 / 정보보안 책임자 / IT 인프라 팀장 / AI/DX 추진 PM / 디지털전환 리드 / 반도체 협력사 IT 본부장.
* **유연한 협의**: 9,000만원을 하한으로 하되, 귀사의 내규·복리후생·향후 비전을 종합적으로 고려해 긍정적이고 유연하게 협의할 준비가 되어 있습니다.`}},v=r(),y=()=>/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)||window.innerWidth<=768,b=()=>typeof crypto<`u`&&crypto.randomUUID?crypto.randomUUID():`${Date.now()}-${Math.random().toString(16).slice(2)}`,x=20,S=6,C=()=>(0,v.jsxs)(`header`,{className:`header`,children:[(0,v.jsxs)(`div`,{className:`header-title`,children:[(0,v.jsx)(`span`,{className:`status-dot`}),(0,v.jsx)(`h1`,{children:`최준영 AI 비서`})]}),(0,v.jsx)(`div`,{className:`badge`,children:`Senior IT Infra`})]}),w=({message:e})=>(0,v.jsx)(`div`,{className:`msg-row ${e.role}`,children:(0,v.jsxs)(`div`,{className:`msg-inner`,children:[(0,v.jsx)(`div`,{className:`avatar ${e.role}`,children:e.role===`assistant`?`🤖`:`👤`}),(0,v.jsx)(`div`,{className:`msg-text`,dangerouslySetInnerHTML:{__html:m(e.content||``)}})]})}),T=({onAsk:e})=>(0,v.jsx)(`div`,{className:`chip-container`,children:Object.entries(_).map(([t,n])=>(0,v.jsx)(`button`,{type:`button`,className:`chip ${t===`btn6`?`highlight`:``}`,onClick:()=>e(t),children:n.label},t))});function E(){let[e,t]=(0,h.useState)(()=>[{id:b(),role:`assistant`,content:`반갑습니다. 최준영 지원자의 AI 면접 비서입니다.
궁금하신 점을 질문해 주시면 13년의 실무 노하우를 바탕으로 답변해 드리겠습니다.`}]),[n,r]=(0,h.useState)(``),[i,a]=(0,h.useState)(!1),[o,s]=(0,h.useState)(!1),c=(0,h.useRef)(null),u=(0,h.useRef)(null),f=(0,h.useRef)(``),p=(0,h.useRef)(null),m=(0,h.useRef)(!1),g=(0,h.useMemo)(()=>{let t=e[e.length-1];return t?.role===`assistant`&&!t.content},[e]);(0,h.useEffect)(()=>{c.current?.scrollTo({top:c.current.scrollHeight,behavior:`smooth`})},[e,i]),(0,h.useEffect)(()=>{!i&&!y()&&u.current?.focus()},[i]),(0,h.useEffect)(()=>{let e=c.current,t=()=>s((e?.scrollTop||0)>300);return e?.addEventListener(`scroll`,t),()=>{e?.removeEventListener(`scroll`,t),p.current&&clearInterval(p.current)}},[]);let E=(0,h.useCallback)(()=>{p.current||=setInterval(()=>{if(f.current.length>0){let e=f.current.slice(0,S);f.current=f.current.slice(S),t(t=>{let n=[...t],r=n[n.length-1];return r?.role===`assistant`&&(r.content+=e),n})}else m.current&&(clearInterval(p.current),p.current=null,a(!1),y()||u.current?.focus())},x)},[]),D=(0,h.useCallback)(e=>{let n=_[e];n&&(l({question:n.q,answer:n.a,trigger:n.label}),t(e=>[...e,{id:b(),role:`user`,content:n.q},{id:b(),role:`assistant`,content:``}]),a(!0),m.current=!0,f.current=n.a,setTimeout(E,100))},[E]),O=(0,h.useCallback)(async n=>{let r=[...e,{id:b(),role:`user`,content:n}];t([...r,{id:b(),role:`assistant`,content:``}]),a(!0),f.current=``,m.current=!1,E();try{await d({messages:r.map(({role:e,content:t})=>({role:e,content:t})).slice(-6),onChunk:e=>{f.current+=e}})}catch(e){console.error(`streamChat error:`,e),f.current=`⚠️ 원활한 통신을 위해 잠시 후 다시 시도해 주세요.`}finally{m.current=!0}},[e,E]),k=(0,h.useCallback)(async e=>{e.preventDefault();let t=n.trim();!t||i||(r(``),y()&&u.current?.blur(),await O(t))},[n,i,O]);return(0,v.jsxs)(`div`,{className:`main-wrapper`,children:[(0,v.jsx)(C,{}),(0,v.jsx)(`div`,{className:`quick-questions-top`,children:(0,v.jsx)(T,{onAsk:D})}),(0,v.jsx)(`main`,{className:`chat-view`,ref:c,children:(0,v.jsxs)(`div`,{className:`messages-list`,children:[e.map(e=>(0,v.jsx)(w,{message:e},e.id)),i&&g&&(0,v.jsx)(`div`,{className:`stream-loading`,children:`AI가 답변을 생성하고 있습니다...`})]})}),o&&(0,v.jsx)(`button`,{type:`button`,className:`scroll-top-btn`,onClick:()=>c.current?.scrollTo({top:0,behavior:`smooth`}),"aria-label":`Move to Top`,children:`↑`}),(0,v.jsx)(`footer`,{className:`bottom-nav`,children:(0,v.jsxs)(`form`,{className:`input-group`,onSubmit:k,children:[(0,v.jsx)(`input`,{type:`text`,ref:u,placeholder:i?`AI 답변 중...`:`입력 창에 질문을 입력하세요...`,value:n,onChange:e=>r(e.target.value),disabled:i,onFocus:e=>{i&&e.target.blur()},"aria-label":`질문 입력`}),(0,v.jsx)(`button`,{type:`submit`,className:`send-btn`,disabled:i||!n.trim(),children:i?`...`:`➤`})]})})]})}function D({onLogin:e}){let[t,n]=(0,h.useState)(``),[r,i]=(0,h.useState)(``),[a,o]=(0,h.useState)(!1),[s,c]=(0,h.useState)(``);return(0,v.jsx)(`div`,{className:`admin-login-wrapper`,children:(0,v.jsxs)(`div`,{className:`glass-card login-card`,children:[(0,v.jsx)(`h2`,{children:`Admin Portal`}),(0,v.jsx)(`p`,{className:`subtitle`,children:`보안 정책에 따라 서버 인증을 거칩니다.`}),(0,v.jsxs)(`form`,{onSubmit:async n=>{n.preventDefault(),o(!0),c(``);try{let n=await p({email:t,password:r});n.success?e():c(n.message||`계정(Email) 또는 비밀번호가 올바르지 않습니다.`)}catch{c(`서버 통신 에러가 발생했습니다.`)}finally{o(!1)}},children:[(0,v.jsxs)(`div`,{className:`input-field`,children:[(0,v.jsx)(`label`,{htmlFor:`admin-email`,children:`Admin Email`}),(0,v.jsx)(`input`,{id:`admin-email`,type:`email`,autoComplete:`username`,value:t,onChange:e=>n(e.target.value),placeholder:`이메일(계정)을 입력하세요`,disabled:a,required:!0})]}),(0,v.jsxs)(`div`,{className:`input-field`,children:[(0,v.jsx)(`label`,{htmlFor:`admin-password`,children:`Admin Password`}),(0,v.jsx)(`input`,{id:`admin-password`,type:`password`,autoComplete:`current-password`,value:r,onChange:e=>i(e.target.value),placeholder:`비밀번호를 입력하세요`,disabled:a,required:!0})]}),s&&(0,v.jsx)(`div`,{className:`login-error`,role:`alert`,children:s}),(0,v.jsx)(`button`,{type:`submit`,className:`login-btn`,disabled:a,children:a?`인증 중...`:`서버 인증 및 로그인`})]})]})})}var O=(0,h.lazy)(()=>i(()=>import(`./AdminDashboard-CUmVa0b3.js`),__vite__mapDeps([0,1,2,3,4]))),k=({isAuthenticated:e,children:t})=>e?t:(0,v.jsx)(o,{to:`/admin/login`,replace:!0}),A=`/ai`;function j(){let[e,t]=(0,h.useState)(()=>!!u());(0,h.useEffect)(()=>{let e=()=>t(!!u()),n=setInterval(e,6e4);return window.addEventListener(`storage`,e),()=>{clearInterval(n),window.removeEventListener(`storage`,e)}},[]);let n=(0,h.useCallback)(()=>t(!0),[]),r=(0,h.useCallback)(()=>{f(),t(!1)},[]);return(0,v.jsx)(c,{basename:A,children:(0,v.jsxs)(a,{children:[(0,v.jsx)(s,{path:`/`,element:(0,v.jsx)(E,{})}),(0,v.jsx)(s,{path:`/admin/login`,element:e?(0,v.jsx)(o,{to:`/admin`,replace:!0}):(0,v.jsx)(D,{onLogin:n})}),(0,v.jsx)(s,{path:`/admin`,element:(0,v.jsx)(k,{isAuthenticated:e,children:(0,v.jsx)(h.Suspense,{fallback:(0,v.jsxs)(`div`,{className:`empty-state-v3`,children:[(0,v.jsx)(`span`,{children:`⏳`}),`로딩 중...`]}),children:(0,v.jsx)(O,{onLogout:r})})})}),(0,v.jsx)(s,{path:`*`,element:(0,v.jsx)(o,{to:`/`,replace:!0})})]})})}var M=class extends h.Component{constructor(e){super(e),this.state={error:null}}static getDerivedStateFromError(e){return{error:e}}componentDidCatch(e,t){console.error(`UI ErrorBoundary caught:`,e,t)}render(){return this.state.error?(0,v.jsxs)(`div`,{className:`error-boundary`,children:[(0,v.jsx)(`h2`,{children:`화면을 그리는 중 오류가 발생했습니다`}),(0,v.jsx)(`p`,{children:`잠시 후 다시 시도해 주세요.`}),(0,v.jsx)(`button`,{type:`button`,onClick:()=>window.location.reload(),children:`새로고침`})]}):this.props.children}};(0,g.createRoot)(document.getElementById(`root`)).render((0,v.jsx)(M,{children:(0,v.jsx)(j,{})}));