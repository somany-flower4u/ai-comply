# AI 컴플리 (AI Comply)

법제처 법령데이터 기반 **「Agentic RAG 모델 개발」** 과제 참가 코드입니다. 서비스 정보를 입력하면 「인공지능 발전과 신뢰 기반 조성 등에 관한 기본법」(AI 기본법)에 비추어 사업자 유형, 고영향 AI 해당 가능성, 준수 의무를 점검하는 Streamlit 앱입니다.

법령은 국가법령정보센터 OPEN API로 수집해 조문 단위로 ChromaDB에 저장합니다. 분석은 에이전트 3개가 순서대로 맡고, 각 에이전트는 관련 조문을 검색한 뒤 로컬 Ollama 모델에 넘겨 답을 만듭니다.

> English summary: a Streamlit RAG app for the Korean AI Basic Act. It collects statutes from the National Law Information Center API, stores article-level chunks in ChromaDB (ko-sroberta-multitask embeddings), and runs three agents (operator type, high-impact AI, obligations) on a local Ollama LLM. It is a pre-check aid, not legal advice.

이 도구는 법률 정보 탐색과 사전 점검용입니다. 법률 자문이나 규제기관의 공식 판단을 대체하지 않습니다.

## 주요 기능

서비스명, 서비스 설명, AI 유형, 산업 분야, 개발 방식, 대상 사용자, 데이터 활용 여부, 개발 단계를 입력하면 에이전트 3개가 차례로 분석합니다. 서비스명, 서비스 설명, 개발 방식은 필수 입력입니다.

1. **분류 에이전트** (`agents/classifier_agent.py`): AI 개발자, AI 서비스제공자, AI 이용자, 생성형 AI 사업자 중 어디에 해당하는지 분류합니다.
2. **고영향 AI 에이전트** (`agents/high_impact_agent.py`): 의료, 금융, 채용, 법집행, 주요기반시설, 교육 분야와 기본권 영향을 바탕으로 위험도를 분석합니다.
3. **의무사항 에이전트** (`agents/obligation_agent.py`): 투명성, 안전성, 이용자 보호, 고영향 AI, 영향평가, 개인정보 관련 의무를 정리합니다.

세 에이전트는 `agents/base_agent.py`의 공통 클래스를 상속합니다. 이 클래스가 벡터 저장소 검색과 Ollama 호출을 맡습니다.

앱은 탭 4개로 구성됩니다.

| 탭 | 내용 |
|---|---|
| 서비스 정보 입력 | 진단에 필요한 정보를 입력하고 분석을 시작합니다. |
| 진단 결과 | 사업자 유형, 고영향 AI 분석, 관련 조문을 보여 줍니다. |
| 체크리스트 | 준수 항목 체크리스트를 보여 줍니다. |
| 법령 검색 | 키워드로 조문을 검색합니다. |

## 처리 흐름

```text
사용자 입력 (app.py)
  -> 법령 벡터 검색: ChromaDB + jhgan/ko-sroberta-multitask
  -> Ollama LLM + 에이전트 3개 (분류, 고영향 AI, 의무사항)
  -> 진단 결과, 체크리스트, 법령 검색 결과
```

- 수집 대상 법령(`config.py`의 `TARGET_LAWS`): AI 기본법, AI 기본법 시행령, 개인정보 보호법, 개인정보 보호법 시행령, 정보통신망 이용촉진 및 정보보호 등에 관한 법률입니다.
- 청킹(`text_processor.py`): 조문 단위로 나누고, 조문이 1,500자를 넘으면 항(①) 단위로 더 나눕니다.
- 임베딩: `jhgan/ko-sroberta-multitask`
- LLM: Ollama, 기본 모델은 `shqkel/EEVE-Korean-Chat-10.8B`입니다. 외부 LLM API는 쓰지 않습니다.

## 폴더 구조

```
app.py               Streamlit UI와 진단 흐름
config.py            환경 변수, 수집 대상 법령, 진단 설정
data_collector.py    국가법령정보센터 API 수집기
text_processor.py    조문 청킹과 메타데이터 처리
vector_store.py      ChromaDB 저장, 검색, 통계
utils.py             결과 포맷팅과 보고서 유틸
agents/
  base_agent.py      RAG 검색과 Ollama 호출 공통 로직
  classifier_agent.py
  high_impact_agent.py
  obligation_agent.py
test_*.py            API, 조문 조회, 수집, 저장 확인 스크립트
requirements.txt
.env.example
run.sh, run.bat      환경 구성과 실행 스크립트
```

## 설치와 실행

필요한 것은 Python 3.11 이상, [Ollama](https://ollama.com/), 국가법령정보센터 OPEN API 인증키입니다.

1. 환경 변수 파일을 만듭니다. `.env`에서 `LAW_API_KEY`를 본인 키로 바꿉니다.

   ```bash
   cp .env.example .env
   ```

   `.env`의 `LAW_API_KEY`에 발급받은 인증키를 넣습니다. Ollama 주소와 모델은 기본값(`http://localhost:11434`, `shqkel/EEVE-Korean-Chat-10.8B`)으로 채워져 있습니다.

2. Ollama 서버를 실행하고 모델을 받습니다.

   ```bash
   ollama serve
   ollama pull shqkel/EEVE-Korean-Chat-10.8B
   ```

3. 앱을 실행합니다. `run.sh`는 가상환경 생성, 패키지 설치, Streamlit 실행을 한 번에 합니다. Windows에서는 `run.bat`을 씁니다.

   ```bash
   ./run.sh
   ```

   직접 실행하려면 다음과 같이 합니다.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. 브라우저에서 `http://localhost:8501`을 엽니다. 처음에는 벡터 저장소가 비어 있으므로 사이드바의 **데이터베이스 구축** 버튼을 눌러 법령을 수집하고 임베딩합니다. 결과는 `CHROMA_PERSIST_DIR`(기본 `./chroma_db`)에 저장됩니다.

환경 변수는 `LAW_API_KEY`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `CHROMA_PERSIST_DIR`, `CHROMA_COLLECTION_NAME`, `LOG_LEVEL`입니다. 기본값은 `config.py`에 있습니다.

`test_*.py`는 pytest 단위 테스트가 아니라 법령 API와 저장소를 직접 호출해 보는 확인용 스크립트입니다. 실행하려면 API 키와 네트워크가 필요합니다.

## 데이터

- **출처:** 국가법령정보센터(법제처) OPEN API의 법령 본문입니다.
- **저장소에 포함하지 않은 것:** 수집한 법령 원문, 임베딩, `chroma_db`. 앱에서 데이터베이스 구축을 실행하면 로컬에 만들어집니다.
- 법령 데이터의 이용 조건은 국가법령정보센터의 안내를 따릅니다.

## 라이선스

코드는 [MIT License](LICENSE)를 따릅니다. 수집한 법령 데이터는 국가법령정보센터의 이용 조건을, 임베딩 모델(`jhgan/ko-sroberta-multitask`)과 Ollama 모델(`shqkel/EEVE-Korean-Chat-10.8B`)은 각 배포처의 라이선스를 따릅니다.
