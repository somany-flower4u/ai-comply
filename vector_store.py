"""
벡터 저장소 모듈 (Legal Vector Store)
ChromaDB와 sentence-transformers를 사용하여 법령 데이터를 벡터화하고 검색합니다.
"""

import logging
import os
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from config import (
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vector_store.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LegalVectorStore:
    """법령 벡터 저장소 클래스"""

    def __init__(self):
        """초기화 - ChromaDB 클라이언트 및 임베딩 모델"""
        logger.info("LegalVectorStore 초기화 중...")
        
        # ChromaDB 디렉토리 생성
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        
        # ChromaDB 클라이언트 초기화 (지속성)
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        logger.info(f"ChromaDB 클라이언트 초기화 완료 (경로: {CHROMA_PERSIST_DIR})")
        
        # 임베딩 모델 로드 (캐시됨)
        logger.info(f"임베딩 모델 로드 중: {EMBEDDING_MODEL}")
        try:
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            logger.info(f"임베딩 모델 로드 완료")
        except Exception as e:
            logger.error(f"임베딩 모델 로드 실패: {str(e)}")
            raise
        
        # 컬렉션 생성 또는 로드
        self.collection = self.create_collection()
        
        logger.info("LegalVectorStore 초기화 완료")

    def create_collection(self) -> chromadb.Collection:
        """
        ChromaDB 컬렉션 생성 또는 기존 컬렉션 로드
        
        Returns:
            ChromaDB 컬렉션
        """
        logger.info(f"컬렉션 '{CHROMA_COLLECTION_NAME}' 접근 중...")
        
        try:
            # 기존 컬렉션 로드 또는 생성
            collection = self.client.get_or_create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            count = collection.count()
            logger.info(f"컬렉션 준비 완료 (현재 {count}개 문서)")
            
            return collection
        except Exception as e:
            logger.error(f"컬렉션 생성 실패: {str(e)}")
            raise

    def add_documents(self, chunks: List[Dict]) -> int:
        """
        처리된 청크를 벡터 저장소에 추가
        
        Args:
            chunks: 청크 리스트
            
        Returns:
            추가된 문서 개수
        """
        logger.info(f"문서 추가 시작: {len(chunks)}개 청크")
        
        if not chunks:
            logger.warning("추가할 청크가 없음")
            return 0
        
        try:
            # 임베딩 생성
            documents = []
            ids = []
            metadatas = []
            embeddings = []
            
            for chunk in chunks:
                # 고유 ID
                chunk_id = chunk.get('chunk_id', '')
                if not chunk_id:
                    logger.warning("청크 ID 누락, 건너뜀")
                    continue
                
                # 문서 텍스트
                document = chunk.get('article_content', '')
                if not document:
                    logger.warning(f"문서 텍스트 누락 ({chunk_id}), 건너뜀")
                    continue
                
                # 메타데이터
                metadata = {
                    'law_name': chunk.get('law_name', ''),
                    'article_no': chunk.get('article_no', ''),
                    'article_title': chunk.get('article_title', ''),
                    'paragraph_no': chunk.get('paragraph_no', ''),
                    'enforcement_date': chunk.get('enforcement_date', ''),
                    'law_type': chunk.get('law_type', ''),
                    'law_id': chunk.get('law_id', ''),
                    'category': ','.join(chunk.get('category', [])),
                    'keywords': ','.join(chunk.get('keywords', [])),
                    'related_articles': ','.join(chunk.get('related_articles', [])),
                    'content_length': str(chunk.get('content_length', 0)),
                }
                
                documents.append(document)
                ids.append(chunk_id)
                metadatas.append(metadata)
                
                # 임베딩 생성
                embedding = self.embedding_model.encode(document, convert_to_tensor=False)
                embeddings.append(embedding)
            
            # 벡터 저장소에 추가
            if documents:
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                
                logger.info(f"✓ {len(documents)}개 문서 추가 완료")
                return len(documents)
            else:
                logger.warning("추가할 유효한 문서 없음")
                return 0
        
        except Exception as e:
            logger.error(f"문서 추가 중 오류: {str(e)}")
            raise

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        유사도 검색
        
        Args:
            query: 검색 쿼리
            n_results: 반환할 결과 개수
            filter_dict: 메타데이터 필터 (ChromaDB where 형식)
            
        Returns:
            검색 결과 리스트
            [
                {
                    "content": str,
                    "metadata": dict,
                    "distance": float
                },
                ...
            ]
        """
        logger.info(f"검색 수행: '{query}' (결과: {n_results}개)")
        
        try:
            # 쿼리 임베딩 생성
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            
            # ChromaDB 검색 수행
            query_kwargs = {
                "query_embeddings": [query_embedding],
                "n_results": n_results,
                "include": ["embeddings", "documents", "metadatas", "distances"]
            }
            
            # 필터가 있는 경우에만 where 파라미터 추가 (검증)
            if filter_dict:
                # ChromaDB where 필터 검증: $contains는 지원하지 않음
                self._validate_where_filter(filter_dict)
                query_kwargs["where"] = filter_dict
            
            results = self.collection.query(**query_kwargs)
            
            # 결과 포매팅
            formatted_results = []
            
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    result = {
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0.0
                    }
                    formatted_results.append(result)
            
            logger.info(f"✓ {len(formatted_results)}개 결과 반환")
            return formatted_results
        
        except Exception as e:
            logger.error(f"검색 중 오류: {str(e)}")
            # 필터 오류 시 필터 없이 재시도
            if filter_dict and "where" in str(e).lower():
                logger.warning("필터 오류 감지, 필터 없이 재시도합니다...")
                try:
                    query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
                    query_kwargs = {
                        "query_embeddings": [query_embedding],
                        "n_results": n_results,
                        "include": ["embeddings", "documents", "metadatas", "distances"]
                    }
                    results = self.collection.query(**query_kwargs)
                    
                    formatted_results = []
                    if results['documents'] and len(results['documents']) > 0:
                        for i, doc in enumerate(results['documents'][0]):
                            result = {
                                "content": doc,
                                "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                                "distance": results['distances'][0][i] if results['distances'] else 0.0
                            }
                            formatted_results.append(result)
                    
                    logger.info(f"✓ 필터 없이 {len(formatted_results)}개 결과 반환")
                    return formatted_results
                except Exception as e2:
                    logger.error(f"필터 없는 검색도 실패: {str(e2)}")
                    return []
            return []

    def _validate_where_filter(self, filter_dict: Dict) -> None:
        """
        ChromaDB where 필터 검증
        
        Args:
            filter_dict: 검증할 필터
            
        Raises:
            ValueError: 지원하지 않는 연산자 사용 시
        """
        def check_filter(filt):
            if isinstance(filt, dict):
                for key, value in filt.items():
                    # ChromaDB에서 지원하지 않는 연산자 확인
                    if isinstance(value, dict):
                        for op_key in value.keys():
                            if op_key.startswith('$') and op_key not in ['$eq', '$ne', '$gt', '$gte', '$lt', '$lte', '$and', '$or']:
                                raise ValueError(f"지원하지 않는 연산자: {op_key}. ChromaDB는 $contains를 지원하지 않습니다. 대신 Python 필터링을 사용하세요.")
                    elif key in ['$and', '$or'] and isinstance(value, list):
                        for item in value:
                            check_filter(item)
        
        check_filter(filter_dict)

    def search_by_category(
        self,
        query: str,
        category: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        카테고리로 필터링된 검색
        
        Args:
            query: 검색 쿼리
            category: 카테고리 필터
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 리스트 (카테고리 필터링됨)
        """
        logger.info(f"카테고리 검색: '{query}' (카테고리: {category})")
        
        try:
            # 카테고리 필터 없이 더 많은 결과를 먼저 검색
            # ChromaDB의 $contains 연산자 오류를 피하기 위해 필터 없이 검색
            search_results = self.search(query, n_results * 3, filter_dict=None)
            
            if not search_results:
                logger.info("검색 결과 없음, 빈 리스트 반환")
                return search_results
            
            # 카테고리 필터링 (메타데이터의 category 필드에 포함된 항목만)
            filtered_results = []
            for result in search_results:
                metadata = result.get('metadata', {})
                categories_str = metadata.get('category', '')
                
                if not categories_str:
                    continue
                
                # 쉼표로 구분된 카테고리들을 분석
                categories = [c.strip() for c in categories_str.split(',')]
                
                # 원하는 카테고리가 포함되어 있는지 확인 (정확한 매칭)
                if any(category.strip().lower() in cat.lower() for cat in categories):
                    filtered_results.append(result)
                    if len(filtered_results) >= n_results:
                        break
            
            # 충분한 결과가 없으면 더 검색
            if len(filtered_results) < n_results:
                logger.info(f"카테고리 필터링으로 {len(filtered_results)}개만 획득, 추가 검색 수행...")
                additional_results = self.search(query, n_results * 2, filter_dict=None)
                for result in additional_results[len(search_results):]:
                    metadata = result.get('metadata', {})
                    categories_str = metadata.get('category', '')
                    
                    if not categories_str:
                        continue
                    
                    categories = [c.strip() for c in categories_str.split(',')]
                    if any(category.strip().lower() in cat.lower() for cat in categories):
                        if result not in filtered_results:
                            filtered_results.append(result)
                        if len(filtered_results) >= n_results:
                            break
            
            logger.info(f"✓ {len(filtered_results)}개 카테고리 필터링 결과 반환")
            return filtered_results[:n_results]
        
        except Exception as e:
            logger.error(f"카테고리 검색 오류: {str(e)}")
            # 실패 시 필터 없이 일반 검색 반환
            logger.info("필터 없이 일반 검색으로 대체")
            return self.search(query, n_results, filter_dict=None)

    def search_by_law(
        self,
        query: str,
        law_name: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        특정 법령에서만 검색
        
        Args:
            query: 검색 쿼리
            law_name: 법령명
            n_results: 반환할 결과 개수
            
        Returns:
            검색 결과 리스트
        """
        logger.info(f"법령 검색: '{query}' (법령: {law_name})")
        
        where_filter = {
            "law_name": law_name
        }
        
        return self.search(query, n_results, where_filter)

    def get_stats(self) -> Dict:
        """
        벡터 저장소 통계 조회
        
        Returns:
            통계 정보
        """
        try:
            count = self.collection.count()
            
            stats = {
                "collection_name": CHROMA_COLLECTION_NAME,
                "total_documents": count,
                "embedding_model": EMBEDDING_MODEL,
                "persist_directory": CHROMA_PERSIST_DIR,
            }
            
            logger.info(f"저장소 통계: 총 {count}개 문서")
            return stats
        
        except Exception as e:
            logger.error(f"통계 조회 중 오류: {str(e)}")
            return {}

    def reset(self) -> bool:
        """
        컬렉션 초기화 (모든 데이터 삭제)
        
        Returns:
            성공 여부
        """
        try:
            logger.warning(f"컬렉션 '{CHROMA_COLLECTION_NAME}' 초기화 중...")
            
            # 컬렉션 삭제
            self.client.delete_collection(name=CHROMA_COLLECTION_NAME)
            
            # 새 컬렉션 생성
            self.collection = self.create_collection()
            
            logger.info("✓ 컬렉션 초기화 완료")
            return True
        
        except Exception as e:
            logger.error(f"컬렉션 초기화 실패: {str(e)}")
            return False

    def build_from_scratch(
        self,
        articles: List[Dict],
        batch_size: int = 50
    ) -> bool:
        """
        처음부터 벡터 저장소 구축
        
        Args:
            articles: 수집된 조문 리스트
            batch_size: 배치 크기
            
        Returns:
            성공 여부
        """
        from data_collector import LawDataCollector
        from text_processor import LegalTextProcessor
        
        logger.info("=" * 60)
        logger.info("벡터 저장소 처음부터 구축 시작")
        logger.info("=" * 60)
        
        try:
            # 1. 기존 컬렉션 초기화
            logger.info("\n[1단계] 기존 컬렉션 초기화...")
            self.reset()
            
            # 2. 텍스트 처리
            logger.info("\n[2단계] 텍스트 처리 중...")
            processor = LegalTextProcessor()
            chunks = processor.process_articles(articles)
            logger.info(f"✓ {len(chunks)}개 청크 생성")
            
            # 3. 배치 단위로 추가
            logger.info("\n[3단계] 벡터 저장소에 추가 중...")
            total_added = 0
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                added = self.add_documents(batch)
                total_added += added
                
                progress = min(i + batch_size, len(chunks))
                logger.info(f"진행률: {progress}/{len(chunks)} ({100*progress//len(chunks)}%)")
            
            # 4. 최종 통계
            logger.info("\n[4단계] 구축 완료")
            stats = self.get_stats()
            
            logger.info("=" * 60)
            logger.info("✓ 벡터 저장소 구축 완료")
            logger.info(f"  - 총 {total_added}개 문서 추가")
            logger.info(f"  - 저장소 문서: {stats.get('total_documents')}개")
            logger.info("=" * 60)
            
            return True
        
        except Exception as e:
            logger.error(f"벡터 저장소 구축 실패: {str(e)}")
            return False


if __name__ == "__main__":
    # 테스트
    store = LegalVectorStore()
    
    # 저장소 통계
    stats = store.get_stats()
    print(f"\n벡터 저장소 통계:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 테스트 검색
    if stats['total_documents'] > 0:
        print("\n테스트 검색 실행...")
        results = store.search("인공지능 투명성", n_results=3)
        print(f"검색 결과: {len(results)}개")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['metadata'].get('law_name')} - {result['metadata'].get('article_no')}")
            print(f"   내용: {result['content'][:80]}...")
