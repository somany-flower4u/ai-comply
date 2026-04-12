"""
수정된 데이터 수집 테스트
"""
from data_collector import LawDataCollector

collector = LawDataCollector()

print("=" * 60)
print("법령 데이터 수집 테스트 (수정된 버전)")
print("=" * 60)

# 모든 대상 법령 수집
articles = collector.collect_all_target_laws()

print(f"\n✓ 수집 완료!")
print(f"총 {len(articles)}개 조문 수집됨\n")

# 법령별 조문 수 집계
from collections import Counter
law_counts = Counter(article['law_name'] for article in articles)

print("법령별 조문 수:")
for law_name, count in sorted(law_counts.items()):
    print(f"  - {law_name}: {count}개")

# 처음 5개 샘플 출력
print(f"\n샘플 (처음 5개 조문):")
for i, article in enumerate(articles[:5], 1):
    print(f"\n{i}. {article['law_name']}")
    print(f"   조문: {article['article_no']} {article['article_title']}")
    print(f"   내용: {article['article_content'][:100]}...")
