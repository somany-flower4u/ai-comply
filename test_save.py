"""
벡터 저장소 저장 테스트
"""
import os
import shutil
from data_collector import LawDataCollector
from vector_store import LegalVectorStore

print("=" * 60)
print("벡터 저장소 저장 테스트")
print("=" * 60)

# 1. 데이터 수집
print("\n[1단계] 데이터 수집 중...")
collector = LawDataCollector()
articles = collector.collect_all_target_laws()
print(f"✓ {len(articles)}개 조문 수집")

# 2. 벡터 저장소 생성 및 데이터 저장
print("\n[2단계] 벡터 저장소 구축 중...")
vs = LegalVectorStore()

# 기존 데이터 확인
stats_before = vs.get_stats()
print(f"구축 전 문서 개수: {stats_before.get('total_documents', 0)}개")

# 구축
vs.reset()
result = vs.build_from_scratch(articles)
print(f"구축 완료: {result}")

# 3. 저장된 데이터 확인
print("\n[3단계] 저장된 데이터 확인...")
stats = vs.get_stats()
print(f"✓ 저장된 문서 개수: {stats.get('total_documents', 0)}개")

# 4. 새 인스턴스에서 데이터 로드 확인
print("\n[4단계] 새 인스턴스에서 데이터 로드 시뮬레이션...")
vs2 = LegalVectorStore()
stats2 = vs2.get_stats()
print(f"✓ 새 인스턴스의 저장소 통계:")
print(f"  - 문서 개수: {stats2.get('total_documents', 0)}개")
print(f"  - 컬렉션명: {stats2.get('collection_name')}")
print(f"  - 디렉토리: {stats2.get('persist_directory')}")

# ChromaDB 디렉토리 확인
chroma_dir = "./chroma_db"
if os.path.exists(chroma_dir):
    print(f"\n✓ ChromaDB 디렉토리 존재")
    print(f"  경로: {os.path.abspath(chroma_dir)}")
    
    # 파일 목록 확인
    for root, dirs, files in os.walk(chroma_dir):
        level = root.replace(chroma_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # 처음 5개 파일만 표시
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}+ {len(files) - 5}개 파일 더...")
else:
    print(f"\n❌ ChromaDB 디렉토리 없음")

print("\n" + "=" * 60)
print("테스트 완료")
print("=" * 60)
