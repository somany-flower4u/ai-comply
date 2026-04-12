"""
텍스트 전처리 및 청킹 모듈 (Legal Text Processor)
한국 법령 문서를 전처리하고 조문 단위로 청킹합니다.
"""

import logging
import re
from typing import Dict, List
from config import CHUNK_SIZE, CHUNK_SEPARATOR, CATEGORY_KEYWORDS

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('text_processor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LegalTextProcessor:
    """법령 텍스트 전처리 및 청킹 클래스"""

    def __init__(self):
        """초기화"""
        logger.info("LegalTextProcessor 초기화 완료")

    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        조문들을 처리하고 청킹
        
        Args:
            articles: 조문 리스트
            
        Returns:
            청크 리스트
        """
        logger.info(f"조문 처리 시작: {len(articles)}개 조문")
        
        chunks = []
        
        for article in articles:
            try:
                # 각 조문을 청킹
                article_chunks = self.chunk_article(article)
                chunks.extend(article_chunks)
            except Exception as e:
                logger.warning(f"조문 처리 오류 ({article.get('article_no')}): {str(e)}")
                continue
        
        logger.info(f"총 {len(chunks)}개 청크 생성 완료")
        return chunks

    def chunk_article(self, article: Dict) -> List[Dict]:
        """
        조문을 청크로 분할
        
        전략:
        - 기본: 각 조문을 하나의 청크로 유지 (법적 자연단위)
        - 1500자 초과: 항(①②③...)으로 추가 분할
        
        Args:
            article: 조문 딕셔너리
            
        Returns:
            청크 리스트
        """
        law_name = article.get('law_name', '')
        law_id = article.get('law_id', '')
        article_no = article.get('article_no', '')
        content = article.get('article_content', '')
        
        # 내용이 청크 크기 이하면 그대로 반환
        if len(content) <= CHUNK_SIZE:
            chunk = article.copy()
            chunk['chunk_id'] = self.create_chunk_id(law_id, law_name, article_no, "")
            chunk['paragraph_no'] = ""
            chunk = self.enrich_metadata(chunk)
            return [chunk]
        
        # 1500자 초과: 항(①②③...)으로 분할
        chunks = []
        paragraphs = self._split_by_paragraphs(content, article_no)
        
        for para_no, para_content in paragraphs:
            chunk = article.copy()
            chunk['article_content'] = para_content.strip()
            chunk['paragraph_no'] = para_no
            chunk['chunk_id'] = self.create_chunk_id(law_id, law_name, article_no, para_no)
            chunk = self.enrich_metadata(chunk)
            chunks.append(chunk)
        
        logger.debug(f"조문 분할: {article_no} -> {len(chunks)}개 청크")
        return chunks

    def _split_by_paragraphs(self, content: str, article_no: str) -> List[tuple]:
        """
        항(①②③...)으로 텍스트 분할
        
        Args:
            content: 조문 내용
            article_no: 조문번호
            
        Returns:
            (항번호, 항내용) 튜플 리스트
        """
        # 항 분리 패턴 (①②③④⑤⑥⑦⑧⑨⑩...)
        paragraph_pattern = r'(①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮|⑯|⑰|⑱|⑲|⑳)'
        
        paragraphs = []
        
        # 항이 없으면 전체를 하나로
        if not re.search(paragraph_pattern, content):
            return [("", content)]
        
        # 항으로 분할
        parts = re.split(f'({paragraph_pattern})', content)
        
        # parts는 [텍스트, 항기호, 텍스트, 항기호, ...] 형태
        current_para = ""
        current_content = ""
        
        for i, part in enumerate(parts):
            if not part.strip():
                continue
            
            if re.match(paragraph_pattern, part):
                # 항 기호를 만남
                if current_para:
                    # 이전 항 저장
                    paragraphs.append((current_para, current_content.strip()))
                
                current_para = part
                current_content = ""
            else:
                # 항 내용
                current_content += part
        
        # 마지막 항 저장
        if current_para:
            paragraphs.append((current_para, current_content.strip()))
        
        return paragraphs if paragraphs else [("", content)]

    def create_chunk_id(self, law_id: str, law_name: str, article_no: str, paragraph_no: str) -> str:
        """
        고유한 청크 ID 생성
        
        형식: {법령ID}_{조문번호}_{항번호}_{UUID}
        """
        import uuid
        
        # law_id가 있으면 사용, 없으면 법령명 해시 사용
        if law_id:
            law_prefix = law_id
        else:
            import hashlib
            law_prefix = hashlib.md5(law_name.encode()).hexdigest()[:6]
        
        article_clean = article_no.replace("제", "").replace("조", "").strip()
        
        # UUID를 짧게 줄임 (처음 8자)
        unique_suffix = str(uuid.uuid4())[:8]
        
        if paragraph_no:
            para_clean = paragraph_no.strip()
            chunk_id = f"{law_prefix}_{article_clean}_{para_clean}_{unique_suffix}"
        else:
            chunk_id = f"{law_prefix}_{article_clean}_{unique_suffix}"
        
        return chunk_id

    def enrich_metadata(self, chunk: Dict) -> Dict:
        """
        청크에 메타데이터 추가
        
        추가 항목:
        - category: 카테고리 (정의, 의무, 벌칙, 고영향AI, 투명성, 안전성)
        - related_articles: 관련 조문 참조
        - keywords: 핵심 법률용어
        
        Args:
            chunk: 청크 딕셔너리
            
        Returns:
            메타데이터가 추가된 청크
        """
        content = chunk.get('article_content', '')
        
        # 카테고리 분류
        category = self._classify_category(content)
        chunk['category'] = category
        
        # 관련 조문 추출
        related_articles = self._extract_related_articles(content)
        chunk['related_articles'] = related_articles
        
        # 핵심 용어 추출
        keywords = self._extract_keywords(content)
        chunk['keywords'] = keywords
        
        # 청크 길이 추가
        chunk['content_length'] = len(content)
        
        return chunk

    def _classify_category(self, content: str) -> List[str]:
        """
        키워드 기반 카테고리 분류
        
        Returns:
            해당하는 카테고리 리스트
        """
        categories = []
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content:
                    if category not in categories:
                        categories.append(category)
                    break
        
        # 기본값
        if not categories:
            categories.append("기타")
        
        return categories

    def _extract_related_articles(self, content: str) -> List[str]:
        """
        관련 조문 참조 추출
        
        패턴: "제33조에 따른", "제34조의", "제2조부터" 등
        """
        # 조문 참조 패턴
        pattern = r'제(\d+)조'
        matches = re.findall(pattern, content)
        
        related = []
        for match in matches:
            article_ref = f"제{match}조"
            if article_ref not in related:
                related.append(article_ref)
        
        return related

    def _extract_keywords(self, content: str) -> List[str]:
        """
        핵심 법률 용어 추출
        """
        # 법률 용어 사전
        legal_terms = [
            "인공지능", "고영향", "투명성", "안전성", "개인정보",
            "의무", "기본권", "영향평가", "위험", "평가",
            "의사결정", "알고리즘", "오작동", "오류",
            "기반", "요건", "기준", "조치", "이용자",
            "개발자", "서비스제공자", "사업자", "규제"
        ]
        
        keywords = []
        for term in legal_terms:
            if term in content and term not in keywords:
                keywords.append(term)
        
        return keywords[:10]  # 최대 10개까지만

    def clean_text(self, text: str) -> str:
        """
        텍스트 정제
        
        - 불필요한 공백 정규화
        - HTML 태그 제거
        - 법적 형식 유지 (①②③, 1. 2. 3., 가. 나. 다.)
        
        Args:
            text: 원본 텍스트
            
        Returns:
            정제된 텍스트
        """
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        
        # 연속 공백을 단일 공백으로
        text = re.sub(r'  +', ' ', text)
        
        # 연속 줄바꿈을 단일 줄바꿈으로
        text = re.sub(r'\n\n+', '\n', text)
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        return text

    def validate_article(self, article: Dict) -> bool:
        """
        조문 유효성 검증
        
        Args:
            article: 조문 딕셔너리
            
        Returns:
            유효하면 True
        """
        required_fields = ['law_name', 'article_no', 'article_content']
        
        for field in required_fields:
            if field not in article or not article[field]:
                logger.warning(f"필수 필드 누락: {field}")
                return False
        
        # 최소 길이 체크
        if len(article.get('article_content', '')) < 10:
            logger.warning(f"내용 길이 부족: {article.get('article_no')}")
            return False
        
        return True


def test_processor():
    """테스트"""
    processor = LegalTextProcessor()
    
    # 테스트 조문
    test_articles = [
        {
            "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
            "article_no": "제31조",
            "article_title": "투명성 확보",
            "article_content": "① 인공지능 개발자는 투명성을 확보하여야 한다. ② 서비스제공자는 이용자에게 알려야 한다.",
            "enforcement_date": "2023-12-20",
            "law_type": "법률",
            "law_id": "test"
        }
    ]
    
    chunks = processor.process_articles(test_articles)
    print(f"\n총 {len(chunks)}개 청크 생성됨")
    for chunk in chunks:
        print(f"\n청크 ID: {chunk['chunk_id']}")
        print(f"카테고리: {chunk['category']}")
        print(f"키워드: {chunk['keywords']}")
        print(f"관련 조문: {chunk['related_articles']}")


if __name__ == "__main__":
    test_processor()
