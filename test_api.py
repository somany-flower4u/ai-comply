"""
API 테스트 스크립트
"""
import requests
import xmltodict

LAW_API_KEY = 'theflower4u_12'
BASE_URL = 'http://www.law.go.kr/DRF'

def test_api():
    try:
        # 1. 법령 검색 (여러 쿼리로 시도)
        queries = [
            'AI기본법',
            '인공지능 기본법',
            '개인정보 보호법'
        ]
        
        for query in queries:
            print(f'[{query}] 검색 중...')
            params = {
                'target': 'law',
                'type': 'XML',
                'query': query,
                'OC': LAW_API_KEY
            }
            
            response = requests.get(f'{BASE_URL}/lawSearch.do', params=params, timeout=10)
            response.raise_for_status()
            
            print(f'응답 상태: {response.status_code}')
            print(f'응답 내용 (처음 1000자):')
            print(response.text[:1000])
            print('---')
            
    except requests.exceptions.ConnectionError as e:
        print(f'❌ 네트워크 오류: {str(e)}')
    except Exception as e:
        print(f'❌ 오류: {str(e)}')

if __name__ == '__main__':
    test_api()
