"""
실제 조문 데이터 수집 테스트
"""
import requests
import xmltodict

LAW_API_KEY = 'theflower4u_12'
BASE_URL = 'http://www.law.go.kr/DRF'

def get_law_articles():
    try:
        # 1. 인공지능기본법 검색
        print('[1] 인공지능기본법 검색...')
        params = {
            'target': 'law',
            'type': 'XML',
            'query': '인공지능 기본법',
            'OC': LAW_API_KEY
        }
        
        response = requests.get(f'{BASE_URL}/lawSearch.do', params=params, timeout=10)
        search_data = xmltodict.parse(response.text)
        
        laws = search_data.get('LawSearch', {}).get('law', [])
        if not isinstance(laws, list):
            laws = [laws]
        
        if not laws:
            print('❌ 검색 결과 없음')
            return
        
        law = laws[0]
        law_id = law.get('법령ID')
        law_name_cdata = law.get('법령명한글')
        
        # CDATA 처리
        if isinstance(law_name_cdata, dict):
            law_name = law_name_cdata.get('#text', '')
        else:
            law_name = law_name_cdata
        
        print(f'✓ 검색 완료')
        print(f'  - 법령명: {law_name}')
        print(f'  - 법령ID: {law_id}')
        
        # 2. 조문 데이터 조회 (MST 파라미터 사용)
        print(f'\n[2] 조문 데이터 조회 중...')
        params2 = {
            'target': 'law',
            'type': 'XML',
            'MST': law.get('법령일련번호'),  # or try 'ID': law_id
            'OC': LAW_API_KEY
        }
        
        response2 = requests.get(f'{BASE_URL}/lawService.do', params=params2, timeout=10)
        print(f'응답 상태: {response2.status_code}')
        
        # 응답 확인
        if response2.status_code == 200:
            # XML 첫 2000자 확인
            print(f'\n응답 내용 (처음 2000자):')
            print(response2.text[:2000])
            
            # 파싱 시도
            try:
                law_data = xmltodict.parse(response2.text)
                print(f'\n✓ XML 파싱 성공')
                print(f'최상위 키: {list(law_data.keys())}')
                
                # 구조 확인
                if 'root' in law_data:
                    root = law_data['root']
                    print(f'\nroot의 키: {list(root.keys())}')
                    
                    if 'law' in root:
                        law_info = root['law']
                        print(f'\nlaw의 키: {list(law_info.keys())[:10]}...')
                        
                        if 'Articles' in law_info:
                            articles = law_info['Articles'].get('Article', [])
                            if not isinstance(articles, list):
                                articles = [articles]
                            print(f'\n조문 개수: {len(articles)}개')
                            
                            # 첫 5개 조문 표시
                            for i, article in enumerate(articles[:5]):
                                article_no = article.get('@Number', '')
                                article_title = article.get('@Title', '')
                                print(f'  {i+1}. {article_no} - {article_title}')
            except Exception as e:
                print(f'❌ XML 파싱 오류: {str(e)}')
        else:
            print(f'❌ 요청 실패: {response2.status_code}')
        
    except Exception as e:
        print(f'❌ 오류: {str(e)}')

if __name__ == '__main__':
    get_law_articles()
