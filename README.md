# AI 컴플리 (AI Comply)

## AI 기본법 규제 자동 진단 서비스

AI 컴플리는 한국의 **AI 기본법(인공지능 발전과 신뢰 기반 조성 등에 관한 기본법)** 규제를 준수하기 위해 AI 서비스 기업들을 위한 **자동 진단 및 컴플라이언스 도우미** 서비스입니다.

### 🎯 주요 기능

- **AI 사업자 유형 자동 분류**: AI 기본법 제2조의 정의에 따라 귀사의 역할을 자동으로 분류합니다
  - 인공지능 개발자
  - 인공지능 서비스제공자
  - 인공지능 이용자
  - 생성형 인공지능 사업자

- **고영향 AI 진단**: AI 기본법 제33조 기준에 따라 고영향 AI 해당 여부를 판단합니다
  - 위험 수준 평가 (고위험/중위험/저위험)
  - 위험 요소 분석
  - 기본권 침해 가능성 진단

- **맞춤형 의무사항 체크리스트**: 분류된 사업자 유형 및 고영향 AI 여부에 따라 준수해야 할 의무사항을 자동으로 생성합니다
  - 투명성 확보 의무
  - 안전성 확보 의무
  - 이용자 보호 의무
  - 고영향 AI 특별 의무
  - AI 영향평가 의무
  - 개인정보 관련 의무

- **컴플라이언스 로드맵**: 단계별 실행 계획과 우선순위를 제시합니다
  - Phase별 구체적 실행 항목
  - 예상 소요 기간
  - 우선순위 구분

- **법령 검색**: 최신 법령 데이터베이스에서 관련 조문을 빠르게 검색합니다
  - 한글 특화 임베딩 모델 사용
  - 카테고리별 필터링

---

## 🛠 기술 스택

### Backend
- **Python 3.11+**
- **LangChain**: LLM 오케스트레이션
- **Ollama**: 로컬 LLM (`qwen2.5:14b`)
- **ChromaDB**: 법령 벡터 저장소
- **Sentence Transformers**: 한글 특화 임베딩 (`jhgan/ko-sroberta-multitask`)

### 데이터 소스
- **국가법령정보센터 OPEN API**: 실시간 법령 데이터 수집

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

### Ollama + qwen2.5:14b

- **모델**: Qwen2.5 14B (알리바바 최신 모델)
- **특징**: 한글 이해도 우수, 추론 능력 강함
- **실행 환경**: 로컬 GPU/CPU (매우 빠름)

### 설정 변경

`config.py` 또는 `.env`에서 변경 가능:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:14b"
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

작성일: 2024년
최종 수정: 2024년
