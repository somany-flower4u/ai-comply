"""
의무사항 매핑 에이전트 (Obligation Mapping Agent)
사업자 유형과 고영향AI 여부에 따라 준수 의무사항을 매핑합니다.
"""

import json
import logging
from typing import Dict, List
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ObligationAgent(BaseAgent):
    """
    의무사항 에이전트
    AI 기본법 및 관련 법령에 따른 준수 의무사항을 진단하고 로드맵을 제시합니다.
    """

    def __init__(self, vector_store, llm_config=None):
        """초기화"""
        super().__init__(vector_store, llm_config)
        logger.info("ObligationAgent 초기화 완료")

    def map_obligations(
        self,
        user_input: Dict,
        operator_types: List[str],
        high_impact_result: Dict
    ) -> Dict:
        """
        의무사항 매핑
        
        Args:
            user_input: 사용자 정보
            operator_types: 분류된 사업자 유형
            high_impact_result: 고영향AI 진단 결과
            
        Returns:
            의무사항 및 로드맵
            {
                "obligations": list[dict],
                "roadmap": list[dict],
                "related_laws": list[dict],
                "summary": str
            }
        """
        logger.info("=" * 60)
        logger.info("의무사항 매핑 시작")
        logger.info("=" * 60)
        
        try:
            # 1단계: 컨텍스트 검색
            logger.info("\n[1단계] 관련 법령 검색 중...")
            context, search_results = self._retrieve_context(
                "의무 투명성 안전성 이용자 보호 개인정보 영향평가 벌칙",
                n_results=10
            )
            
            # 2단계: 프롬프트 구성
            logger.info("[2단계] LLM 호출 중...")
            is_high_impact = high_impact_result.get("is_high_impact", False)
            
            system_prompt = """당신은 AI 기본법 및 관련 법령 전문가입니다.
사업자 유형과 고영향AI 여부에 따라 준수해야 할 의무사항을 매핑합니다.

의무사항 카테고리:
1. 투명성 확보 의무: 데이터, 개발 과정, 성능 정보 공개
2. 안전성 확보 의무: 오작동/오류 방지, 위험 평가
3. 이용자 보호 의무: 의사결정 공개, 설명 제공, 배상책임
4. 고영향AI 특별 의무: 영향평가, 모니터링, 보고
5. AI 영향평가 의무: 고영향AI의 필수 평가
6. 개인정보 관련 의무: PIPA 준수

각 의무사항마다:
- 법적 근거 (관련 조문)
- 우선순위 (필수/권장)
- 수행 주기
- 구체적 체크리스트 항목

항상 한국어로, 실행 가능한 구체적 조언을 제공하세요."""

            user_prompt = f"""다음 AI 서비스에 대한 준수 의무사항을 매핑해주세요:

서비스명: {user_input.get('service_name', '')}
사업자 유형: {', '.join(operator_types)}
고영향AI 해당: {is_high_impact}
위험도: {high_impact_result.get('risk_level', '저위험')}
산업분야: {user_input.get('industry_sector', '')}
개인정보 포함: {'예' if '개인정보 포함 데이터' in user_input.get('data_usage', []) else '아니오'}

다음 JSON 형식으로 응답하세요:
{{
  "obligations": [
    {{
      "category": "의무 카테고리",
      "name": "의무사항명",
      "description": "상세 설명",
      "legal_basis": ["제XX조", "제XX조"],
      "priority": "필수/권장",
      "deadline": "이행 주기",
      "checklist": ["구체적 실행 항목1", "구체적 실행 항목2", ...]
    }},
    ...
  ],
  "roadmap": [
    {{
      "phase": 1,
      "title": "단계 제목",
      "duration": "소요 기간",
      "actions": ["구체적 실행 항목1", ...]
    }},
    ...
  ],
  "related_laws": [
    {{
      "law_name": "법령명",
      "articles": ["제XX조"],
      "relevance": "관련성 설명"
    }},
    ...
  ],
  "summary": "종합 요약 및 권장사항"
}}"""

            # 3단계: LLM 호출
            response = self._generate(system_prompt, user_prompt, context)
            
            # 4단계: 응답 파싱
            logger.info("[3단계] 응답 분석 중...")
            parsed = self._parse_llm_response(response)
            
            # 5단계: 출처 추출
            references = self._format_source_references(search_results)
            
            # 참고 법령 추가
            related_laws = parsed.get("related_laws", [])
            for ref in references:
                # 중복 확인
                if not any(law['law_name'] == ref['법령명'] for law in related_laws):
                    related_laws.append({
                        "law_name": ref['법령명'],
                        "articles": [ref['조문']],
                        "relevance": "검색 결과"
                    })
            
            # 결과 구성
            result = {
                "obligations": parsed.get("obligations", []),
                "roadmap": parsed.get("roadmap", []),
                "related_laws": related_laws,
                "summary": parsed.get("summary", response)
            }
            
            logger.info(f"✓ 의무사항 매핑 완료: {len(result['obligations'])}개 의무사항")
            logger.info(f"  - 로드맵 단계: {len(result['roadmap'])}개")
            logger.info("=" * 60)
            
            return result
        
        except Exception as e:
            logger.error(f"의무사항 매핑 실패: {str(e)}", exc_info=True)
            return {
                "obligations": [],
                "roadmap": [],
                "related_laws": [],
                "summary": f"의무사항 매핑 실패: {str(e)}"
            }

    def get_obligation_priority_icon(self, priority: str) -> str:
        """
        우선순위별 아이콘 반환
        
        Args:
            priority: 우선순위 ("필수" 또는 "권장")
            
        Returns:
            아이콘 문자열
        """
        if priority == "필수":
            return "🔴"  # 빨강
        elif priority == "권장":
            return "🟡"  # 노랑
        else:
            return "⚪"  # 회색

    def get_obligation_category_color(self, category: str) -> str:
        """
        의무 카테고리별 색상 반환
        
        Args:
            category: 의무 카테고리
            
        Returns:
            색상 코드 (16진수)
        """
        colors = {
            "투명성 확보 의무": "#4CAF50",
            "안전성 확보 의무": "#2196F3",
            "이용자 보호 의무": "#FF9800",
            "고영향AI 특별 의무": "#F44336",
            "AI 영향평가 의무": "#9C27B0",
            "개인정보 관련 의무": "#00BCD4"
        }
        
        return colors.get(category, "#9E9E9E")

    def generate_checklist(self, obligations: List[Dict]) -> List[Dict]:
        """
        의무사항을 체크리스트로 변환
        
        Args:
            obligations: 의무사항 리스트
            
        Returns:
            체크리스트 항목
        """
        checklist = []
        
        for obligation in obligations:
            category = obligation.get("category", "기타")
            name = obligation.get("name", "")
            items = obligation.get("checklist", [])
            priority = obligation.get("priority", "권장")
            
            for i, item in enumerate(items):
                checklist.append({
                    "id": f"{len(checklist) + 1:03d}",
                    "category": category,
                    "obligation": name,
                    "item": item,
                    "priority": priority,
                    "completed": False,
                    "notes": ""
                })
        
        return checklist

    def estimate_workload(self, obligations: List[Dict]) -> Dict:
        """
        의무사항 이행에 필요한 업무량 추정
        
        Args:
            obligations: 의무사항 리스트
            
        Returns:
            업무량 추정 정보
        """
        total_items = sum(len(o.get("checklist", [])) for o in obligations)
        essential_items = sum(
            len(o.get("checklist", [])) 
            for o in obligations 
            if o.get("priority") == "필수"
        )
        
        # 대략적 추정 (실제로는 더 복잡한 계산 필요)
        estimated_weeks = max(1, (total_items // 5))
        
        return {
            "total_checklist_items": total_items,
            "essential_items": essential_items,
            "recommended_items": total_items - essential_items,
            "estimated_weeks": estimated_weeks,
            "estimated_months": max(1, (estimated_weeks // 4)),
            "team_size_estimate": max(1, (total_items // 10))
        }
