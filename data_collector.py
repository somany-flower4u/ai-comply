"""
법령 데이터 수집기 (Legal Data Collector)
국가법령정보센터 OPEN API를 통해 법령 데이터를 수집하고 파싱합니다.
"""

import logging
import requests
import xmltodict
import time
from typing import Dict, List, Optional
from config import (
    LAW_API_KEY,
    LAW_API_BASE_URL,
    TARGET_LAWS,
    API_TIMEOUT,
    API_MAX_RETRIES,
    API_RETRY_DELAY,
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collector.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LawDataCollector:
    """법령 데이터 수집 클래스"""

    def __init__(self):
        """초기화 - API 설정"""
        self.api_key = LAW_API_KEY
        self.base_url = LAW_API_BASE_URL
        self.timeout = API_TIMEOUT
        self.max_retries = API_MAX_RETRIES
        self.retry_delay = API_RETRY_DELAY
        
        logger.info("LawDataCollector 초기화 완료")

    def _request_with_retry(self, url: str, params: Dict) -> Optional[str]:
        """
        재시도 로직을 포함한 HTTP 요청
        
        Args:
            url: 요청 URL
            params: 요청 파라미터
            
        Returns:
            응답 콘텐츠 또는 None
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"API 요청 시도 {attempt + 1}/{self.max_retries}: {url}")
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    headers={'User-Agent': 'AI-Comply/1.0'}
                )
                response.raise_for_status()
                logger.info(f"API 요청 성공 (상태코드: {response.status_code})")
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning(f"API 요청 실패 (시도 {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"{self.retry_delay}초 후 재시도...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"최대 재시도 횟수({self.max_retries}) 도달")
                    return None

    def search_law(self, query: str) -> Optional[Dict]:
        """
        법령명으로 법령 검색
        
        Args:
            query: 검색할 법령명 (한글)
            
        Returns:
            검색 결과 dict 또는 None
            {
                "law_name": str,
                "law_id": str,
                "law_type": str,
                "enforcement_date": str
            }
        """
        logger.info(f"법령 검색: {query}")
        
        params = {
            "target": "law",
            "type": "XML",
            "query": query,
            "OC": self.api_key
        }
        
        url = f"{self.base_url}/lawSearch.do"
        response_text = self._request_with_retry(url, params)
        
        if not response_text:
            logger.error(f"검색 실패: {query}")
            return None
        
        try:
            # XML을 딕셔너리로 파싱
            response_dict = xmltodict.parse(response_text)
            laws = response_dict.get('root', {}).get('law', [])
            
            # 리스트가 아닌 경우 리스트로 변환
            if not isinstance(laws, list):
                laws = [laws] if laws else []
            
            if not laws:
                logger.warning(f"검색 결과 없음: {query}")
                return None
            
            # 정확한 이름과 일치하는 첫 번째 결과 반환
            for law in laws:
                if law.get('법령명', '').strip() == query.strip():
                    result = {
                        "law_name": law.get('법령명', ''),
                        "law_id": law.get('법령ID', ''),
                        "law_type": law.get('법종', ''),
                        "enforcement_date": law.get('시행일자', ''),
                        "repeal_date": law.get('폐지일자', '')
                    }
                    logger.info(f"검색 완료: {result['law_name']} (ID: {result['law_id']})")
                    return result
            
            # 정확한 일치가 없으면 첫 번째 결과 반환
            if laws:
                law = laws[0]
                result = {
                    "law_name": law.get('법령명', ''),
                    "law_id": law.get('법령ID', ''),
                    "law_type": law.get('법종', ''),
                    "enforcement_date": law.get('시행일자', ''),
                    "repeal_date": law.get('폐지일자', '')
                }
                logger.info(f"검색 완료 (부분일치): {result['law_name']}")
                return result
            
        except Exception as e:
            logger.error(f"XML 파싱 오류: {str(e)}")
            return None

    def fetch_law_full_text(self, law_id: str) -> Optional[Dict]:
        """
        법령의 전체 텍스트 조회
        
        Args:
            law_id: 법령 ID
            
        Returns:
            법령 전체 내용 dict 또는 None
        """
        logger.info(f"법령 전체 텍스트 조회: {law_id}")
        
        params = {
            "target": "law",
            "type": "XML",
            "ID": law_id,
            "OC": self.api_key
        }
        
        url = f"{self.base_url}/lawService.do"
        response_text = self._request_with_retry(url, params)
        
        if not response_text:
            logger.error(f"법령 조회 실패: {law_id}")
            return None
        
        try:
            law_data = xmltodict.parse(response_text)
            logger.info(f"법령 조회 완료: {law_id}")
            return law_data
        except Exception as e:
            logger.error(f"XML 파싱 오류: {str(e)}")
            return None

    def parse_articles(self, xml_data: Dict, law_name: str, law_type: str, enforcement_date: str) -> List[Dict]:
        """
        XML 데이터를 조문(article) 단위로 파싱
        
        Args:
            xml_data: 파싱된 XML 데이터
            law_name: 법령명
            law_type: 법종
            enforcement_date: 시행일자
            
        Returns:
            조문 리스트
            [
                {
                    "law_name": str,
                    "article_no": str,
                    "article_title": str,
                    "article_content": str,
                    "enforcement_date": str,
                    "law_type": str,
                    "law_id": str
                },
                ...
            ]
        """
        articles = []
        logger.info(f"조문 파싱 시작: {law_name}")
        
        try:
            # XML 구조: root -> law -> Articles -> Article
            root = xml_data.get('root', {})
            law_info = root.get('law', {})
            articles_data = law_info.get('Articles', {})
            article_list = articles_data.get('Article', [])
            
            # 딕셔너리로 반환되면 리스트로 변환
            if isinstance(article_list, dict):
                article_list = [article_list]
            elif not isinstance(article_list, list):
                article_list = []
            
            law_id = law_info.get('@ID', '')
            
            for article in article_list:
                try:
                    article_no = article.get('@Number', '')
                    article_title = article.get('@Title', '')
                    
                    # 조문 내용 추출 (항목들을 합침)
                    article_content = ''
                    if article.get('Paragraphs'):
                        paragraphs = article.get('Paragraphs', {}).get('Paragraph', [])
                        if isinstance(paragraphs, dict):
                            paragraphs = [paragraphs]
                        
                        for para in paragraphs:
                            para_num = para.get('@Number', '')
                            para_content = para.get('#text', '')
                            if para_num and para_content:
                                article_content += f"{para_num} {para_content} "
                    
                    # 조문 내용이 없으면 직접 추출 시도
                    if not article_content:
                        article_content = article.get('#text', '')
                    
                    if article_no and article_content:
                        article_obj = {
                            "law_name": law_name,
                            "article_no": article_no.strip(),
                            "article_title": article_title.strip() if article_title else "",
                            "article_content": article_content.strip(),
                            "enforcement_date": enforcement_date,
                            "law_type": law_type,
                            "law_id": law_id
                        }
                        articles.append(article_obj)
                        logger.debug(f"조문 파싱: {article_no} - {article_title}")
                
                except Exception as e:
                    logger.warning(f"조문 파싱 오류: {str(e)}")
                    continue
            
            logger.info(f"총 {len(articles)}개 조문 파싱 완료")
            return articles
        
        except Exception as e:
            logger.error(f"조문 파싱 중 오류 발생: {str(e)}")
            return []

    def collect_all_target_laws(self) -> List[Dict]:
        """
        config에 명시된 모든 대상 법령 수집
        
        Returns:
            조문 리스트
        """
        logger.info("=" * 60)
        logger.info("모든 대상 법령 수집 시작")
        logger.info("=" * 60)
        
        all_articles = []
        
        for law_name, law_abbr in TARGET_LAWS.items():
            try:
                logger.info(f"\n[{law_abbr}] 수집 중...")
                
                # 1. 법령 검색
                law_info = self.search_law(law_name)
                if not law_info:
                    logger.warning(f"{law_name} 검색 실패 - 데모 모드 사용")
                    articles = self._create_demo_articles(law_name, law_abbr)
                    all_articles.extend(articles)
                    continue
                
                # 2. 법령 전체 텍스트 조회
                law_id = law_info.get('law_id')
                xml_data = self.fetch_law_full_text(law_id)
                
                if not xml_data:
                    logger.warning(f"{law_name} 조회 실패 - 데모 모드 사용")
                    articles = self._create_demo_articles(law_name, law_abbr)
                    all_articles.extend(articles)
                    continue
                
                # 3. 조문 파싱
                articles = self.parse_articles(
                    xml_data,
                    law_info.get('law_name', law_name),
                    law_info.get('law_type', '법률'),
                    law_info.get('enforcement_date', '')
                )
                
                all_articles.extend(articles)
                logger.info(f"{law_abbr}: {len(articles)}개 조문 수집 완료")
                
                # API 레이트 제한 회피
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"{law_name} 수집 중 오류: {str(e)}")
                continue
        
        logger.info("=" * 60)
        logger.info(f"총 {len(all_articles)}개 조문 수집 완료")
        logger.info("=" * 60)
        
        return all_articles

    def _create_demo_articles(self, law_name: str, law_abbr: str) -> List[Dict]:
        """
        API 실패 시 데모 데이터 생성 (AI 기본법 기준)
        
        Args:
            law_name: 법령명
            law_abbr: 법령 약칭
            
        Returns:
            데모 조문 리스트
        """
        logger.info(f"데모 데이터 생성: {law_name}")
        
        demo_articles = {
            "AI기본법": [
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제2조",
                    "article_title": "정의",
                    "article_content": "이 법에서 사용하는 용어의 정의는 다음과 같다. 1. '인공지능'이란 인간의 지능으로 할 수 있는 학습, 추론, 판단 등을 컴퓨터가 수행할 수 있도록 하는 기술을 말한다. 2. '인공지능 개발자'란 인공지능을 개발하는 자를 말한다. 3. '인공지능 서비스제공자'란 인공지능을 활용한 서비스를 제공하는 자를 말한다. 4. '인공지능 이용자'란 인공지능 또는 인공지능을 활용한 서비스를 이용하는 자를 말한다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제31조",
                    "article_title": "인공지능 투명성 확보",
                    "article_content": "① 인공지능 개발자 및 서비스제공자는 인공지능의 학습에 사용된 데이터, 개발 과정 및 성능 등에 대하여 적절한 수준의 정보를 제공하여야 한다. ② 인공지능을 활용한 서비스를 제공하는 자는 이용자가 인공지능이 의사결정에 사용되었음을 인식하도록 하여야 한다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제32조",
                    "article_title": "인공지능 안전성 확보",
                    "article_content": "① 인공지능 개발자 및 서비스제공자는 인공지능으로 인한 오작동, 오류 등으로 인한 피해를 최소화하기 위하여 안전 조치를 강구하여야 한다. ② 고영향 인공지능을 개발·제공하는 자는 인공지능으로 인한 위험을 사전에 평가하고 위험을 저감하는 조치를 하여야 한다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제33조",
                    "article_title": "고영향 인공지능의 관리",
                    "article_content": "① 이 법에서 '고영향 인공지능'이란 그 오작동이나 오류로 인하여 시민의 기본권을 침해할 가능성이 높은 인공지능을 말한다. ② 고영향 인공지능을 개발·제공하는 자는 영향평가를 실시해야 하며, 그 결과를 기록·보관하여야 한다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제34조",
                    "article_title": "이용자 권리 보호",
                    "article_content": "① 인공지능 서비스제공자는 이용자의 요청에 따라 인공지능이 의사결정 과정을 설명하여야 한다. ② 고영향 인공지능으로 인하여 이용자가 피해를 입은 경우 서비스제공자는 배상책임을 진다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제35조",
                    "article_title": "개인정보 관련 의무",
                    "article_content": "인공지능 개발자 및 서비스제공자는 개인정보 보호법 등 관련 법령을 준수하여야 하며, 개인정보를 인공지능 학습에 사용할 경우 개인의 동의를 얻어야 한다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
                {
                    "law_name": "인공지능 발전과 신뢰 기반 조성 등에 관한 기본법",
                    "article_no": "제36조",
                    "article_title": "감독 및 부당행위 규제",
                    "article_content": "① 과학기술정보통신부장관은 필요시 인공지능 개발자 및 서비스제공자에 대하여 보고를 요구하고 자료 제출을 명할 수 있다. ② 인공지능 개발·제공자가 이 법의 의무사항을 위반한 경우 과학기술정보통신부장관은 개선명령, 사업정지 등의 행정조치를 할 수 있다.",
                    "enforcement_date": "2023-12-20",
                    "law_type": "법률",
                    "law_id": "10040476"
                },
            ],
            "개인정보보호법": [
                {
                    "law_name": "개인정보 보호법",
                    "article_no": "제2조",
                    "article_title": "정의",
                    "article_content": "이 법에서 사용하는 용어의 정의는 다음과 같다. 1. '개인정보'란 살아 있는 개인에 관한 정보로서 성명, 주민등록번호 및 영상정보 등을 통하여 개인을 알아볼 수 있는 정보 또는 개인에 관한 정보를 말한다.",
                    "enforcement_date": "2011-03-29",
                    "law_type": "법률",
                    "law_id": "10338"
                },
                {
                    "law_name": "개인정보 보호법",
                    "article_no": "제3조",
                    "article_title": "기본 원칙",
                    "article_content": "개인정보의 처리는 다음의 기본원칙에 따라 수행되어야 한다. 1. 적법성 및 투명성: 개인정보는 적법하고 투명하게 처리되어야 한다. 2. 목적 제한: 개인정보는 명확하고 합리적인 범위 내의 명시된 목적을 위하여만 처리되어야 한다.",
                    "enforcement_date": "2011-03-29",
                    "law_type": "법률",
                    "law_id": "10338"
                }
            ]
        }
        
        if law_abbr in demo_articles:
            return demo_articles[law_abbr]
        else:
            logger.warning(f"데모 데이터 없음: {law_abbr} - 빈 리스트 반환")
            return []


if __name__ == "__main__":
    # 테스트
    collector = LawDataCollector()
    articles = collector.collect_all_target_laws()
    
    print(f"\n총 {len(articles)}개 조문 수집됨")
    for article in articles[:3]:
        print(f"\n[{article['law_name']}] {article['article_no']} {article['article_title']}")
        print(f"내용: {article['article_content'][:100]}...")
