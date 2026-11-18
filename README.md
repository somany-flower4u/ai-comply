# 🤖 AI 컴플리 (AI Comply)
## AI 기본법 규제 자동 진단 및 컴플라이언스 도우미

> **한국의 AI 기본법 준수를 위한 지능형 자동 진단 서비스**
> 
> AI 기업들이 개발하는 서비스의 법적 지위를 정확히 파악하고, 준수해야 할 의무사항을 자동으로 진단해주는 스마트 컴플라이언스 플랫폼입니다.

---

## 📋 목차
1. [개요](#개요)
2. [주요 기능](#주요-기능)
3. [시스템 아키텍처](#시스템-아키텍처)
4. [기술 스택](#기술-스택)
5. [설치 및 구성](#설치-및-구성)
6. [사용 방법](#사용-방법)
7. [프로젝트 구조](#프로젝트-구조)
8. [API 및 모듈 설명](#api-및-모듈-설명)
9. [데이터 흐름](#데이터-흐름)
10. [문제 해결](#문제-해결)
11. [라이선스](#라이선스)

---

## 개요

### 🎯 프로젝트의 목적
AI 컴플리는 **한국의 AI 기본법(인공지능 발전과 신뢰 기반 조성 등에 관한 기본법)**을 준수하려는 AI 서비스 기업들을 위한 **자동 진단 및 컴플라이언스 도우미**입니다.

AI 서비스는 개발자, 서비스 제공자, 이용자 등 여러 역할을 동시에 수행할 수 있으며, 각 역할에 따라 법적 의무가 다릅니다. 또한 "고영향 AI"로 분류되면 더욱 강화된 규제가 적용됩니다.

AI 컴플리는 다음을 자동으로 수행합니다:
- ✅ 귀사의 AI 서비스가 어떤 법적 역할인지 분류
- ✅ 고영향 AI 해당 여부 진단
- ✅ 준수해야 할 의무사항 자동 생성
- ✅ 단계별 실행 로드맵 제시

### 📊 주요 혁신점
- **LLM + RAG 하이브리드**: 최신 LLM의 추론 능력과 법령DB의 정확한 정보를 결합
- **한국어 최적화**: 한글 임베딩 모델과 한국 법령 전문 학습 데이터
- **로컬 LLM 지원**: 비용 효율적이고 프라이빗한 온프레미스 배포 가능
- **동적 피드백**: 법령 변경시 자동 업데이트

---

## 주요 기능

### 1️⃣ AI 사업자 유형 자동 분류
귀사의 AI 서비스 정보를 입력하면, **AI 기본법 제2조**에 따라 법적 지위를 자동으로 분류합니다.

**분류 가능한 유형:**
- **인공지능 개발자**: 인공지능을 개발하는 자
- **인공지능 서비스제공자**: 인공지능 또는 인공지능을 활용한 서비스를 제공하는 자
- **인공지능 이용자**: 인공지능 또는 이를 활용한 서비스를 이용하는 자
- **생성형 인공지능 사업자**: 생성형 인공지능을 개발 및 서비스 제공하는 자

**진단 결과:**
```json
{
  "operator_types": ["인공지능 개발자", "생성형 인공지능 사업자"],
  "reasoning": "상세 분류 이유",
  "confidence": "높음",
  "relevant_articles": ["제2조", "제3조"]
}
```

### 2️⃣ 고영향 AI 진단
**AI 기본법 제33조** 기준에 따라 귀사의 AI가 "고영향 AI"에 해당하는지 판단합니다.

**고영향 AI 정의:**
> "그 오작동이나 오류로 인하여 시민의 기본권을 침해할 가능성이 높은 인공지능"

**평가 기준:**
| 요소 | 설명 | 영향도 |
|------|------|--------|
| **사용 영역** | 의료, 금융, 법집행, 교육 등 기본권 관련 분야 | ⭐⭐⭐⭐⭐ |
| **기본권 영향** | 생명권, 신체권, 인격권, 사생활권 등 | ⭐⭐⭐⭐⭐ |
| **중대성** | 오류 발생 시 피해 정도 | ⭐⭐⭐⭐ |
| **빈도** | 의사결정 수행 빈도 | ⭐⭐⭐ |
| **대체 가능성** | 인간 심사 또는 대체 수단 여부 | ⭐⭐⭐ |

**위험도 분류:**
- 🔴 **고위험**: 기본권 침해 가능성이 높음 → 강화된 규제 적용
- 🟡 **중위험**: 기본권 침해 가능성이 중간 → 중점 관리 필요
- 🟢 **저위험**: 기본권 침해 가능성이 낮음 → 기초 준수만으로 충분

**진단 결과:**
```json
{
  "is_high_impact": false,
  "risk_level": "저위험",
  "risk_factors": [
    {
      "factor": "사용 영역",
      "score": 1,
      "explanation": "콘텐츠/미디어 산업으로 기본권 침해 가능성 낮음"
    }
  ],
  "recommendation": "기본 투명성 확보 의무만 준수하면 됨"
}
```

### 3️⃣ 맞춤형 의무사항 체크리스트
분류된 사업자 유형 및 고영향 AI 여부에 따라 **준수해야 할 의무사항을 자동 생성**합니다.

**의무사항 카테고리:**

#### 📢 투명성 확보 의무
- 학습 데이터 정보 공개
- 개발 과정 정보 공개
- 성능 정보 공개
- 제한사항 및 오류 가능성 공지

#### 🛡️ 안전성 확보 의무
- 오작동/오류 방지 조치
- 위험 평가 및 관리
- 모니터링 시스템 구축
- 정기적인 감시 및 점검

#### 👤 이용자 보호 의무
- 의사결정 공개
- 설명 제공
- 이의제기 절차 마련
- 배상책임 보험

#### ⚡ 고영향 AI 특별 의무 (해당 시)
- 영향평가 수행 필수
- 모니터링 강화
- 정기적 보고서 제출

#### 📋 AI 영향평가 의무
- 평가 항목 및 범위 확정
- 평가 수행 및 문서화
- 개선 사항 반영

#### 🔐 개인정보 관련 의무
- 개인정보 보호법 준수
- 동의 관리
- 접근 통제
- 암호화

**체크리스트 모식:**
```json
{
  "category": "투명성 확보",
  "description": "학습 데이터의 종류, 규모, 전처리 방법 등 공개",
  "legal_basis": ["제24조"],
  "priority": "필수",
  "deadline": "연 1회 이상",
  "checklist": [
    "학습 데이터 출처 문서화",
    "정제 및 라벨링 프로세스 기록",
    "공개 방식 및 시기 결정"
  ]
}
```

### 4️⃣ 컴플라이언스 로드맵
**단계별 실행 계획**을 제시하여 조직적인 준수 활동을 지원합니다.

**로드맵 예시:**
```
Phase 1: 기초 준비 (1-2주)
├─ 현황 파악 및 법적 요구사항 검토
├─ 담당 조직 구성
└─ 내부 정책 수립

Phase 2: 투명성 확보 (2-4주)
├─ 데이터 정보 문서화
├─ 개발 과정 기록
└─ 공시 자료 작성

Phase 3: 안전성 강화 (3-6주)
├─ 모니터링 시스템 구축
├─ 오류 관리 절차 수립
└─ 테스트 및 검증

Phase 4: 영향평가 (4-8주)
├─ 평가항목 정의
├─ 평가 수행
└─ 개선사항 반영
```

### 5️⃣ 법령 검색
최신 법령 데이터베이스에서 관련 조문을 빠르게 검색할 수 있습니다.

**주요 법령:**
- AI 기본법 및 시행령
- 개인정보 보호법 및 시행령
- 정보통신망 이용촉진 및 정보보호 등에 관한 법률

**검색 방식:**
- 키워드 검색 (의미 기반 벡터 검색)
- 카테고리 필터 (정의, 의무, 벌칙 등)
- 조문별 상세 내용 조회

---

## 시스템 아키텍처

### 전체 흐름도
```
┌─────────────────────────────────────────────────────────────┐
│                         End User                            │
│                    (Streamlit Web UI)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Layer (app.py)                     │
│  - 사용자 입력 수집                                          │
│  - 진단 오케스트레이션                                       │
│  - 결과 렌더링                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┬─────────────┬──────────────────┐
│ Classifier   │HighImpact   │ Obligation       │
│ Agent        │ Agent       │ Agent            │
│ (분류)       │ (진단)      │ (의무사항)       │
└──────┬───────┴──────┬──────┴────────┬─────────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
    ┌────────────────────────────────┐
    │    Base Agent (RAG 엔진)       │
    │ - 법령 검색 (벡터 유사도)      │
    │ - LLM 호출 (추론)             │
    │ - 응답 파싱                   │
    └──────────────┬─────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌──────────────────┐  ┌───────────────┐
│   Vector Store   │  │   LLM Engine  │
│   (ChromaDB)     │  │   (Ollama)    │
│   + 법령 임베딩  │  │               │
└──────────────────┘  └───────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│  Data Source Layer                   │
│  - 법령정보센터 API (데이터 수집)    │
│  - 벡터 임베딩 모델 (ko-sroberta)    │
└──────────────────────────────────────┘
```

### 핵심 컴포넌트

#### 1. **Streamlit UI** (`app.py`)
- 4개 탭으로 구성된 사용자 인터페이스
- 서비스 정보 입력 폼
- 진단 결과 시각화
- 의무사항 체크리스트
- 법령 검색 기능

#### 2. **에이전트 시스템** (`agents/`)
세 가지 전문가 에이전트가 협력하여 진단을 수행합니다:

**ClassifierAgent** (`classifier_agent.py`)
- 담당: AI 사업자 유형 분류
- 입력: 서비스 정보
- 출력: 분류된 유형, 근거, 관련 조문

**HighImpactAgent** (`high_impact_agent.py`)
- 담당: 고영향 AI 진단
- 입력: 서비스 정보, 사업자 유형
- 출력: 위험도, 위험요소, 권장사항

**ObligationAgent** (`obligation_agent.py`)
- 담당: 의무사항 매핑
- 입력: 서비스 정보, 사업자 유형, 고영향AI 여부
- 출력: 체크리스트, 로드맵, 관련법령

#### 3. **Base Agent** (`agents/base_agent.py`)
모든 에이전트의 기본 클래스로 RAG 로직을 제공합니다:

```python
class BaseAgent:
    def _retrieve_context(query, n_results=5):
        # 벡터 검색으로 관련 법령 조문 검색
        # 컨텍스트 포매팅
        
    def _generate(system_prompt, user_prompt, context):
        # LLM 호출
        # 응답 생성
        
    def _parse_llm_response(response):
        # JSON 파싱 (다단계 전략)
        # Markdown 코드블록 추출
        # 응답 검증
```

#### 4. **벡터 저장소** (`vector_store.py`)
ChromaDB를 기반으로 법령을 벡터화하고 검색합니다:

- 임베딩 모델: `jhgan/ko-sroberta-multitask` (한글 특화)
- 저장소: Persistent ChromaDB
- 검색 방식: 코사인 유사도

```python
class LegalVectorStore:
    def search(query, n_results=5):
        # 쿼리를 벡터로 변환
        # 유사도 기반 검색
        # 메타데이터 포함 반환
        
    def search_by_category(query, category, n_results=5):
        # 카테고리 필터링
        # 검색 수행
```

#### 5. **데이터 수집** (`data_collector.py`)
국가법령정보센터 API에서 법령을 수집하고 처리합니다:

```python
class LawDataCollector:
    def collect_all_target_laws():
        # 목표 법령 목록 순회
        # 각 법령 상세 정보 수집
        # 조문별 파싱
        # 청킹 (1500자 기준)
        
    def _request_with_retry(url, params):
        # 재시도 로직 포함 (최대 3회)
        # 지수 백오프
```

---

## 기술 스택

### Backend & ML
| 항목 | 도구 | 버전 | 목적 |
|------|------|------|------|
| **언어** | Python | 3.11+ | 프로젝트 기본 언어 |
| **LLM 오케스트레이션** | LangChain | ≥0.2.0 | 프롬프트 템플레이트, 체인, 메모리 관리 |
| **로컬 LLM** | Ollama | ≥0.1.0 | 온프레미스 LLM 실행 (qwen2.5:14b, EEVE-Korean-Chat-10.8B) |
| **벡터 DB** | ChromaDB | ≥0.5.0 | 법령 벡터 저장 및 검색 |
| **임베딩** | Sentence Transformers | ≥2.7.0 | 한글 텍스트 벡터화 (ko-sroberta-multitask) |
| **딥러닝** | PyTorch | ≥2.0.0 | 임베딩 모델 실행 |

### Frontend & UI
| 항목 | 도구 | 버전 | 목적 |
|------|------|------|------|
| **웹 UI** | Streamlit | ≥1.35.0 | 빠른 프로토타이핑 및 배포 |

### Data & API
| 항목 | 도구 | 버전 | 목적 |
|------|------|------|------|
| **HTTP 요청** | Requests | ≥2.31.0 | API 호출 |
| **XML 파싱** | xmltodict | ≥0.13.0 | 법령정보센터 XML 응답 파싱 |
| **HTML 파싱** | BeautifulSoup4 | ≥4.12.0 | HTML 크롤링 및 파싱 |

### Utilities
| 항목 | 도구 | 버전 | 목적 |
|------|------|------|------|
| **환경 변수** | python-dotenv | ≥1.0.0 | .env 파일 관리 |
| **타입 검증** | Pydantic | ≥2.0.0 | 데이터 모델 검증 |

---

## 설치 및 구성

### 📦 사전 요구사항

**1. 시스템 요구사항**
- OS: Windows 10/11, macOS, Linux
- Python: 3.11 이상
- 메모리: 최소 8GB (권장 16GB)
- 디스크: 최소 10GB (법령DB + 모델)

**2. 외부 서비스**
- Ollama (로컬 LLM 실행)
- 국가법령정보센터 OPEN API 키

### 🔧 설치 단계

#### Step 1: 저장소 클론
```bash
git clone https://github.com/your-repo/ai-comply.git
cd ai-comply
```

#### Step 2: Python 가상환경 생성
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: 의존성 설치
```bash
pip install -r requirements.txt

# PyTorch (선택사항 - 이미 포함되어 있음)
# CPU 버전
pip install torch torchvision

# GPU 버전 (CUDA 12.1)
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Step 4: 환경 변수 설정
`.env` 파일 생성:
```bash
# .env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=shqkel/EEVE-Korean-Chat-10.8B
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=korean_law_db
EMBEDDING_MODEL=jhgan/ko-sroberta-multitask
LAW_API_KEY=your_api_key_here
LAW_API_BASE_URL=http://www.law.go.kr/DRF
CHUNK_SIZE=1500
API_TIMEOUT=30
API_MAX_RETRIES=3
API_RETRY_DELAY=2
```

#### Step 5: Ollama 설정
**5-1. Ollama 설치**
- Windows/macOS: [ollama.com](https://ollama.com) 에서 다운로드
- Linux: `curl -fsSL https://ollama.ai/install.sh | sh`

**5-2. Ollama 실행**
```bash
# 기본 포트 11434에서 서비스 시작
ollama serve

# (별도 터미널에서) 모델 다운로드
ollama pull shqkel/EEVE-Korean-Chat-10.8B
# 또는
ollama pull qwen2.5:14b

# (향후) 모델 실행
ollama run shqkel/EEVE-Korean-Chat-10.8B
```

**5-3. Ollama 상태 확인**
```bash
# 다른 터미널에서
curl http://localhost:11434/api/tags
```

#### Step 6: API 키 획득
국가법령정보센터 OPEN API:
1. [법령정보센터](https://www.law.go.kr) 접속
2. OPEN API 신청
3. API 키 발급 받기
4. `.env` 파일에 `LAW_API_KEY` 입력

#### Step 7: 벡터 DB 초기화
```bash
# 첫 실행 시에만 필요
python -c "from data_collector import LawDataCollector; from vector_store import LegalVectorStore; collector = LawDataCollector(); articles = collector.collect_all_target_laws(); vs = LegalVectorStore(); vs.build_from_scratch(articles)"
```

또는 Streamlit UI에서 사이드바의 "🔄 데이터베이스 구축" 버튼 클릭

#### Step 8: 애플리케이션 실행
```bash
streamlit run app.py
```

자동으로 브라우저가 열립니다:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 사용 방법

### 📱 Web UI 튜토리얼

#### **Tab 1: 📋 서비스 정보 입력**

1. **기본 정보 입력**
   - 서비스/제품명: 예) "AI 채용 심사 시스템"
   - 현재 개발 단계: 선택 (기획/개발중/베타/운영중)
   - 서비스 설명: 구체적인 기능 설명 (200자 이상 권장)

2. **기술 정보 선택**
   - AI 유형: 생성형 AI, 예측/분류 AI 등 선택
   - 산업 분야: 의료, 금융, 채용 등 해당 분야 선택
   - 개발 방식: "자체 개발" 또는 "외부 API 활용" 등 선택

3. **데이터 및 대상 입력**
   - 개인정보 포함 여부
   - 서비스 대상 (소비자/B2B/공공기관 등)
   - 데이터 출처

4. **진단 시작**
   - "🚀 진단 시작" 버튼 클릭
   - 진행 상황을 진행률 바로 확인 가능

#### **Tab 2: 📊 진단 결과**

진단 완료 후 자동으로 이 탭으로 이동합니다.

**A. 📋 사업자 유형 분류 결과**
```
분류 결과: ✓ 인공지능 개발자, ✓ 생성형 인공지능 사업자

상세 분류 이유:
[클릭하여 펼치기]
"귀사의 AI 서비스는 인공지능 개발자로 분류됩니다. 왜냐하면..."
```

**B. ⚠️ 고영향 AI 진단 결과**
- 위험도 시각화: 🟢 저위험 / 🟡 중위험 / 🔴 고위험
- 위험요소 분석:
  ```
  사용 영역: ███░░░░░░ (3/5)
  기본권 영향: █░░░░░░░░ (1/5)
  중대성: ██░░░░░░░ (2/5)
  ...
  ```
- 권장사항

**C. ✅ 의무사항 체크리스트**
- 의무사항 목록 (최대 10개 표시)
- 우선순위 표시: 🔴 필수 / 🟡 권장
- 체크박스로 진행상황 추적

#### **Tab 3: ✅ 의무사항 상세 체크리스트**

모든 의무사항의 세부 정보를 확인합니다.

**필터링:**
- 카테고리별 필터 (전체/투명성/안전성/이용자보호 등)

**세부 정보:**
- 의무명
- 설명
- 법적 근거 (조문 참고)
- 이행 주기
- 실행 체크리스트 아이템

**다운로드:**
- 📄 진단 보고서 (Markdown)
- 📊 체크리스트 (JSON)

#### **Tab 4: 🔍 법령 검색**

관련 법령을 자유롭게 검색합니다.

**검색 방법:**
1. 검색어 입력 (예: "투명성", "개인정보", "의무")
2. 검색 범위 선택 (전체/정의/의무/벌칙 등)
3. "🔎 검색" 버튼 클릭

**검색 결과:**
- 관련 법령 조문 리스트
- 법령명, 조문번호, 조문제목, 내용
- "📖 법령정보센터에서 보기" 링크

---

## 프로젝트 구조

```
ai-comply/
│
├── 📄 app.py                        # Streamlit 메인 애플리케이션
├── 📄 config.py                     # 프로젝트 설정 (API, 모델, 경로)
├── 📄 requirements.txt              # Python 의존성
├── 📄 README.md                     # 이 파일
├── 📄 .env.example                  # 환경 변수 템플릿
├── 📄 run.sh / run.bat              # 실행 스크립트
│
├── 📂 agents/                       # AI 에이전트 시스템
│   ├── 📄 __init__.py
│   ├── 📄 base_agent.py             # 기본 에이전트 (RAG, LLM 호출)
│   ├── 📄 classifier_agent.py       # 사업자 유형 분류 에이전트
│   ├── 📄 high_impact_agent.py      # 고영향 AI 진단 에이전트
│   └── 📄 obligation_agent.py       # 의무사항 매핑 에이전트
│
├── 📂 chroma_db/                    # ChromaDB 벡터 저장소 (생성됨)
│   ├── 📄 chroma.sqlite3
│   └── 📂 [collection directories]
│
├── 📂 logs/                         # 로그 파일 (생성됨)
│   ├── 📄 agents.log
│   ├── 📄 data_collector.log
│   └── 📄 vector_store.log
│
├── 📄 data_collector.py             # 법령 데이터 수집
├── 📄 vector_store.py               # 벡터 저장소 관리
├── 📄 text_processor.py             # 텍스트 전처리
├── 📄 utils.py                      # 유틸리티 함수들
│
└── 📄 test_*.py                     # 테스트 스크립트들
    ├── 📄 test_api.py
    ├── 📄 test_articles.py
    ├── 📄 test_collect.py
    └── 📄 test_save.py
```

### 핵심 파일 설명

#### `app.py` (500+ 줄)
Streamlit 웹 애플리케이션의 메인 파일입니다.

**주요 함수:**
- `init_session_state()`: 세션 초기화
- `render_sidebar()`: 사이드바 렌더링
- `main()`: 메인 애플리케이션 로직
- `perform_diagnosis()`: 진단 오케스트레이션

**세션 상태:**
- `vector_store`: 벡터 저장소 인스턴스
- `user_input`: 사용자 입력 데이터
- `diagnosis_results`: 진단 결과 캐시
- `active_tab`: 현재 활성 탭

#### `agents/base_agent.py` (300+ 줄)
모든 에이전트의 부모 클래스입니다.

**핵심 메서드:**
```python
def _retrieve_context(query, n_results, category_filter):
    """벡터 검색으로 관련 법령 조문 검색"""
    
def _generate(system_prompt, user_prompt, context):
    """LLM 호출하여 응답 생성"""
    
def _parse_llm_response(response):
    """다단계 JSON 파싱
    - Markdown 코드블록 추출
    - 직접 JSON 파싱
    - 줄바꿈 제거 후 재시도
    - 끝쉼표 제거 후 재시도
    """
    
def _format_source_references(search_results):
    """검색 결과를 참고 출처로 포매팅"""
```

#### `agents/classifier_agent.py` (150+ 줄)
AI 사업자 유형 분류 에이전트입니다.

**입력 데이터:**
```json
{
  "service_name": "AI 채용 심사 시스템",
  "service_description": "자소서와 경력기술서를 분석하여 채용 후보자를 추천",
  "ai_type": "예측/분류 AI",
  "development_method": ["자체 개발"],
  "target_users": ["기업 고객(B2B)"],
  "industry_sector": "채용/인사",
  "data_usage": ["개인정보 포함 데이터"],
  "development_stage": "서비스 운영 중"
}
```

**출력 데이터:**
```json
{
  "operator_types": ["인공지능 개발자", "인공지능 서비스제공자"],
  "reasoning": "자체 개발한 AI를 기업고객에게 서비스 제공하므로...",
  "confidence": "높음",
  "key_factors": ["자체 개발", "B2B 서비스 제공", "개인정보 활용"],
  "relevant_articles": [...]
}
```

#### `agents/high_impact_agent.py` (200+ 줄)
고영향 AI 진단 에이전트입니다.

**평가 기준:**
- 사용 영역 (의료, 금융, 법집행, 교육 등)
- 기본권 영향 (생명권, 신체권, 인격권, 사생활권)
- 중대성 (오류 발생 시 피해)
- 빈도 (의사결정 빈도)
- 대체 가능성 (인간 심사 여부)

**출력 데이터:**
```json
{
  "is_high_impact": false,
  "risk_level": "저위험",
  "risk_factors": [
    {
      "factor": "사용 영역",
      "score": 2,
      "explanation": "채용/인사 분야는 중간도의 기본권 영향"
    }
  ],
  "reasoning": "채용 시스템이지만...",
  "recommendation": "고영향 AI 아님, 기본 의무 준수 충분"
}
```

#### `agents/obligation_agent.py` (200+ 줄)
의무사항 매핑 에이전트입니다.

**의무사항 카테고리:**
1. 투명성 확보 의무
2. 안전성 확보 의무
3. 이용자 보호 의무
4. 고영향 AI 특별 의무
5. AI 영향평가 의무
6. 개인정보 관련 의무

**출력 데이터:**
```json
{
  "obligations": [
    {
      "category": "투명성 확보",
      "name": "학습 데이터 정보 공개",
      "description": "학습에 사용된 데이터의 종류, 규모, 전처리 방법 공개",
      "legal_basis": ["제24조"],
      "priority": "필수",
      "deadline": "연 1회",
      "checklist": ["데이터 출처 기록", "규모 파악", "전처리 문서화"]
    }
  ],
  "roadmap": [...],
  "related_laws": [...]
}
```

#### `vector_store.py` (250+ 줄)
ChromaDB를 통한 벡터 저장소 관리입니다.

**핵심 기능:**
```python
def build_from_scratch(articles):
    """처음부터 벡터 DB 구축"""
    
def search(query, n_results=5):
    """키워드 검색"""
    
def search_by_category(query, category, n_results=5):
    """카테고리 필터링 검색"""
    
def get_stats():
    """저장된 조문 통계 반환"""
```

#### `data_collector.py` (300+ 줄)
국가법령정보센터 API에서 법령을 수집합니다.

**핵심 기능:**
```python
def collect_all_target_laws():
    """모든 목표 법령 수집"""
    
def search_law(query):
    """법령명으로 검색"""
    
def get_law_detail(law_id):
    """법령 상세 정보 조회"""
    
def _parse_article(article_xml):
    """조문 XML 파싱"""
```

---

## API 및 모듈 설명

### REST API 엔드포인트 (향후 추가 계획)

```
# 진단 API
POST /api/diagnosis
Request: {
  "service_name": "...",
  "service_description": "...",
  ...
}
Response: {
  "classifier": {...},
  "high_impact": {...},
  "obligation": {...}
}

# 검색 API
GET /api/search?query=...&category=...
Response: [{...}, {...}, ...]
```

### Python API 예제

#### 예제 1: 진단 수행
```python
from vector_store import LegalVectorStore
from agents import ClassifierAgent, HighImpactAgent, ObligationAgent

# 초기화
vs = LegalVectorStore()

# 사용자 입력
user_input = {
    "service_name": "AI 채용 심사 시스템",
    "service_description": "자소서 분석 및 추천...",
    "ai_type": "예측/분류 AI",
    ...
}

# 1단계: 분류
classifier = ClassifierAgent(vs)
result1 = classifier.classify(user_input)

# 2단계: 진단
high_impact = HighImpactAgent(vs)
result2 = high_impact.diagnose(
    user_input,
    result1['operator_types']
)

# 3단계: 의무사항
obligation = ObligationAgent(vs)
result3 = obligation.map_obligations(
    user_input,
    result1['operator_types'],
    result2
)

print(result1)  # 분류 결과
print(result2)  # 진단 결과
print(result3)  # 의무사항
```

#### 예제 2: 법령 검색
```python
from vector_store import LegalVectorStore

vs = LegalVectorStore()

# 키워드 검색
results = vs.search("투명성 의무", n_results=5)
for result in results:
    print(f"[{result['metadata']['law_name']}]")
    print(f"조문: {result['metadata']['article_no']}")
    print(f"내용: {result['content']}\n")

# 카테고리 필터링 검색
results = vs.search_by_category(
    "고영향 AI",
    category="정의",
    n_results=3
)
```

#### 예제 3: 데이터 수집
```python
from data_collector import LawDataCollector
from vector_store import LegalVectorStore

# 법령 수집
collector = LawDataCollector()
articles = collector.collect_all_target_laws()
print(f"수집된 조문: {len(articles)}개")

# 벡터 DB 구축
vs = LegalVectorStore()
vs.build_from_scratch(articles)
vs.get_stats()  # 통계 출력
```

---

## 데이터 흐름

### 1️⃣ 데이터 수집 흐름

```
국가법령정보센터 API
        │
        ▼
┌─────────────────────┐
│  LawDataCollector   │
│ - 법령명으로 검색   │
│ - 법령 상세정보조회 │
│ - XML 파싱          │
│ - 조문 추출         │
└─────────────────────┘
        │
        ▼ (Article List)
┌─────────────────────┐
│  TextProcessor      │
│ - 전처리            │
│ - 청킹 (1500자)     │
│ - 메타데이터 생성   │
└─────────────────────┘
        │
        ▼ (Processed Articles)
┌─────────────────────┐
│  LegalVectorStore   │
│ - 임베딩 생성       │
│ - ChromaDB 저장     │
└─────────────────────┘
```

**데이터 구조 예시:**
```json
{
  "id": "AI기본법_제33조_1",
  "content": "고영향 인공지능이란 그 오작동이나 오류로 인하여...",
  "metadata": {
    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
    "law_id": "10100",
    "article_no": "제33조",
    "article_title": "고영향 인공지능의 정의",
    "enforcement_date": "2024-12-26",
    "law_type": "기본법",
    "category": "정의"
  }
}
```

### 2️⃣ 진단 흐름

```
User Input (웹 폼)
    │
    ▼
┌──────────────────────┐
│   Session State      │
│  저장 및 캐싱        │
└──────────────────────┘
    │
    ├─ (Step 1) ClassifierAgent
    │   ├─ 벡터 검색: "사업자 유형 정의"
    │   ├─ LLM 호출: 분류 프롬프트
    │   └─ JSON 파싱: 결과 추출
    │
    ├─ (Step 2) HighImpactAgent
    │   ├─ 벡터 검색: "고영향 AI 정의"
    │   ├─ LLM 호출: 진단 프롬프트
    │   └─ JSON 파싱: 결과 추출
    │
    └─ (Step 3) ObligationAgent
        ├─ 벡터 검색: "의무 투명성 안전성"
        ├─ LLM 호출: 의무사항 프롬프트
        └─ JSON 파싱: 결과 추출
    
    ▼
Results Cache
    │
    ▼
Streamlit Rendering
    └─ Tab 2: 진단 결과 표시
```

### 3️⃣ RAG 쿼리 처리 흐름

```
사용자 쿼리 (자연어)
    │
    ▼
┌──────────────────────┐
│  쿼리 임베딩         │
│  (ko-sroberta)       │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│  ChromaDB 검색       │
│  (코사인 유사도)     │
│  상위 N개 결과 반환  │
└──────────────────────┘
    │
    ▼ (Context Documents)
┌──────────────────────┐
│  컨텍스트 포매팅     │
│  ```                 │
│  [1] 법령: ...       │
│  [2] 법령: ...       │
│  ...                 │
│  ```                 │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│  프롬프트 구성       │
│  - System Prompt     │
│  - Context (RAG)     │
│  - User Prompt       │
└──────────────────────┘
    │
    ▼
┌──────────────────────┐
│  Ollama (LLM)        │
│  추론 및 생성        │
└──────────────────────┘
    │
    ▼
LLM Response (JSON)
    │
    ▼
┌──────────────────────┐
│  응답 파싱           │
│  - JSON 검출         │
│  - 유효성 검증       │
│  - 타입 변환         │
└──────────────────────┘
    │
    ▼
Final Result (Python Dict)
```

---

## 문제 해결

### 🔴 일반적인 문제 및 해결 방법

#### 1. Ollama 연결 오류
**증상:** `requests.exceptions.ConnectionError: Failed to connect to Ollama`

**해결 방법:**
```bash
# Ollama 서버 실행 여부 확인
curl http://localhost:11434/api/tags

# Ollama 서버 재시작
ollama serve

# 방화벽 확인
# Windows: netstat -ano | findstr :11434
# macOS: lsof -i :11434
```

#### 2. 메모리 부족 오류
**증상:** `RuntimeError: CUDA out of memory` 또는 `MemoryError`

**해결 방법:**
- Ollama 모델 변경 (가벼운 모델 사용)
  ```bash
  ollama pull mistral    # 경량 모델
  # .env 파일에서 OLLAMA_MODEL 변경
  ```
- 청크 크기 감소
  ```python
  # config.py에서
  CHUNK_SIZE = 1000  # 1500에서 감소
  ```

#### 3. ChromaDB 손상
**증상:** `Failed to create collection` 또는 DB 오류

**해결 방법:**
```bash
# 벡터 DB 초기화 (데이터 재수집)
rm -rf chroma_db/

# Streamlit UI에서 "🔄 데이터베이스 구축" 클릭
```

#### 4. API 키 오류
**증상:** `LAW_API_KEY is empty` 또는 `401 Unauthorized`

**해결 방법:**
1. [법령정보센터](https://www.law.go.kr) 접속
2. API 신청 페이지에서 새 키 발급
3. `.env` 파일 업데이트
   ```bash
   LAW_API_KEY=your_new_key
   ```

#### 5. JSON 파싱 오류
**증상:** `LLM이 요청된 JSON 형식으로 응답하지 않았습니다`

**해결 방법:**
1. 입력 텍스트 단순화 (기존 시스템 프롬프트 문제)
2. 다른 LLM 모델 시도
   ```bash
   ollama pull qwen2.5:14b
   # .env에서 OLLAMA_MODEL 변경
   ```
3. 페이지 새로고침 후 재시도

#### 6. 속도 저하
**증상:** 진단에 5분 이상 소요

**성능 최적화:**
```python
# config.py 조정
CHUNK_SIZE = 1000  # 기본 1500
N_SEARCH_RESULTS = 3  # 기본 5

# Ollama 성능 설정
# .env에 추가
OLLAMA_TEMPERATURE=0.3  # 더 결정론적 (범위: 0-1)
```

### 📊 로그 확인

**로그 파일 위치:**
- `agents.log`: 에이전트 실행 로그
- `data_collector.log`: 데이터 수집 로그
- `vector_store.log`: 벡터 저장소 로그

**로그 레벨:**
```bash
# 상세 로그 확인
tail -f agents.log | grep -E "ERROR|WARNING"

# 실시간 모니터링
watch -n 1 'tail -20 agents.log'
```

---

## 고급 설정

### 🔧 LLM 모델 변경

**지원하는 모델:**
```bash
# 한국어 특화 모델 (권장)
ollama pull shqkel/EEVE-Korean-Chat-10.8B

# 일반 모델
ollama pull qwen2.5:14b
ollama pull mistral
ollama pull neural-chat

# 설정 변경
# .env
OLLAMA_MODEL=qwen2.5:14b
```

### 📈 검색 결과 최적화

```python
# config.py
# 검색 결과 수 조정
N_SEARCH_RESULTS = 5  # 기본값

# 코사인 유사도 임계값 (향후)
SIMILARITY_THRESHOLD = 0.5

# 검색 쿼리 개선
# agents/base_agent.py _retrieve_context() 메서드
# 쿼리 전처리 로직 추가 가능
```

### 🔐 보안 설정

```python
# config.py
# API 타임아웃 (초)
API_TIMEOUT = 30

# 최대 재시도 횟수
API_MAX_RETRIES = 3

# 재시도 간격 (초)
API_RETRY_DELAY = 2

# 환경 변수 검증
import os
assert os.getenv("LAW_API_KEY"), "LAW_API_KEY is required"
```

---

## 개발 및 확장

### 🚀 새 에이전트 추가

```python
# agents/custom_agent.py
from .base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def diagnose(self, user_input):
        # 1. 컨텍스트 검색
        context, results = self._retrieve_context(
            "검색 쿼리",
            n_results=5
        )
        
        # 2. 프롬프트 구성
        system_prompt = "당신은 ...한 전문가입니다"
        user_prompt = f"다음을 진단하세요: {user_input}"
        
        # 3. LLM 호출
        response = self._generate(
            system_prompt,
            user_prompt,
            context
        )
        
        # 4. 응답 파싱
        parsed = self._parse_llm_response(response)
        
        return parsed
```

### 🧪 테스트

```bash
# 단위 테스트
python -m pytest test_*.py -v

# 통합 테스트
python test_api.py

# 성능 테스트
python -c "from agents import ClassifierAgent; ..."
```

---

## 라이선스

MIT License - 자세한 내용은 LICENSE 파일 참조

---

## 기여 가이드

버그 리포트, 기능 요청, Pull Request를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 연락처 및 지원

- **이슈 리포트**: GitHub Issues
- **이메일**: support@stelide.com

---

## 감사의 말

- 국가법령정보센터 (법령 데이터 제공)
- Sentence Transformers (한글 임베딩 모델)
- Ollama (로컬 LLM 플랫폼)
- ChromaDB (벡터 DB)
- Streamlit (웹 UI 프레임워크)

---

**마지막 업데이트:** 2024년 12월 26일
**버전:** 1.0.0
**상태:** Production Ready

### Frontend
- **Streamlit**: 대화형 웹 UI
- **Python 표준 라이브러리**

### 개발도구
- **Git**: 버전 관리
- **pip**: 패키지 관리

---

## 📋 프로젝트 구조

```
ai-comply/
│
├── requirements.txt              # 패키지 의존성
├── .env.example                  # 환경변수 템플릿
├── config.py                     # 설정 파일
│
├── data_collector.py             # 법령 데이터 수집 (OPEN API)
├── text_processor.py             # 법령 텍스트 전처리 및 청킹
├── vector_store.py               # ChromaDB 벡터 저장소 관리
│
├── agents/                       # AI 진단 에이전트
│   ├── __init__.py
│   ├── base_agent.py             # 기본 에이전트 클래스 (RAG 로직)
│   ├── classifier_agent.py       # 사업자 유형 분류
│   ├── high_impact_agent.py      # 고영향 AI 진단
│   └── obligation_agent.py       # 의무사항 매핑
│
├── app.py                        # Streamlit 메인 UI
├── utils.py                      # 유틸리티 함수
│
├── run.sh                        # Linux/Mac 실행 스크립트
├── run.bat                       # Windows 실행 스크립트
│
├── chroma_db/                    # ChromaDB 저장소 (자동 생성)
└── README.md                     # 이 파일
```

---

## 🚀 설치 및 실행

### 사전 요구사항

1. **Python 3.11 이상**
   ```bash
   python --version
   ```

2. **Ollama 설치 및 실행**
   - [https://ollama.ai](https://ollama.ai) 에서 Ollama 다운로드
   - 설치 후 명령어로 실행:
     ```bash
     ollama serve
     ```
   - 첫 사용 시 `qwen2.5:14b` 모델 다운로드:
     ```bash
     ollama pull qwen2.5:14b
     ```

### 설치

#### Windows
```bash
run.bat
```

#### Mac/Linux
```bash
bash run.sh
```

또는 수동 설치:
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일을 편집하여 필요시 API 키 설정

# 앱 실행
streamlit run app.py
```

### 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 을 열어 접속하세요.

---

## 📖 사용 가이드

### 1. 데이터베이스 구축

처음 사용할 때는 사이드바의 **"데이터베이스 구축"** 버튼을 클릭하여 법령 데이터를 수집합니다.

- 국가법령정보센터에서 AI 관련 법령 자동 수집
- 텍스트 전처리 및 벡터화
- ChromaDB에 저장 (약 2-5분 소요)

### 2. 서비스 정보 입력

**📋 서비스 정보 입력** 탭에서:
- 서비스명과 설명
- AI 유형 (생성형, 예측/분류 등)
- 개발 방식 (자체개발, API 활용 등)
- 서비스 대상 (B2C, B2B, 공공기관 등)
- 산업 분야
- 개인정보 포함 여부

모든 정보를 입력 후 **"🚀 진단 시작"** 버튼 클릭

### 3. 진단 결과 확인

**📊 진단 결과** 탭에서 다음 내용 확인:
- **사업자 유형 분류**: 어떤 역할에 해당하는지
- **고영향 AI 진단**: 규제 강도 판단
- **의무사항 체크리스트**: 준수해야 할 의무사항

### 4. 체크리스트 관리

**✅ 체크리스트** 탭에서:
- 모든 의무사항의 상세 내용 확인
- 각 항목별 법적 근거 확인
- 체크박스로 이행 현황 추적

### 5. 법령 검색

**🔍 법령 검색** 탭에서:
- 특정 키워드로 법령 검색
- 카테고리별 필터
- 국가법령정보센터로 바로 이동

### 6. 보고서 생성

- **진단 보고서 다운로드**: 전체 결과를 마크다운 형식으로 저장
- **체크리스트 내보내기**: JSON 형식으로 저장

---

## ⚙️ 환경 설정

### `.env` 파일

```bash
# 국가법령정보 OPEN API 키 (선택)
LAW_API_KEY=your_api_key_here

# Ollama 설정
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:14b

# ChromaDB 설정
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=korean_law_db

# 로깅
LOG_LEVEL=INFO
```

### API 키 (선택사항)

국가법령정보센터 OPEN API를 사용하여 최신 법령 데이터를 자동으로 수집할 수 있습니다:

1. [OPEN API Portal](https://open.law.go.kr/) 방문
2. 회원가입 및 API 키 신청
3. `.env` 파일의 `LAW_API_KEY`에 입력

API 키 없이도 데모 데이터로 기본 진단이 가능합니다.

---

## 📚 법령 데이터

### 수집 대상 법령

- 인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 (AI기본법)
- 인공지능 발전과 신뢰 기반 조성 등에 관한 기본법 시행령 (AI기본법시행령)
- 개인정보 보호법
- 개인정보 보호법 시행령
- 정보통신망 이용촉진 및 정보보호 등에 관한 법률

### 벡터화 및 검색

- **임베딩 모델**: `jhgan/ko-sroberta-multitask` (한글 특화)
- **검색 방식**: 유사도 기반 의미 검색 (Vector Similarity Search)
- **청킹 전략**: 조문(Article) 단위로 청킹, 1500자 초과 시 항(Paragraph)으로 재분할

---

## 🔍 주요 기능 상세

### 1. 사업자 유형 분류 (ClassifierAgent)

**목표**: AI 기본법 제2조에 따른 사업자 유형 분류

**분류 기준**:
- AI를 직접 개발하는가? → **AI 개발자**
- AI를 활용한 서비스를 제공하는가? → **AI 서비스제공자**
- AI를 서비스로만 사용하는가? → **AI 이용자**
- 생성형 AI를 개발/제공하는가? → **생성형 AI 사업자**

**출력**: 사업자 유형 리스트, 분류 이유, 신뢰도

### 2. 고영향 AI 진단 (HighImpactAgent)

**목표**: AI 기본법 제33조의 "고영향 AI" 해당 여부 판단

**평가 기준**:
- **사용 영역**: 의료, 금융, 채용, 법집행, 주요기반시설 등
- **기본권 영향**: 생명권, 신체권, 인격권, 사생활권 등
- **중대성**: 오류 발생 시 피해 정도
- **빈도**: 의사결정에 사용되는 빈도
- **대체 가능성**: 인간 심사의 대체 가능 여부

**위험도 수준**:
- 🔴 **고위험**: 기본권 침해 가능성 높음
- 🟡 **중위험**: 기본권 침해 가능성 중간
- 🟢 **저위험**: 기본권 침해 가능성 낮음

**출력**: 고영향 AI 여부, 위험도 수준, 위험요소 분석, 권장사항

### 3. 의무사항 매핑 (ObligationAgent)

**목표**: 분류된 사업자 유형과 고영향 AI 여부에 따른 준수 의무사항 제시

**의무 카테고리**:

1. **투명성 확보 의무** (제31조)
   - 학습 데이터 정보 공개
   - 개발 과정 정보 공개
   - AI 성능 정보 공개
   - 이용자 통지

2. **안전성 확보 의무** (제32조)
   - 오작동/오류 방지 조치
   - 안전성 테스트
   - 모니터링 체계 구축

3. **이용자 보호 의무** (제34조)
   - 의사결정 과정 설명
   - 배상책임 보험
   - 불만 처리 절차

4. **고영향 AI 특별 의무** (고영향 AI만 해당)
   - AI 영향평가 수행
   - 위험 평가 및 저감
   - 정기적 모니터링
   - 결과 기록 및 보관

5. **AI 영향평가 의무** (제33조)
   - 영향평가 항목별 점검
   - 전문가 검증

6. **개인정보 관련 의무**
   - 개인정보보호법 준수
   - 별도 동의 취득
   - DPA(Data Processing Agreement) 체결

**출력**: 의무사항 목록, 단계별 로드맵, 관련 법령, 종합 의견

---

## 📈 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit UI                           │
│  (서비스 정보 입력 → 진단 → 결과 조회 → 보고서 생성)      │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │   Agent System  │
        │                 │
        │  Classifier     │◄──────┐
        │  HighImpact     │       │
        │  Obligation     │       │ Interact
        └────────┬────────┘       │
                 │                │
        ┌────────▼────────────────┘
        │   Vector Store (ChromaDB)
        │   + RAG Logic
        └────────┬─────────────────┐
                 │                 │
        ┌────────▼──────┐    ┌─────▼──────────┐
        │   LLM Ollama  │    │ Korean Embeddings
        │  (qwen2.5:14b)│    │ (ko-sroberta)
        │               │    │
        └───────────────┘    └────────────────┘
                 ▲
                 │
        ┌────────┴────────────┐
        │  Legal Documents    │
        │  (Korean Laws)      │
        │                     │
        │  • AI Basic Law     │
        │  • PIPA             │
        │  • etc.             │
        └─────────────────────┘
```

---

## 🤖 LLM 설정

### Ollama + EEVE-Korean-Chat-10.8B

- **모델**: shqkel/EEVE-Korean-Chat-10.8B:latest
- **특징**: 한글 이해도 우수, 추론 능력 강함
- **실행 환경**: 로컬 GPU/CPU (매우 빠름)

### 설정 변경

`config.py` 또는 `.env`에서 변경 가능:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "shqkel/EEVE-Korean-Chat-10.8B:latest"
```

다른 모델 사용 예:
```bash
ollama pull llama2
ollama pull mistral
```

---

## 📊 성능 및 제한사항

### 성능
- **법령 수집**: ~2분 (인터넷 속도에 따라 변동)
- **벡터화**: ~1분 (CPU에서 ~3분)
- **진단**: ~10-30초 (LLM 응답 시간)

### 제한사항
- 로컬 Ollama 필요 (GPU 권장)
- API 할당량 제한 (국가법령정보센터)
- 벡터 저장소 크기 (대량의 법령 데이터)

### 시스템 요구사항
- **메모리**: 최소 8GB (권장 16GB)
- **GPU**: RTX 3060 이상 권장 (CPU로도 가능하지만 느림)
- **디스크**: 10GB 이상 가용 공간

---

## 🧪 테스트

### 단위 테스트
```bash
python data_collector.py      # 데이터 수집 테스트
python text_processor.py      # 텍스트 처리 테스트
python vector_store.py        # 벡터 저장소 테스트
```

---

## 📝 로깅

모든 모듈에서 상세 로그를 생성합니다:

- `data_collector.log`: 법령 데이터 수집 로그
- `text_processor.log`: 텍스트 처리 로그
- `vector_store.log`: 벡터 저장소 로그
- `agents.log`: 에이전트 실행 로그

로그 레벨은 `config.py`에서 설정 가능합니다.

---

## 🐛 주요 기능 및 버그 리포트

GitHub Issues를 통해 버그 리포트 및 기능 제안을 받습니다.

---

## ⚖️ 법적 고지

**중요**: 본 서비스는 정보 제공용이며, 법적 조언이 아닙니다.

- 실제 법적 판단이 필요한 경우 전문가 상담을 권장합니다
- 법령 정보는 자동 수집되며 오류가 있을 수 있습니다
- 최신 법령 정보는 국가법령정보센터에서 확인하세요

---

## 📞 지원 및 문의

### 관련 기관
- **국가법령정보센터**: https://www.law.go.kr/
- **과학기술정보통신부**: https://www.msit.go.kr/
- **OPEN API 문서**: https://open.law.go.kr/

### 개발자 문의
프로젝트 이슈 페이지를 참고하세요.

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 🙏 기여 및 감사

본 프로젝트는 다음을 기반으로 합니다:

- **LangChain**: https://python.langchain.com/
- **Ollama**: https://ollama.ai/
- **ChromaDB**: https://www.trychroma.com/
- **Streamlit**: https://streamlit.io/
- **Sentence Transformers**: https://www.sbert.net/
- **국가법령정보센터**: https://www.law.go.kr/

---

## 이용 약관

이 소프트웨어는 "있는 대로" 제공되며, 명시적이거나 묵시적인 어떤 보증도 하지 않습니다.

작성일: 2026. 04. 12. (일)  
최종 수정: 2026. 04. 12. (일)  

