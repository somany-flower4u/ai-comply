"""
고영향 AI 진단 에이전트 (High-Impact AI Diagnosis Agent)
서비스가 '고영향 AI'에 해당하는지 진단합니다.
"""

import json
import logging
from typing import Dict, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class HighImpactAgent(BaseAgent):
    """
    고영향 AI 진단 에이전트
    
    고영향 AI: AI Basic Law Article 33
    "그 오작동이나 오류로 인하여 시민의 기본권을 침해할 가능성이 높은 인공지능"
    """

    def __init__(self, vector_store, llm_config=None):
        """초기화"""
        super().__init__(vector_store, llm_config)
        logger.info("HighImpactAgent 초기화 완료")

    def diagnose(
        self,
        user_input: Dict,
        operator_types: List[str]
    ) -> Dict:
        """
        고영향 AI 진단 수행
        
        Args:
            user_input: 사용자 정보
            operator_types: 분류된 사업자 유형
            
        Returns:
            진단 결과
            {
                "is_high_impact": bool,
                "risk_level": str,
                "risk_factors": list[dict],
                "relevant_articles": list[dict],
                "reasoning": str
            }
        """
        logger.info("=" * 60)
        logger.info("고영향 AI 진단 시작")
        logger.info("=" * 60)
        
        try:
            # 1단계: 컨텍스트 검색
            logger.info("\n[1단계] 관련 법령 검색 중...")
            context, search_results = self._retrieve_context(
                "고영향 인공지능 위험도 평가 영향평가 기본권 침해",
                n_results=8,
                category_filter="고영향AI"
            )
            
            # 2단계: 프롬프트 구성
            logger.info("[2단계] LLM 호출 중...")
            system_prompt = """당신은 AI 기본법 고영향 AI 진단 전문가입니다.
사용자 정보를 분석하여 그 AI 서비스가 '고영향 AI'에 해당하는지 판단합니다.

고영향 AI의 정의 (Article 33):
"그 오작동이나 오류로 인하여 시민의 기본권을 침해할 가능성이 높은 인공지능"

평가 기준:
1. 사용 영역 (Usage Domain):
   - 의료/헬스케어: 진단, 치료결정
   - 금융/보험: 신용평가, 대출심사
   - 채용/인사: 채용결정, 평가
   - 법집행/사법: 수사, 기소, 판결 보조
   - 주요 기반시설: 전기, 수도, 통신
   - 교육: 성적평가, 진로지도
   
2. 기본권 영향:
   - 생명권, 신체권 (매우 높음)
   - 인격권, 사생활권 (높음)
   - 재산권, 직업의 자유 (중간)
   
3. 중대성: 오류 발생 시 피해 정도
4. 빈도: 의사결정 빈도
5. 대체 가능성: 인간 심사 가능 여부

위험 등급:
- 고위험 (High): 기본권 침해 가능성 높음
- 중위험 (Medium): 기본권 침해 가능성 중간
- 저위험 (Low): 기본권 침해 가능성 낮음

항상 한국어로 응답하세요."""

            user_prompt = f"""다음 AI 서비스에 대해 고영향 AI 여부를 진단해주세요:

서비스명: {user_input.get('service_name', '')}
서비스 설명: {user_input.get('service_description', '')}
AI 유형: {user_input.get('ai_type', '')}
산업 분야: {user_input.get('industry_sector', '')}
서비스 대상: {', '.join(user_input.get('target_users', []))}
의사결정 영향: {user_input.get('decision_impact', '심사 중')}
개인정보 활용: {user_input.get('data_usage', [])}
사업자 유형: {', '.join({operator_types})}

다음 JSON 형식으로 응답하세요:
{{
  "is_high_impact": true/false,
  "risk_level": "고위험/중위험/저위험",
  "risk_factors": [
    {{
      "factor": "위험요소명",
      "score": 1-5,
      "explanation": "설명"
    }},
    ...
  ],
  "reasoning": "상세한 진단 이유",
  "recommendation": "권장사항"
}}"""

            # 3단계: LLM 호출
            response = self._generate(system_prompt, user_prompt, context)
            
            # 4단계: 응답 파싱
            logger.info("[3단계] 응답 분석 중...")
            parsed = self._parse_llm_response(response)
            
            # 5단계: 출처 추출
            references = self._format_source_references(search_results)
            
            # 결과 구성
            is_high_impact = parsed.get("is_high_impact", False)
            risk_level = parsed.get("risk_level", "저위험")
            
            result = {
                "is_high_impact": is_high_impact,
                "risk_level": risk_level,
                "risk_factors": parsed.get("risk_factors", []),
                "relevant_articles": references,
                "reasoning": parsed.get("reasoning", response),
                "recommendation": parsed.get("recommendation", "")
            }
            
            logger.info(f"✓ 진단 완료: 고영향AI={is_high_impact}, 위험도={risk_level}")
            logger.info("=" * 60)
            
            return result
        
        except Exception as e:
            logger.error(f"진단 중 오류: {str(e)}", exc_info=True)
            return {
                "is_high_impact": False,
                "risk_level": "저위험",
                "risk_factors": [],
                "relevant_articles": [],
                "reasoning": f"진단 실패: {str(e)}",
                "recommendation": ""
            }

    def get_risk_level_info(self, risk_level: str) -> Dict:
        """
        위험도 레벨 정보 조회
        
        Args:
            risk_level: 위험도 레벨 문자열
            
        Returns:
            UI용 정보
        """
        risk_info = {
            "고위험": {
                "color": "red",
                "icon": "🚨",
                "description": "기본권 침해 가능성이 높습니다. 강력한 규제가 필요합니다.",
                "priority": "최상"
            },
            "중위험": {
                "color": "orange",
                "icon": "⚠️",
                "description": "기본권 침해 가능성이 있습니다. 중점 관리가 필요합니다.",
                "priority": "높음"
            },
            "저위험": {
                "color": "green",
                "icon": "✅",
                "description": "기본권 침해 가능성이 낮습니다. 기초 준수만으로 충분합니다.",
                "priority": "중간"
            }
        }
        
        return risk_info.get(risk_level, {
            "color": "gray",
            "icon": "❓",
            "description": "위험도 정보 확인 실패",
            "priority": "확인 필요"
        })

    def _calculate_risk_score(self, risk_factors: List[Dict]) -> float:
        """
        위험요소 점수 계산
        
        Args:
            risk_factors: 위험요소 리스트
            
        Returns:
            종합 위험 점수 (0-5)
        """
        if not risk_factors:
            return 0.0
        
        scores = [rf.get("score", 0) for rf in risk_factors]
        average_score = sum(scores) / len(scores)
        
        return round(average_score, 1)
