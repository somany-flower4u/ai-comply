"""
AI 컴플리 메인 애플리케이션 (Streamlit UI)
AI 기본법 규제 자동 진단 서비스의 웹 인터페이스
"""

import streamlit as st
import logging
from typing import Dict, List
import json

# 페이지 설정
st.set_page_config(
    page_title="AI 컴플리 - AI 기본법 규제 자동 진단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 로깅
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 모듈 import
from config import STREAMLIT_PAGE_TITLE, STREAMLIT_PAGE_ICON, STREAMLIT_LAYOUT
from vector_store import LegalVectorStore
from agents import ClassifierAgent, HighImpactAgent, ObligationAgent
from utils import format_law_link, create_diagnosis_report


# ============================================================================
# 세션 상태 초기화
# ============================================================================
def init_session_state():
    """세션 상태 초기화"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = {}
    
    if 'diagnosis_results' not in st.session_state:
        st.session_state.diagnosis_results = None
    
    if 'checklist' not in st.session_state:
        st.session_state.checklist = {}


# ============================================================================
# 사이드바
# ============================================================================
def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.title("AI 컴플리")
        st.markdown("""
        ### 🚀 AI 기본법 규제 자동 진단 서비스
        
        당신의 AI 서비스가 준수해야 할 의무사항을 
        자동으로 진단해드립니다.
        """)
        
        st.divider()
        
        # 데이터베이스 관리
        st.subheader("📚 데이터베이스 관리")
        
        if st.button("🔄 데이터베이스 구축", use_container_width=True):
            st.info("데이터베이스 구축을 시작합니다. 잠시만 기다려주세요...")
            
            try:
                from data_collector import LawDataCollector
                
                with st.spinner("법령 데이터 수집 중..."):
                    collector = LawDataCollector()
                    articles = collector.collect_all_target_laws()
                
                with st.spinner("벡터 저장소 구축 중..."):
                    vs = LegalVectorStore()
                    vs.reset()
                    vs.build_from_scratch(articles)
                
                st.session_state.vector_store = vs
                st.success(f"✓ 데이터베이스 구축 완료!\n총 {len(articles)}개 조문이 수집되었습니다.")
                
            except Exception as e:
                st.error(f"데이터베이스 구축 실패: {str(e)}")
        
        # DB 상태
        if st.session_state.vector_store:
            try:
                stats = st.session_state.vector_store.get_stats()
                st.metric(
                    "📊 저장된 조문 수",
                    stats.get('total_documents', 0)
                )
            except:
                st.metric("📊 저장된 조문 수", "감지 불가")
        
        st.divider()
        
        # 관련 링크
        st.subheader("📖 관련 자료")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("법령정보센터", use_container_width=True):
                st.markdown(
                    "[국가법령정보센터](https://www.law.go.kr/)",
                    unsafe_allow_html=True
                )
        
        with col2:
            if st.button("API 문서", use_container_width=True):
                st.markdown(
                    "[OPEN API](https://open.law.go.kr/)",
                    unsafe_allow_html=True
                )
        
        st.divider()
        
        # 정보
        st.caption("""
        ℹ️ AI 컴플리는 한국의 AI 기본법 준수 현황을 
        진단하는 자동화 서비스입니다.
        
        ⚠️ 본 서비스는 정보 제공용이며, 
        법적 조언은 아닙니다.
        """)


# ============================================================================
# 메인 콘텐츠
# ============================================================================
def main():
    """메인 애플리케이션"""
    
    # 세션 상태 초기화
    init_session_state()
    
    # 벡터 저장소 로드
    if st.session_state.vector_store is None:
        try:
            st.session_state.vector_store = LegalVectorStore()
        except Exception as e:
            st.error(f"벡터 저장소 로드 실패: {str(e)}")
            st.info("먼저 사이드바의 '데이터베이스 구축' 버튼을 클릭해주세요.")
            return
    
    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 서비스 정보 입력",
        "📊 진단 결과",
        "✅ 체크리스트",
        "🔍 법령 검색"
    ])
    
    # ========================================================================
    # Tab 1: 서비스 정보 입력
    # ========================================================================
    with tab1:
        st.header("📋 AI 서비스 정보 입력")
        st.markdown("""
        당신의 AI 서비스에 대해 자세히 알려주세요.
        이 정보를 바탕으로 맞춤 진단을 수행합니다.
        """)
        
        with st.form("service_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # 서비스명
                service_name = st.text_input(
                    "서비스/제품명",
                    placeholder="예: AI 채용 심사 시스템",
                    value=st.session_state.user_input.get('service_name', '')
                )
            
            with col2:
                # 개발 단계
                development_stage = st.selectbox(
                    "현재 개발 단계",
                    ["기획 단계", "개발 중", "베타 테스트", "서비스 운영 중"],
                    index=0 if not st.session_state.user_input else 
                           ["기획 단계", "개발 중", "베타 테스트", "서비스 운영 중"].index(
                               st.session_state.user_input.get('development_stage', '기획 단계')
                           )
                )
            
            # 서비스 설명
            service_description = st.text_area(
                "서비스 설명",
                placeholder="AI 서비스의 주요 기능과 목적을 설명해주세요",
                height=100,
                value=st.session_state.user_input.get('service_description', '')
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # AI 유형
                ai_type = st.selectbox(
                    "AI 유형",
                    ["생성형 AI", "예측/분류 AI", "추천 시스템", 
                     "자연어처리", "컴퓨터비전", "기타"],
                    index=1 if not st.session_state.user_input else
                          ["생성형 AI", "예측/분류 AI", "추천 시스템", 
                           "자연어처리", "컴퓨터비전", "기타"].index(
                              st.session_state.user_input.get('ai_type', '예측/분류 AI')
                          )
                )
            
            with col2:
                # 산업 분야
                industry_sector = st.selectbox(
                    "산업 분야",
                    ["의료/헬스케어", "금융/보험", "교육", "법률", 
                     "채용/인사", "자율주행/교통", "콘텐츠/미디어", 
                     "전자상거래", "제조", "공공행정", "기타"],
                    index=4 if not st.session_state.user_input else
                          ["의료/헬스케어", "금융/보험", "교육", "법률", 
                           "채용/인사", "자율주행/교통", "콘텐츠/미디어", 
                           "전자상거래", "제조", "공공행정", "기타"].index(
                              st.session_state.user_input.get('industry_sector', '채용/인사')
                          )
                )
            
            with col3:
                # 개발 방식
                development_method = st.multiselect(
                    "개발 방식",
                    ["자체 개발", "외부 API 활용", "오픈소스 모델 활용", "위탁 개발"],
                    default=st.session_state.user_input.get('development_method', [])
                )
            
            # 서비스 대상
            target_users = st.multiselect(
                "서비스 대상",
                ["일반 소비자", "기업 고객(B2B)", "공공기관", "내부 업무용"],
                default=st.session_state.user_input.get('target_users', [])
            )
            
            # 데이터 활용
            data_usage = st.multiselect(
                "데이터 활용",
                ["개인정보 포함 데이터", "공공데이터", "자체 수집 데이터", "제3자 제공 데이터"],
                default=st.session_state.user_input.get('data_usage', [])
            )
            
            # 제출 버튼
            submitted = st.form_submit_button(
                "🚀 진단 시작",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if not service_name or not service_description or not development_method:
                    st.error("필수 항목을 모두 입력해주세요.")
                else:
                    # 사용자 정보 저장
                    st.session_state.user_input = {
                        'service_name': service_name,
                        'service_description': service_description,
                        'ai_type': ai_type,
                        'development_method': development_method,
                        'target_users': target_users,
                        'industry_sector': industry_sector,
                        'data_usage': data_usage,
                        'development_stage': development_stage,
                    }
                    
                    # 진단 수행
                    perform_diagnosis()
    
    # ========================================================================
    # Tab 2: 진단 결과
    # ========================================================================
    with tab2:
        st.header("📊 진단 결과")
        
        if st.session_state.diagnosis_results is None:
            st.info("👈 왼쪽 탭에서 정보를 입력하고 진단을 시작해주세요.")
        else:
            results = st.session_state.diagnosis_results
            
            # 1. 사업자 유형 분류
            st.subheader("📋 사업자 유형 분류 결과")
            
            classifier_result = results.get('classifier', {})
            operator_types = classifier_result.get('operator_types', [])
            
            if operator_types:
                cols = st.columns(len(operator_types))
                for col, op_type in zip(cols, operator_types):
                    with col:
                        st.info(f"✓ {op_type}")
            
            with st.expander("상세 분류 이유"):
                st.markdown(classifier_result.get('reasoning', '분석 실패'))
                
                if classifier_result.get('relevant_articles'):
                    st.markdown("**관련 조문:**")
                    for article in classifier_result['relevant_articles']:
                        st.caption(
                            f"[{article.get('법령명')}] "
                            f"{article.get('조문')} "
                            f"{article.get('조문제목')}"
                        )
            
            st.divider()
            
            # 2. 고영향 AI 진단
            st.subheader("⚠️ 고영향 AI 진단 결과")
            
            high_impact_result = results.get('high_impact', {})
            is_high_impact = high_impact_result.get('is_high_impact', False)
            risk_level = high_impact_result.get('risk_level', '저위험')
            
            # 위험도 시각화
            risk_colors = {
                "고위험": "🔴 고위험",
                "중위험": "🟡 중위험",
                "저위험": "🟢 저위험"
            }
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"### {risk_colors.get(risk_level, risk_level)}")
            
            if is_high_impact:
                st.error("⚠️ 이 서비스는 고영향 AI로 분류됩니다. 강화된 규제가 적용됩니다.")
            else:
                st.success("✓ 이 서비스는 고영향 AI로 분류되지 않습니다.")
            
            # 위험요소 분석
            risk_factors = high_impact_result.get('risk_factors', [])
            if risk_factors:
                st.markdown("**위험요소 분석:**")
                for factor in risk_factors:
                    score = factor.get('score', 0)
                    bar_length = min(score * 2, 10)
                    bar = "█" * bar_length + "░" * (10 - bar_length)
                    st.markdown(f"- {factor.get('factor', '')} `{bar}` ({score}/5)")
                    st.caption(factor.get('explanation', ''))
            
            with st.expander("상세 진단 내용"):
                st.markdown(high_impact_result.get('reasoning', '분석 실패'))
            
            st.divider()
            
            # 3. 의무사항 체크리스트
            st.subheader("✅ 의무사항 체크리스트")
            
            obligation_result = results.get('obligation', {})
            obligations = obligation_result.get('obligations', [])
            
            st.markdown(f"**총 {len(obligations)}개 의무사항**")
            
            for i, obligation in enumerate(obligations[:10]):  # 최대 10개 표시
                category = obligation.get('category', '')
                name = obligation.get('name', '')
                priority = obligation.get('priority', '권간')
                
                priority_icon = "🔴" if priority == "필수" else "🟡"
                
                checkbox_key = f"obligation_{i}"
                is_checked = st.checkbox(
                    f"{priority_icon} {category} - {name}",
                    value=st.session_state.checklist.get(checkbox_key, False),
                    key=checkbox_key
                )
                st.session_state.checklist[checkbox_key] = is_checked
            
            if len(obligations) > 10:
                st.info(f"+ {len(obligations) - 10}개 의무사항 더보기")
            
            # 다운로드 버튼
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 진단 보고서 다운로드"):
                    report = create_diagnosis_report(
                        classifier_result,
                        high_impact_result,
                        obligation_result
                    )
                    st.download_button(
                        label="클릭하여 다운로드",
                        data=report,
                        file_name="AI_COMPLY_진단보고서.md",
                        mime="text/markdown"
                    )
            
            with col2:
                if st.button("📊 체크리스트 내보내기"):
                    checklist_data = json.dumps(
                        [ob for ob in obligations],
                        ensure_ascii=False,
                        indent=2
                    )
                    st.download_button(
                        label="클릭하여 다운로드",
                        data=checklist_data,
                        file_name="의무사항_체크리스트.json",
                        mime="application/json"
                    )
    
    # ========================================================================
    # Tab 3: 체크리스트 상세보기
    # ========================================================================
    with tab3:
        st.header("✅ 의무사항 상세 체크리스트")
        
        if st.session_state.diagnosis_results is None:
            st.info("진단 결과를 먼저 조회해주세요.")
        else:
            obligation_result = st.session_state.diagnosis_results.get('obligation', {})
            obligations = obligation_result.get('obligations', [])
            
            # 카테고리별 필터
            if obligations:
                categories = list(set(ob.get('category', '') for ob in obligations))
                selected_category = st.selectbox(
                    "의무 카테고리 필터",
                    ["전체"] + categories
                )
                
                # 필터링
                filtered_obligations = obligations
                if selected_category != "전체":
                    filtered_obligations = [
                        ob for ob in obligations
                        if ob.get('category', '') == selected_category
                    ]
                
                # 표시
                for i, obligation in enumerate(filtered_obligations):
                    with st.expander(f"💼 {obligation.get('name', '')}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**카테고리:** {obligation.get('category', '')}")
                            st.markdown(f"**설명:** {obligation.get('description', '')}")
                            
                            if obligation.get('legal_basis'):
                                st.markdown(
                                    f"**법적 근거:** {', '.join(obligation['legal_basis'])}"
                                )
                            
                            if obligation.get('deadline'):
                                st.markdown(f"**이행 주기:** {obligation['deadline']}")
                            
                            st.markdown("**체크리스트:**")
                            for item in obligation.get('checklist', []):
                                st.checkbox(item, value=False)
                        
                        with col2:
                            priority = obligation.get('priority', '권장')
                            if priority == "필수":
                                st.error("필 수")
                            else:
                                st.warning("권 장")
            else:
                st.info("의무사항이 없습니다.")
    
    # ========================================================================
    # Tab 4: 법령 검색
    # ========================================================================
    with tab4:
        st.header("🔍 법령 검색")
        st.markdown("보유한 법령 데이터베이스에서 자유롭게 검색하세요.")
        
        search_query = st.text_input(
            "검색어 입력",
            placeholder="예: 투명성, 안전성, 개인정보, 등"
        )
        
        search_type = st.selectbox(
            "검색 범위",
            ["전체", "정의", "의무", "벌칙", "고영향AI", "투명성", "안전성"],
        )
        
        if st.button("🔎 검색", use_container_width=True):
            if search_query:
                with st.spinner("검색 중..."):
                    try:
                        # 벡터 검색 수행
                        if search_type == "전체":
                            results = st.session_state.vector_store.search(
                                search_query, n_results=5
                            )
                        else:
                            results = st.session_state.vector_store.search_by_category(
                                search_query, search_type, n_results=5
                            )
                        
                        st.success(f"검색 결과: {len(results)}개")
                        
                        for i, result in enumerate(results, 1):
                            metadata = result.get('metadata', {})
                            
                            with st.expander(
                                f"[{i}] {metadata.get('law_name', '')} "
                                f"- {metadata.get('article_no', '')}"
                            ):
                                st.markdown(
                                    f"**조문:** {metadata.get('article_title', '')}"
                                )
                                st.markdown(
                                    f"**내용:** {result.get('content', '')}"
                                )
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button(
                                        "📖 법령정보센터에서 보기",
                                        key=f"law_link_{i}"
                                    ):
                                        law_link = format_law_link(
                                            metadata.get('law_name', '')
                                        )
                                        st.markdown(f"[링크]({law_link})")
                                
                                with col2:
                                    st.caption(
                                        f"시행일: {metadata.get('enforcement_date', '')} | "
                                        f"법종: {metadata.get('law_type', '')}"
                                    )
                    
                    except Exception as e:
                        st.error(f"검색 실패: {str(e)}")
            else:
                st.warning("검색어를 입력해주세요.")


def perform_diagnosis():
    """진단 수행"""
    st.session_state.diagnosis_results = None
    
    user_input = st.session_state.user_input
    vector_store = st.session_state.vector_store
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1단계: 사업자 유형 분류
        status_text.text("1단계: 사업자 유형 분류 중...")
        progress_bar.progress(25)
        
        classifier = ClassifierAgent(vector_store)
        classifier_result = classifier.classify(user_input)
        
        # 2단계: 고영향 AI 진단
        status_text.text("2단계: 고영향 AI 진단 중...")
        progress_bar.progress(50)
        
        high_impact_agent = HighImpactAgent(vector_store)
        high_impact_result = high_impact_agent.diagnose(
            user_input,
            classifier_result.get('operator_types', [])
        )
        
        # 3단계: 의무사항 매핑
        status_text.text("3단계: 의무사항 분석 중...")
        progress_bar.progress(75)
        
        obligation_agent = ObligationAgent(vector_store)
        obligation_result = obligation_agent.map_obligations(
            user_input,
            classifier_result.get('operator_types', []),
            high_impact_result
        )
        
        # 진단 완료
        progress_bar.progress(100)
        status_text.text("✓ 진단 완료!")
        
        # 결과 저장
        st.session_state.diagnosis_results = {
            'classifier': classifier_result,
            'high_impact': high_impact_result,
            'obligation': obligation_result
        }
        
        # 결과 탭으로 전환
        st.switch_to_query_params(tab="진단 결과")
        st.success("진단이 완료되었습니다! 아래에서 결과를 확인하세요.")
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"진단 중 오류 발생: {str(e)}")
        logger.error(f"진단 실패: {str(e)}", exc_info=True)


if __name__ == "__main__":
    render_sidebar()
    main()
