"""
기본 에이전트 클래스 (Base Agent)
모든 진단 에이전트가 상속받는 기본 클래스로 RAG 로직을 제공합니다.
"""

import json
import logging
from typing import Dict, List, Optional
from langchain_community.llms import Ollama
from vector_store import LegalVectorStore

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agents.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BaseAgent:
    """모든 에이전트의 기본 클래스"""

    def __init__(self, vector_store: LegalVectorStore, llm_config: Optional[Dict] = None):
        """
        기본 에이전트 초기화
        
        Args:
            vector_store: LegalVectorStore 인스턴스
            llm_config: LLM 설정 (선택)
        """
        self.vector_store = vector_store
        
        # LLM 설정 (기본값)
        if llm_config is None:
            llm_config = {}
        
        from config import OLLAMA_BASE_URL, OLLAMA_MODEL
        import requests
        
        # Ollama 서버 연결 확인
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"{llm_config.get('base_url', OLLAMA_BASE_URL)}/api/tags",
                    timeout=5
                )
                if response.status_code == 200:
                    logger.info("✓ Ollama 서버 연결 확인 완료")
                    break
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    logger.warning(f"Ollama 연결 시도 {attempt + 1}/{max_retries} 실패, 재시도 중...")
                    import time
                    time.sleep(2)
                else:
                    logger.error("⚠️  Ollama 서버에 연결할 수 없습니다. Ollama가 실행 중인지 확인하세요.")
        
        self.llm = Ollama(
            base_url=llm_config.get('base_url', OLLAMA_BASE_URL),
            model=llm_config.get('model', OLLAMA_MODEL),
            temperature=llm_config.get('temperature', 0.3),
            top_k=llm_config.get('top_k', 40),
            top_p=llm_config.get('top_p', 0.9),
            timeout=120.0,  # 타임아웃을 120초로 설정 (모델 로딩 시간 고려)
        )
        
        logger.info(f"{self.__class__.__name__} 초기화 완료")

    def _retrieve_context(
        self,
        query: str,
        n_results: int = 5,
        category_filter: Optional[str] = None
    ) -> tuple[str, List[Dict]]:
        """
        벡터 저장소에서 컨텍스트 검색
        
        Args:
            query: 검색 쿼리
            n_results: 반환할 결과 개수
            category_filter: 카테고리 필터 (선택)
            
        Returns:
            (컨텍스트 문자열, 검색 결과)
        """
        logger.info(f"컨텍스트 검색: {query}")
        
        try:
            # 벡터 저장소 검색
            if category_filter:
                search_results = self.vector_store.search_by_category(
                    query, category_filter, n_results
                )
            else:
                search_results = self.vector_store.search(query, n_results)
            
            # 컨텍스트 포매팅
            context = ""
            for i, result in enumerate(search_results, 1):
                metadata = result.get('metadata', {})
                law_name = metadata.get('law_name', '')
                article_no = metadata.get('article_no', '')
                article_title = metadata.get('article_title', '')
                content = result.get('content', '')
                
                context += f"""
[{i}] 법령: {law_name}
    조문: {article_no} {article_title}
    내용: {content}
---"""
            
            logger.info(f"✓ {len(search_results)}개 결과 검색됨")
            return context.strip(), search_results
        
        except Exception as e:
            logger.error(f"컨텍스트 검색 오류: {str(e)}")
            return "", []

    def _generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = ""
    ) -> str:
        """
        LLM으로 응답 생성
        
        Args:
            system_prompt: 시스템 프롬프트
            user_prompt: 사용자 프롬프트
            context: RAG 컨텍스트
            
        Returns:
            LLM 응답
        """
        logger.info(f"LLM 호출 중 ({self.__class__.__name__})...")
        
        try:
            # 전체 프롬프트 구성
            if context:
                full_prompt = f"""{system_prompt}

[참고 법령]
{context}

{user_prompt}"""
            else:
                full_prompt = f"""{system_prompt}

{user_prompt}"""
            
            # LLM 호출
            response = self.llm.invoke(full_prompt)
            
            logger.info(f"✓ LLM 응답 생성 완료 (길이: {len(response)})")
            return response.strip()
        
        except Exception as e:
            logger.error(f"LLM 호출 오류: {str(e)}")
            raise

    def _format_source_references(self, search_results: List[Dict]) -> List[Dict]:
        """
        검색 결과를 출처 참고로 포매팅
        
        Args:
            search_results: 검색 결과 리스트
            
        Returns:
            포매팅된 출처 리스트
        """
        references = []
        
        for result in search_results:
            metadata = result.get('metadata', {})
            reference = {
                "법령명": metadata.get('law_name', ''),
                "조문": metadata.get('article_no', ''),
                "조문제목": metadata.get('article_title', ''),
                "시행일자": metadata.get('enforcement_date', ''),
                "법령유형": metadata.get('law_type', ''),
            }
            
            # 중복 제거
            if reference not in references:
                references.append(reference)
        
        return references

    def _parse_llm_response(self, response: str) -> Dict:
        """
        LLM 응답 파싱 (JSON 또는 텍스트)
        
        Args:
            response: LLM 응답
            
        Returns:
            파싱된 응답
        """
        import re
        
        try:
            response_stripped = response.strip()
            logger.info(f"응답 파싱 시도 (길이: {len(response_stripped)}자)")
            
            # 1단계: Markdown 코드블록에서 JSON 추출
            json_code_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response, re.DOTALL)
            if json_code_match:
                json_str = json_code_match.group(1).strip()
                logger.info(f"Markdown JSON 블록 감지, 추출 시도")
                try:
                    parsed = json.loads(json_str)
                    logger.info("✓ JSON 파싱 성공 (Markdown 블록)")
                    return parsed
                except json.JSONDecodeError as e:
                    logger.warning(f"Markdown 블록 파싱 실패: {str(e)[:100]}")
            
            # 2단계: 직접 JSON 파싱 (응답이 JSON으로 시작하는 경우)
            if response_stripped.startswith('{') and response_stripped.endswith('}'):
                try:
                    parsed = json.loads(response_stripped)
                    logger.info("✓ JSON 파싱 성공 (직접)")
                    return parsed
                except json.JSONDecodeError as e:
                    logger.warning(f"직접 파싱 실패: {str(e)[:100]}")
            
            # 3단계: 응답 내 JSON 블록 찾기
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                logger.info(f"JSON 블록 범위 감지: [{json_start}:{json_end}] (길이: {len(json_str)}자)")
                
                # 3-1: 직접 파싱 시도
                try:
                    parsed = json.loads(json_str)
                    logger.info("✓ JSON 파싱 성공 (블록 검출)")
                    return parsed
                except json.JSONDecodeError as e:
                    logger.warning(f"블록 파싱 실패 (1차): {str(e)[:100]}")
                    
                    # 3-2: 줄바꿈 제거하고 재시도
                    json_cleaned = json_str.replace('\n', ' ').replace('  ', ' ')
                    try:
                        parsed = json.loads(json_cleaned)
                        logger.info("✓ JSON 파싱 성공 (줄바꿈 제거 후)")
                        return parsed
                    except json.JSONDecodeError:
                        logger.warning(f"블록 파싱 실패 (2차)")
                        
                        # 3-3: 마지막 쉼표 제거 시도 (일반적인 오류)
                        json_comma_fix = re.sub(r',\s*}', '}', json_str)
                        json_comma_fix = re.sub(r',\s*]', ']', json_comma_fix)
                        try:
                            parsed = json.loads(json_comma_fix)
                            logger.info("✓ JSON 파싱 성공 (쉼표 제거 후)")
                            return parsed
                        except json.JSONDecodeError:
                            logger.warning(f"블록 파싱 실패 (3차)")
                            pass
        
        except Exception as e:
            logger.warning(f"응답 파싱 중 예상 오류: {str(e)}")
        
        # 파싱 실패 - 로그 기록 및 원본 응답 반환
        logger.error(f"JSON 파싱 완전 실패. 응답 일부:\n{response[:300]}...")
        
        return {
            "error": "JSON parsing failed",
            "raw_response": response,
            "is_high_impact": False,
            "risk_level": "저위험",
            "risk_factors": [],
            "reasoning": response[:500] if response else "응답이 없습니다.",
            "recommendation": "",
            "operator_types": [],
            "confidence": "낮음"
        }
