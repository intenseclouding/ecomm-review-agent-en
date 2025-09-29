import streamlit as st
from datetime import datetime
import sys
import json
import os
from typing import List, Dict, Any
sys.path.append('.')

# 키워드 저장 파일 경로
KEYWORDS_FILE = "agent/keyword_extractor/registered_keywords.json"

def load_keywords() -> Dict[str, List[str]]:
    """등록된 키워드 목록 로드"""
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_keywords(keywords: Dict[str, List[str]]):
    """키워드 목록 저장"""
    with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)

def register_keyword(keyword: str, synonyms: List[str] = None) -> Dict[str, Any]:
    """새로운 키워드를 동의어와 함께 등록"""
    if synonyms is None:
        synonyms = []

    # 기존 키워드 로드
    keywords = load_keywords()

    # 새 키워드 추가 (키워드 자체도 동의어 목록에 포함)
    all_synonyms = [keyword] + synonyms
    keywords[keyword] = list(set(all_synonyms))  # 중복 제거

    # 저장
    save_keywords(keywords)

    return {
        "status": "registered",
        "keyword": keyword,
        "synonyms": keywords[keyword],
        "total_keywords": len(keywords)
    }

# 키워드 검색 에이전트 import 시도
try:
    from agent.keyword_extractor.agent import search_keywords
    AGENT_AVAILABLE = True
    print("✅ Keyword Search Agent import 성공")
except ImportError as e:
    print(f"❌ Keyword Search Agent import 실패: {e}")
    AGENT_AVAILABLE = False
except Exception as e:
    print(f"❌ 예상치 못한 오류: {e}")
    AGENT_AVAILABLE = False

st.set_page_config(
    page_title="키워드 검색 시스템",
    page_icon="🏷️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main > div {
        padding-top: 1rem;
    }
    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0 !important;
    }
    .product-rating-container {
        background: linear-gradient(135deg, #eef2ff 0%, #f5f7ff 100%);
        border: 1px solid #dbe3ff;
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 14px 34px rgba(99, 102, 241, 0.12);
    }
    .product-rating-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 32px;
        align-items: start;
    }
    .keyword-badge {
        background-color: #e1f5fe;
        color: #01579b;
        padding: 4px 8px;
        margin: 2px;
        border-radius: 12px;
        font-size: 12px;
        display: inline-block;
    }

    /* Streamlit 버튼 커스텀 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        height: auto !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    .stButton > button:focus {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 세션 상태 초기화
if 'keyword_matching_results' not in st.session_state:
    st.session_state.keyword_matching_results = {}

if 'show_keyword_modal' not in st.session_state:
    st.session_state.show_keyword_modal = False

if 'comments' not in st.session_state:
    st.session_state.comments = [
        {
            "id": 1,
            "author": "김민수",
            "rating": 5,
            "content": "이 제품 정말 좋아요! 음질도 훌륭하고 배터리도 오래 갑니다.",
            "timestamp": "2024-01-15 14:30"
        },
        {
            "id": 2,
            "author": "이영희",
            "rating": 4,
            "content": "디자인이 예쁘고 착용감도 편안해요. 가성비 좋은 제품입니다.",
            "timestamp": "2024-01-14 16:45"
        },
        {
            "id": 3,
            "author": "박철수",
            "rating": 3,
            "content": "보통 수준이에요. 가격 대비 적당한 것 같습니다.",
            "timestamp": "2024-01-13 10:20"
        },
        {
            "id": 4,
            "author": "최지영",
            "rating": 5,
            "content": "소리가 깨끗하고 외관도 세련되네요. 만족합니다!",
            "timestamp": "2024-01-12 09:15"
        }
    ]

# 메인 콘텐츠 영역
st.title("🏷️ 키워드 검색 시스템")

# 제품 정보 섹션 (최상단 이동)
st.markdown(
    """
    <div class="product-rating-container">
        <div class="product-rating-grid">
            <div>
                <h3>🎧 무선 블루투스 헤드폰</h3>
                <p><strong>브랜드:</strong> TechSound Pro</p>
                <p><strong>모델:</strong> TS-WH1000</p>
                <p><strong>가격:</strong> ₩199,000</p>
                <p><strong>주요 특징:</strong> 노이즈 캔슬링, 30시간 배터리, 고해상도 오디오</p>
            </div>
            <div>
                <h3>⭐ 평점 정보</h3>
                <p><strong>평균 평점:</strong> 4.3/5.0</p>
                <p><strong>총 리뷰:</strong> {total_reviews}개</p>
            </div>
        </div>
    </div>
    """.format(total_reviews=len(st.session_state.comments)),
    unsafe_allow_html=True
)

# 키워드 관리 섹션
st.subheader("🏷️ 키워드 관리")

if AGENT_AVAILABLE:
    # 등록된 키워드 표시 및 새 키워드 등록 버튼
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write("**등록된 키워드**")
        registered_keywords = load_keywords()
        if registered_keywords:
            # 키워드 목록만 표시 (클릭 기능 제거)
            cols = st.columns(4)
            for idx, (keyword, synonyms) in enumerate(registered_keywords.items()):
                col_idx = idx % 4
                with cols[col_idx]:
                    st.markdown(f"**🏷️ {keyword}**")
                    st.caption(f"동의어: {', '.join(synonyms[1:]) if len(synonyms) > 1 else '없음'}")
        else:
            st.info("⚠️ 등록된 키워드가 없습니다. 새 키워드를 등록해주세요!")

    with col2:
        if st.button("➕ 새 키워드 등록", type="primary", use_container_width=True):
            st.session_state["show_keyword_modal"] = True
            st.rerun()

    # 키워드 등록 모달 (팝업)
    if st.session_state.get("show_keyword_modal", False):
        with st.container():
            st.markdown("---")
            st.subheader("➕ 새 키워드 등록")

            with st.form("keyword_form"):
                new_keyword = st.text_input("키워드", placeholder="예: 음질")
                synonyms_input = st.text_input("동의어 (쉼표로 구분)", placeholder="예: 소리, 사운드, 오디오")

                col1, col2 = st.columns([1, 1])
                with col1:
                    submit = st.form_submit_button("🏷️ 등록", type="primary", use_container_width=True)
                with col2:
                    cancel = st.form_submit_button("❌ 취소", use_container_width=True)

                if submit:
                    if new_keyword:
                        synonyms = [s.strip() for s in synonyms_input.split(",") if s.strip()] if synonyms_input else []
                        try:
                            with st.spinner("키워드 등록 중..."):
                                result = register_keyword(new_keyword, synonyms)
                                if result.get('success', True):
                                    st.success(f"✅ 키워드 '{new_keyword}' 등록 완료!")
                                    st.session_state["show_keyword_modal"] = False
                                    st.rerun()
                                else:
                                    st.error(f"❌ 키워드 등록 실패: {result.get('error', '알 수 없는 오류')}")
                        except Exception as e:
                            st.error(f"❌ 키워드 등록 실패: {str(e)}")
                    else:
                        st.error("키워드를 입력해주세요.")

                if cancel:
                    st.session_state["show_keyword_modal"] = False
                    st.rerun()

            st.markdown("---")
else:
    st.error("❌ 키워드 검색 에이전트를 사용할 수 없습니다.")

st.divider()

# 리뷰 섹션
st.subheader("📝 고객 리뷰")

# 키워드 검색 실행 버튼
if AGENT_AVAILABLE:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write("등록된 키워드를 기반으로 모든 리뷰를 분석하고 관련 키워드를 추출합니다.")
    with col2:
        if st.button("🔍 전체 키워드 검색", type="primary", use_container_width=True):
            with st.spinner("모든 리뷰 키워드 검색 중..."):
                try:
                    for comment in st.session_state.comments:
                        # 키워드 검색 분석 실행
                        match_result = search_keywords(comment['content'])

                        # 검색 결과를 comment별로 저장
                        st.session_state.keyword_matching_results[comment['id']] = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "review_text": comment['content'],
                            "match_result": match_result
                        }

                    st.success(f"{len(st.session_state.comments)}개 리뷰의 키워드 검색이 완료되었습니다!")
                    st.rerun()

                except Exception as e:
                    st.error(f"키워드 검색 중 오류가 발생했습니다: {str(e)}")
else:
    st.error("❌ 키워드 검색 에이전트를 사용할 수 없습니다.")

# 리뷰 표시 섹션
# 키워드 검색 결과가 있으면 필터 버튼 표시, 없으면 전체 리뷰 표시
if st.session_state.keyword_matching_results:
    # 모든 발견된 키워드 수집
    all_found_keywords = set()
    for result in st.session_state.keyword_matching_results.values():
        match_result = result.get('match_result', {})
        if match_result.get('success'):
            analysis_result = match_result.get('analysis_result', {})

            if 'matched_keywords' in analysis_result:
                matched_keywords = analysis_result.get('matched_keywords', [])
                # 새로운 형식: 딕셔너리 배열에서 키워드 추출
                if matched_keywords and isinstance(matched_keywords[0], dict):
                    keywords = [item.get('keyword', '') for item in matched_keywords if item.get('keyword')]
                    all_found_keywords.update(keywords)
                # 기존 형식: 문자열 배열
                else:
                    all_found_keywords.update(matched_keywords)

    if all_found_keywords:
        st.subheader("🔍 발견된 키워드로 필터링")

        # 세션 상태에서 선택된 키워드 가져오기
        if "selected_filter_keyword" not in st.session_state:
            st.session_state["selected_filter_keyword"] = "전체"

        selected_keyword = st.session_state["selected_filter_keyword"]

        # 세련된 키워드 필터 버튼들
        cols = st.columns(min(6, len(all_found_keywords) + 1))

        # 전체 버튼
        with cols[0]:
            if st.button("# 전체", key="filter_all", type="primary" if selected_keyword == "전체" else "secondary"):
                st.session_state["selected_filter_keyword"] = "전체"
                st.rerun()

        # 각 키워드 버튼
        for idx, keyword in enumerate(sorted(list(all_found_keywords)), 1):
            if idx < len(cols):
                with cols[idx]:
                    button_type = "primary" if selected_keyword == keyword else "secondary"
                    if st.button(f"# {keyword}", key=f"filter_{keyword}", type=button_type):
                        st.session_state["selected_filter_keyword"] = keyword
                        st.rerun()

        st.divider()

        # 선택된 키워드로 리뷰 필터링 및 하이라이트 표시
        selected_keyword = st.session_state.get("selected_filter_keyword", "전체")

        # 필터링된 리뷰만 표시
        filtered_comments = []
        for comment in st.session_state.comments:
            if selected_keyword == "전체":
                if comment['id'] in st.session_state.keyword_matching_results:
                    filtered_comments.append(comment)
            elif comment['id'] in st.session_state.keyword_matching_results:
                result = st.session_state.keyword_matching_results[comment['id']]
                match_result = result.get('match_result', {})
                if match_result.get('success'):
                    analysis_result = match_result.get('analysis_result', {})
                    matched_keywords = analysis_result.get('matched_keywords', [])

                    # 새로운 형식: 딕셔너리 배열에서 키워드 추출
                    if matched_keywords and isinstance(matched_keywords[0], dict):
                        keywords = [item.get('keyword', '') for item in matched_keywords if item.get('keyword')]
                    # 기존 형식: 문자열 배열
                    else:
                        keywords = matched_keywords

                    if selected_keyword in keywords:
                        filtered_comments.append(comment)

        if filtered_comments:
            st.write(f"**{selected_keyword}** 관련 리뷰: {len(filtered_comments)}개")

            for comment in reversed(filtered_comments):
                with st.container():
                    # 리뷰 내용 하이라이트 처리
                    highlighted_content = comment['content']

                    if comment['id'] in st.session_state.keyword_matching_results:
                        result = st.session_state.keyword_matching_results[comment['id']]
                        match_result = result.get('match_result', {})

                        if match_result.get('success'):
                            analysis_result = match_result.get('analysis_result', {})

                            # 선택된 키워드와 관련된 구문만 하이라이트
                            matched_keywords = analysis_result.get('matched_keywords', [])
                            phrases_to_highlight = []

                            if matched_keywords and isinstance(matched_keywords[0], dict):
                                for item in matched_keywords:
                                    item_keyword = item.get('keyword', '')
                                    original_phrase = item.get('original_phrase', '')

                                    # 선택된 키워드와 일치하거나 전체 선택일 때만 하이라이트
                                    if (selected_keyword == "전체" or item_keyword == selected_keyword) and original_phrase:
                                        phrases_to_highlight.append(original_phrase)
                            # 기존 형식: matched_phrases 배열 (전체 선택 시에만)
                            elif selected_keyword == "전체":
                                phrases_to_highlight = analysis_result.get('matched_phrases', [])

                            # 구문 하이라이트
                            for phrase in phrases_to_highlight:
                                if phrase and phrase in highlighted_content:
                                    highlighted_content = highlighted_content.replace(
                                        phrase,
                                        f'<mark style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); color: #856404; padding: 3px 8px; border-radius: 8px; font-weight: 500; box-shadow: 0 2px 6px rgba(255, 235, 59, 0.3); border: 1px solid #ffeaa7;">{phrase}</mark>'
                                    )

                    col1, col2, col3 = st.columns([4, 1, 1])

                    with col1:
                        st.write(f"**{comment['author']}**")
                        st.markdown(highlighted_content, unsafe_allow_html=True)

                        # 발견된 키워드 표시
                        if comment['id'] in st.session_state.keyword_matching_results:
                            result = st.session_state.keyword_matching_results[comment['id']]
                            match_result = result.get('match_result', {})
                            if match_result.get('success'):
                                analysis_result = match_result.get('analysis_result', {})
                                matched_keywords = analysis_result.get('matched_keywords', [])

                                # 새로운 형식: 딕셔너리 배열에서 키워드 추출
                                if matched_keywords and isinstance(matched_keywords[0], dict):
                                    keywords = [item.get('keyword', '') for item in matched_keywords if item.get('keyword')]
                                # 기존 형식: 문자열 배열
                                else:
                                    keywords = matched_keywords

                                if keywords:
                                    keywords_html = ""
                                    for kw in keywords:
                                        if kw == selected_keyword and selected_keyword != "전체":
                                            keywords_html += f'<span class="keyword-badge" style="background-color: #ff9800; color: white; font-weight: bold;">{kw}</span>'
                                        else:
                                            keywords_html += f'<span class="keyword-badge">{kw}</span>'
                                    st.markdown(f"**발견된 키워드:** {keywords_html}", unsafe_allow_html=True)

                    with col2:
                        st.caption("⭐" * comment['rating'])
                        st.caption(f"{comment['rating']}/5")

                    with col3:
                        st.caption(comment['timestamp'])

                    st.divider()
        else:
            if selected_keyword == "전체":
                st.info("키워드 검색을 먼저 실행해주세요.")
            else:
                st.info(f"'{selected_keyword}' 키워드가 포함된 리뷰가 없습니다.")
else:
    # 키워드 검색 전에도 전체 리뷰 표시
    st.subheader("📝 전체 고객 리뷰")
    st.write(f"**전체 리뷰**: {len(st.session_state.comments)}개")

    for comment in reversed(st.session_state.comments):
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.write(f"**{comment['author']}**")
                st.write(comment['content'])

            with col2:
                st.caption("⭐" * comment['rating'])
                st.caption(f"{comment['rating']}/5")

            with col3:
                st.caption(comment['timestamp'])

            st.divider()

st.divider()

# 새 리뷰 등록 섹션
st.subheader("✍️ 새 리뷰 등록")

with st.form("new_comment_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        author_name = st.text_input("작성자", placeholder="이름을 입력하세요")
        comment_content = st.text_area("리뷰 내용", placeholder="제품에 대한 리뷰를 작성해주세요", height=100)
    
    with col2:
        rating = st.selectbox("평점", [1, 2, 3, 4, 5], index=4)
    
    if st.form_submit_button("리뷰 등록", type="primary"):
        if author_name and comment_content:
            new_comment = {
                'id': max([c['id'] for c in st.session_state.comments]) + 1 if st.session_state.comments else 1,
                'author': author_name,
                'content': comment_content,
                'rating': rating,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            
            st.session_state.comments.append(new_comment)
            st.success("리뷰가 등록되었습니다!")
            st.rerun()
        else:
            st.error("작성자와 리뷰 내용을 모두 입력해주세요.")
