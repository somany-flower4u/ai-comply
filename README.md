# AI 컴플리 (AI Comply)

한국의 **인공지능 발전과 신뢰 기반 조성 등에 관한 기본법(이하 AI 기본법)**을 기준으로 AI 서비스의 규제 적용 가능성과 주요 준수 항목을 점검하는 Streamlit 기반 RAG 애플리케이션입니다.

서비스 정보를 입력하면 법령 검색 결과를 바탕으로 다음 내용을 단계적으로 분석합니다.

- AI 사업자 유형 분류
- 고영향 AI 해당 가능성 및 위험도 분석
- 서비스에 적용될 수 있는 준수 의무 체크리스트 생성
- 관련 법령 조문 검색

> **주의:** 이 프로젝트는 법률 정보 탐색과 사전 점검을 돕기 위한 도구이며 법률 자문이나 규제기관의 공식 판단을 대체하지 않습니다. 실제 적용 여부와 대응 방안은 최신 법령·시행령·고시를 확인하고 전문가의 검토를 받으세요.

## 주요 기능

### 서비스 진단

서비스명, 설명, AI 유형, 산업 분야, 개발 방식, 대상 사용자, 데이터 활용 여부, 개발 단계를 입력하면 세 전문 에이전트가 순서대로 분석합니다.

1. **분류 에이전트** — AI 개발자, AI 서비스제공자, AI 이용자, 생성형 AI 사업자 등 역할을 분류합니다.
2. **고영향 AI 에이전트** — 의료·금융·채용·교육·법집행·주요기반시설 등 분야와 기본권 영향 요소를 바탕으로 위험도를 분석합니다.
3. **의무사항 에이전트** — 투명성, 안전성, 이용자 보호, 고영향 AI, 영향평가, 개인정보 관련 항목을 정리합니다.

### 법령 기반 검색

국가법령정보센터 OPEN API에서 수집한 법령을 조문 단위로 처리하고, 한국어 임베딩 모델로 벡터화해 의미 기반 검색을 제공합니다.

현재 기본 수집 대상은 다음과 같습니다.

- 인공지능 발전과 신뢰 기반 조성 등에 관한 기본법
- 같은 법 시행령
- 개인정보 보호법 및 시행령
- 정보통신망 이용촉진 및 정보보호 등에 관한 법률

### 로컬 실행

LLM은 Ollama를 사용하므로 외부 LLM API 없이 로컬 환경에서 실행할 수 있습니다. 법령 원문과 임베딩 데이터도 로컬 ChromaDB에 저장됩니다.

## 처리 흐름

```text
사용자 입력
    ↓
Streamlit UI (app.py)
    ↓
법령 벡터 검색 ← ChromaDB + ko-sroberta-multitask
    ↓
Ollama LLM + 전문 에이전트
    ├─ 사업자 유형 분류
    ├─ 고영향 AI 분석
    └─ 준수 의무 생성
    ↓
진단 결과 · 체크리스트 · 법령 검색 결과
```

## 요구 사항

- Python 3.11 이상
- Ollama
- 국가법령정보센터 OPEN API 키
- 법령 데이터와 임베딩 모델을 저장할 디스크 공간

## 빠른 시작

### 1. 저장소 내려받기

```bash
git clone https://github.com/somany-flower4u/ai-comply.git
cd ai-comply
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

`.env`를 열어 최소한 `LAW_API_KEY`를 실제 키로 변경하세요. `.env.example`에는 비밀키를 커밋하지 마세요.

```dotenv
LAW_API_KEY=your-law-api-key
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=shqkel/EEVE-Korean-Chat-10.8B
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=korean_law_db
LOG_LEVEL=INFO
```

### 3. Ollama 준비

Ollama를 설치한 뒤 서버를 실행하고, 설정한 모델을 내려받습니다.

```bash
ollama serve
ollama pull shqkel/EEVE-Korean-Chat-10.8B
```

다른 모델을 사용할 경우 `.env`의 `OLLAMA_MODEL`을 변경하세요. 해당 모델이 한국어 지시를 충분히 이해하는지 확인하는 것을 권장합니다.

### 4. 실행

#### macOS / Linux

```bash
./run.sh
```

실행 스크립트는 Python 버전 확인, 가상환경 생성, 의존성 설치, `.env` 준비, Streamlit 실행을 수행합니다.

#### Windows

```bat
run.bat
```

#### 수동 실행

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 [http://localhost:8501](http://localhost:8501)을 여세요.

## 첫 실행: 법령 데이터베이스 구축

처음 실행하면 벡터 저장소가 비어 있을 수 있습니다.

1. 사이드바의 **데이터베이스 구축** 버튼을 클릭합니다.
2. 국가법령정보센터에서 대상 법령을 수집합니다.
3. 조문을 검색 가능한 청크로 나누고 `jhgan/ko-sroberta-multitask`로 임베딩합니다.
4. ChromaDB의 `korean_law_db` 컬렉션에 저장합니다.

법령 수집과 임베딩 생성에는 네트워크 및 시간이 필요합니다. 이후 실행에서는 `CHROMA_PERSIST_DIR`에 저장된 컬렉션을 재사용합니다. 법령 변경을 반영하려면 데이터베이스 구축을 다시 실행하세요.

## 화면 구성

| 화면 | 설명 |
| --- | --- |
| 서비스 정보 입력 | 진단에 필요한 서비스 정보를 입력하고 분석을 시작합니다. |
| 진단 결과 | 사업자 유형, 고영향 AI 위험도, 분석 근거와 관련 조문을 확인합니다. |
| 체크리스트 | 진단 결과를 바탕으로 생성된 준수 항목과 실행 계획을 확인합니다. |
| 법령 검색 | 키워드·카테고리·법령별로 관련 조문을 검색합니다. |

서비스 설명, 서비스명, 개발 방식은 진단에 필요한 필수 입력값입니다.

## 프로젝트 구조

```text
ai-comply/
├── app.py                 # Streamlit UI와 진단 흐름
├── config.py              # 환경 변수 및 법령·진단 설정
├── data_collector.py      # 국가법령정보센터 API 수집기
├── text_processor.py      # 조문 청킹 및 메타데이터 처리
├── vector_store.py        # ChromaDB 저장·검색·통계
├── utils.py               # 결과 포맷팅 및 보고서 유틸리티
├── agents/
│   ├── base_agent.py      # RAG 검색과 Ollama 호출 공통 로직
│   ├── classifier_agent.py# 사업자 유형 분류
│   ├── high_impact_agent.py# 고영향 AI 분석
│   └── obligation_agent.py# 준수 의무 생성
├── requirements.txt       # Python 의존성
├── .env.example           # 환경 변수 예시
├── run.sh                 # macOS/Linux 실행 스크립트
├── run.bat                # Windows 실행 스크립트
└── test_*.py              # API·수집·저장 관련 테스트
```

## 설정

주요 설정은 `config.py`에서 관리하며 환경 변수로 덮어쓸 수 있습니다.

| 변수 | 기본값 | 용도 |
| --- | --- | --- |
| `LAW_API_KEY` | 없음 | 국가법령정보센터 OPEN API 인증키 |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 서버 주소 |
| `OLLAMA_MODEL` | `shqkel/EEVE-Korean-Chat-10.8B` | 분석에 사용할 LLM |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB 저장 경로 |
| `CHROMA_COLLECTION_NAME` | `korean_law_db` | ChromaDB 컬렉션 이름 |
| `LOG_LEVEL` | `INFO` | 로그 레벨 |

임베딩 모델은 `jhgan/ko-sroberta-multitask`로 고정되어 있습니다.

## 테스트

의존성을 설치한 뒤 다음 명령으로 테스트를 실행합니다.

```bash
pytest -q
```

일부 테스트는 법령 API, Ollama 또는 로컬 벡터 저장소에 접근할 수 있어야 정상적으로 동작합니다. 외부 서비스가 필요한 테스트는 실행 환경과 `.env` 설정을 먼저 확인하세요.

## 문제 해결

### Ollama에 연결할 수 없습니다

```bash
curl http://localhost:11434/api/tags
```

Ollama가 실행 중인지 확인하고 `OLLAMA_BASE_URL`이 실제 주소와 일치하는지 확인하세요.

### 데이터베이스 구축이 실패합니다

- `LAW_API_KEY`가 유효한지 확인합니다.
- 국가법령정보센터 API 요청 제한 또는 네트워크 상태를 확인합니다.
- `chroma_db` 경로에 쓰기 권한과 충분한 디스크 공간이 있는지 확인합니다.
- 임베딩 모델을 처음 내려받을 때 네트워크가 필요합니다.

### 분석 결과가 부정확합니다

분석 결과는 검색된 법령 조문과 LLM 응답 품질에 영향을 받습니다. 서비스 설명을 구체적으로 작성하고, 관련 조문 원문과 최신 법령을 직접 대조하세요.

## 보안 및 개인정보

- API 키와 운영 환경의 비밀값은 `.env`에만 저장하고 Git에 커밋하지 마세요.
- 실제 개인정보나 민감한 사업 정보를 테스트 입력으로 사용하지 않는 것을 권장합니다.
- 로컬 실행이라도 로그·ChromaDB·캐시 디렉터리에 입력 정보가 남을 수 있으므로 운영 환경의 접근 권한을 관리하세요.

## 라이선스

현재 저장소에는 별도 라이선스 파일이 포함되어 있지 않습니다. 재배포·상업적 이용 전 저장소 소유자에게 이용 조건을 확인하세요.

## 참고 자료

- [국가법령정보센터](https://www.law.go.kr/)
- [국가법령정보 공동활용 OPEN API](https://open.law.go.kr/)
- [Ollama](https://ollama.com/)
- [Streamlit](https://streamlit.io/)
- [Chroma](https://www.trychroma.com/)
