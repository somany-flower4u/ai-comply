"""
사업자 유형 분류 에이전트 (Classifier Agent)
사용자의 AI 서비스를 AI 기본법 내 사업자 유형으로 분류합니다.
"""

import json
import logging
from typing import Dict, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ClassifierAgent(BaseAgent):
    """
    AI 사업자 유형 분류 에이전트
    
    AI 기본법 제2조의 사업자 유형:
    - 인공지능 개발자 (AI Developer)
    - 인공지능 서비스제공자 (AI Service Provider)
    - 인공지능 이용자 (AI User)
    - 생성형 인공지능 사업자 (Generative AI Operator)
    """

    def __init__(self, vector_store, llm_config=None):
        """초기화"""
        super().__init__(vector_store, llm_config)
        logger.info("ClassifierAgent 초기화 완료")

    def classify(self, user_input: Dict) -> Dict:
        """
        사용자 입력을 기반으로 AI 사업자 유형 분류
        
        Args:
            user_input: 사용자 정보
            {
                "service_name": str,
                "service_description": str,
                "ai_type": str,
                "development_method": list,
                "target_users": list,
                "industry_sector": str,
                "data_usage": list,
                "development_stage": str
            }
            
        Returns:
            분류 결과
            {
                "operator_types": list[str],
                "reasoning": str,
                "relevant_articles": list[dict],
                "confidence": str
            }
        """
        logger.info("=" * 60)
        logger.info("AI 사업자 유형 분류 시작")
        logger.info("=" * 60)
        
        try:
            # 1단계: 컨텍스트 검색
            logger.info("\n[1단계] 관련 법령 검색 중...")
            context, search_results = self._retrieve_context(
                "인공지능 개발자 서비스제공자 사업자 유형 정의",
                n_results=5,
                category_filter="정의"
            )
            
            # 2단계: 프롬프트 구성
            logger.info("[2단계] LLM 호출 중...")
            system_prompt = """당신은 한국의 AI 기본법 전문가입니다.
사용자가 제공한 AI 서비스 정보를 분석하여, AI 기본법 제2조에 따른 사업자 유형을 분류합니다.

분류 가능한 유형:
1. 인공지능 개발자: 인공지능을 개발하는 자
2. 인공지능 서비스제공자: 인공지능을 활용한 서비스를 제공하는 자
3. 인공지능 이용자: 인공지능 또는 이를 활용한 서비스를 이용하는 자
4. 생성형 인공지능 사업자: 생성형 인공지능을 개발 및 제공하는 자

주의:
- 한 법인이 여러 유형의 사업자일 수 있습니다.
- 법적 정의를 정확히 적용하세요.
- 항상 한국어로 응답하세요."""

            user_prompt = f"""다음 AI 서비스에 대해 사업자 유형을 분류해주세요:

서비스명: {user_input.get('service_name', '')}
서비스 설명: {user_input.get('service_description', '')}
AI 유형: {user_input.get('ai_type', '')}
개발 방식: {', '.join(user_input.get('development_method', []))}
서비스 대상: {', '.join(user_input.get('target_users', []))}
산업 분야: {user_input.get('industry_sector', '')}
데이터 활용: {', '.join(user_input.get('data_usage', []))}
개발 단계: {user_input.get('development_stage', '')}

===== 반드시 아래의 JSON 형식으로만 응답하세요. 다른 텍스트는 절대 포함하지 마세요. =====
{{
  "operator_types": ["분류된 유형1", "분류된 유형2"],
  "reasoning": "상세한 분류 이유",
  "confidence": "높음" 또는 "중간" 또는 "낮음",
  "key_factors": ["주요 고려 요소1", "주요 고려 요소2"]
}}
===== 위의 JSON만 응답하세요. 추가 설명은 하지 마세요. ===="""

            # 3단계: LLM 호출
            response = self._generate(system_prompt, user_prompt, context)
            
            # 4단계: 응답 파싱
            logger.info("[3단계] 응답 분석 중...")
            parsed = self._parse_llm_response(response)
            
            # 5단계: 출처 추출
            references = self._format_source_references(search_results)
            
            # 결과 구성
            result = {
                "operator_types": parsed.get("operator_types", []),
                "reasoning": parsed.get("reasoning", response),
                "relevant_articles": references,
                "confidence": parsed.get("confidence", "중간"),
                "key_factors": parsed.get("key_factors", [])
            }
            
            logger.info(f"✓ 분류 완료: {', '.join(result['operator_types'])}")
            logger.info(f"  신뢰도: {result['confidence']}")
            logger.info("=" * 60)
            
            return result
        
        except Exception as e:
            logger.error(f"분류 중 오류: {str(e)}", exc_info=True)
            return {
                "operator_types": [],
                "reasoning": f"분류 실패: {str(e)}",
                "relevant_articles": [],
                "confidence": "낮음",
                "key_factors": []
            }

    def _format_result_for_ui(self, result: Dict) -> Dict:
        """
        UI 표시용으로 결과 포매팅
        
        Args:
            result: 분류 결과
            
        Returns:
            UI용 포매팅된 결과
        """
        operator_type_map = {
            "인공지능 개발자": {
                "badge_color": "blue",
                "icon": "🔧",
                "description": "AI 시스템을 개발하는 주체"
            },
            "인공지능 서비스제공자": {
                "badge_color": "green",
                "icon": "🚀",
                "description": "AI 기반 서비스를 제공하는 주체"
            },
            "인공지능 이용자": {
                "badge_color": "purple",
                "icon": "👥",
                "description": "AI 서비스를 사용하는 주체"
            },
            "생성형 인공지능 사업자": {
                "badge_color": "orange",
                "icon": "✨",
                "description": "생성형 AI를 개발/제공하는 주체"
            }
        }
        
        formatted_types = []
        for op_type in result.get("operator_types", []):
            info = operator_type_map.get(op_type, {"badge_color": "gray", "icon": "?", "description": ""})
            formatted_types.append({
                "type": op_type,
                **info
            })
        
        return {
            **result,
            "formatted_types": formatted_types
        }
