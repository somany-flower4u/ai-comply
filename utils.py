"""
유틸리티 함수 모듈 (Utils)
링크 생성, 보고서 생성, 텍스트 정제 등 공통 기능을 제공합니다.
"""

import logging
from typing import Dict, List
from datetime import datetime
from urllib.parse import quote

logger = logging.getLogger(__name__)


def format_law_link(law_name: str) -> str:
    """
    국가법령정보센터 법령 링크 생성
    
    Args:
        law_name: 법령명 (한글)
        
    Returns:
        URL 문자열
    """
    try:
        # URL 인코딩
        encoded_name = quote(law_name.encode('utf-8'))
        url = f"https://www.law.go.kr/법령/{encoded_name}"
        logger.debug(f"법령 링크 생성: {law_name} -> {url}")
        return url
    except Exception as e:
        logger.error(f"링크 생성 실패: {str(e)}")
        return "https://www.law.go.kr/"


def format_article_link(law_name: str, article_no: str) -> str:
    """
    특정 조문으로의 딥링크 생성
    
    Args:
        law_name: 법령명
        article_no: 조문번호 (예: "제2조")
        
    Returns:
        URL 문자열
    """
    try:
        encoded_name = quote(law_name.encode('utf-8'))
        # 국가법령정보센터 딥링크 형식
        # 실제 API 차용: https://www.law.go.kr/법령/법령명#조문번호
        url = f"https://www.law.go.kr/법령/{encoded_name}#{article_no}"
        return url
    except Exception as e:
        logger.error(f"딥링크 생성 실패: {str(e)}")
        return format_law_link(law_name)


def sanitize_text(text: str) -> str:
    """
    출력용 텍스트 정제
    
    Args:
        text: 원본 텍스트
        
    Returns:
        정제된 텍스트
    """
    if not text:
        return ""
    
    # 연속 공백 제거
    import re
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n\n+', '\n', text)
    
    return text.strip()


def create_diagnosis_report(
    classifier_result: Dict,
    high_impact_result: Dict,
    obligation_result: Dict
) -> str:
    """
    진단 결과를 마크다운 보고서로 변환
    
    Args:
        classifier_result: 사업자 분류 결과
        high_impact_result: 고영향AI 진단 결과
        obligation_result: 의무사항 매핑 결과
        
    Returns:
        마크다운 형식 보고서
    """
    logger.info("진단 보고서 생성 중...")
    
    report = f"""# AI 컴플리 - 진단 보고서

생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}

---

## 📋 Executive Summary

이 보고서는 귀사의 AI 서비스에 대한 한국 AI 기본법 준수 현황 진단 결과입니다.
자세한 내용은 아래 섹션을 참고하시기 바랍니다.

---

## 1️⃣ 사업자 유형 분류

### 분류 결과

**분류된 사업자 유형:**

"""
    
    operator_types = classifier_result.get('operator_types', [])
    for op_type in operator_types:
        report += f"- ✓ {op_type}\n"
    
    report += f"""
### 분류 근거

{classifier_result.get('reasoning', '분석 불가')}

### 관련 법령

"""
    
    for article in classifier_result.get('relevant_articles', []):
        report += f"""
- **{article.get('법령명')}** - {article.get('조문')} {article.get('조문제목')}
  - 시행일: {article.get('시행일자', 'N/A')}
"""
    
    report += f"""
---

## 2️⃣ 고영향 AI 진단

### 진단 결과

**고영향 AI 해당 여부:** {'✓ 해당' if high_impact_result.get('is_high_impact') else '✗ 미해당'}

**위험도 수준:** {high_impact_result.get('risk_level', '데이터 없음')}

### 위험요소 분석

"""
    
    risk_factors = high_impact_result.get('risk_factors', [])
    for factor in risk_factors:
        score = factor.get('score', 0)
        report += f"""
**{factor.get('factor', '')}** (점수: {score}/5)

{factor.get('explanation', '')}

"""
    
    report += f"""
### 진단 설명

{high_impact_result.get('reasoning', '분석 불가')}

**권장사항:** {high_impact_result.get('recommendation', '추가 상담 요청')}

---

## 3️⃣ 의무사항 체크리스트

총 {len(obligation_result.get('obligations', []))}개 의무사항이 식별되었습니다.

"""
    
    # 의무사항별 상세 정보
    for obligation in obligation_result.get('obligations', []):
        priority_mark = "🔴 [필수]" if obligation.get('priority') == '필수' else "🟡 [권장]"
        
        report += f"""
### {priority_mark} {obligation.get('category', '')} - {obligation.get('name', '')}

**설명:** {obligation.get('description', '')}

**법적 근거:**
"""
        
        for legal_basis in obligation.get('legal_basis', []):
            report += f"- {legal_basis}\n"
        
        report += f"""
**이행 주기:** {obligation.get('deadline', '지정 없음')}

**체크리스트:**
"""
        
        for item in obligation.get('checklist', []):
            report += f"- [ ] {item}\n"
        
        report += "\n"
    
    # 로드맵
    report += f"""
---

## 4️⃣ 컴플라이언스 로드맵

### 실행 계획

"""
    
    for phase in obligation_result.get('roadmap', []):
        report += f"""
#### Phase {phase.get('phase', 'N/A')}: {phase.get('title', '')}

**소요 기간:** {phase.get('duration', 'N/A')}

**실행 항목:**
"""
        
        for action in phase.get('actions', []):
            report += f"- {action}\n"
        
        report += "\n"
    
    # 관련 법령
    report += f"""
---

## 5️⃣ 관련 법령

"""
    
    for law in obligation_result.get('related_laws', []):
        report += f"""
### {law.get('law_name', '')}

**관련 조문:**
"""
        for article in law.get('articles', []):
            report += f"- {article}\n"
        
        report += f"\n**관련성:** {law.get('relevance', '')}\n\n"
    
    report += f"""
---

## 📝 종합 의견

{obligation_result.get('summary', '종합 의견 분석 중...')}

---

## 📞 추가 지원

더 자세한 상담이 필요하신 경우, 다음 기관에 문의하시기 바랍니다:

- **국가법령정보센터:** https://www.law.go.kr/
- **과학기술정보통신부:** https://www.msit.go.kr/
- **AI기본법 관련 가이드:** https://www.msit.go.kr/

---

*이 보고서는 자동 진단 시스템에 의해 생성되었습니다.*
*법적 조언은 아니며, 실제 법적 상황에 대해서는 전문가 상담을 권장합니다.*

"""
    
    logger.info("✓ 보고서 생성 완료")
    return report


def export_checklist_to_markdown(obligations: List[Dict]) -> str:
    """
    의무사항을 마크다운 체크리스트로 변환
    
    Args:
        obligations: 의무사항 리스트
        
    Returns:
        마크다운 형식 체크리스트
    """
    logger.info("체크리스트 내보내기 중...")
    
    md = """# AI 컴플라이언스 체크리스트

작성 날짜: {0}

## 체크리스트

""".format(datetime.now().strftime('%Y년 %m월 %d일'))
    
    current_category = ""
    
    for obligation in obligations:
        category = obligation.get('category', '')
        
        if category != current_category:
            md += f"\n### {category}\n\n"
            current_category = category
        
        priority = obligation.get('priority', '권장')
        priority_mark = "🔴" if priority == '필수' else "🟡"
        
        md += f"#### {priority_mark} {obligation.get('name', '')}\n\n"
        md += f"{obligation.get('description', '')}\n\n"
        
        md += "**이행 항목:**\n"
        for item in obligation.get('checklist', []):
            md += f"- [ ] {item}\n"
        
        md += f"\n**법적 근거:** {', '.join(obligation.get('legal_basis', []))}\n\n"
    
    md += """
---

## 사용 설명

이 체크리스트는 의무사항별로 정리되어 있습니다.

- 🔴 **[필수]**: 반드시 수행해야 하는 의무사항
- 🟡 **[권장]**: 권장되는 의무사항

각 항목을 체크하면서 진행 상황을 추적하세요.

"""
    
    logger.info("✓ 체크리스트 생성 완료")
    return md


def format_highlight_text(text: str, keyword: str, color: str = "yellow") -> str:
    """
    텍스트에서 키워드 하이라이트
    
    Args:
        text: 원본 텍스트
        keyword: 강조할 키워드
        color: 색상명
        
    Returns:
        HTML 형식 텍스트
    """
    import re
    
    # 키워드를 HTML span으로 감싸기
    highlighted = re.sub(
        f'({keyword})',
        f'<span style="background-color: {color};">\\1</span>',
        text,
        flags=re.IGNORECASE
    )
    
    return highlighted


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """
    텍스트 읽는 시간 추정 (분 단위)
    
    Args:
        text: 텍스트
        wpm: 분당 단어 수 (기본값: 200)
        
    Returns:
        추정 시간 (분)
    """
    words = len(text.split())
    minutes = max(1, words // wpm)
    return minutes


def get_progress_percentage(completed: int, total: int) -> int:
    """
    진행률 계산
    
    Args:
        completed: 완료한 항목 수
        total: 전체 항목 수
        
    Returns:
        진행률 (0-100)
    """
    if total == 0:
        return 0
    return min(100, (completed * 100) // total)


if __name__ == "__main__":
    # 테스트
    print("유틸리티 함수 테스트")
    
    # 링크 테스트
    link = format_law_link("인공지능 발전과 신뢰 기반 조성 등에 관한 기본법")
    print(f"법령 링크: {link}")
    
    # 텍스트 정제 테스트
    text = "이것은  \n\n   테스트 문자열입니다."
    clean = sanitize_text(text)
    print(f"정제 결과: {clean}")
