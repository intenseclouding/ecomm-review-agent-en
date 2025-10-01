import json
import os
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any

from keyword_extractor.agent import search_keywords

# 키워드 저장 파일 경로
KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "keyword_extractor", "registered_keywords.txt")

def load_keywords() -> List[str]:
    """등록된 키워드 목록 로드"""
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
            return keywords
    return []

def save_keywords(keywords: List[str]):
    """키워드 목록 저장"""
    with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
        for keyword in keywords:
            f.write(f"{keyword}\n")

def register_keyword(keyword: str) -> Dict[str, Any]:
    """새로운 키워드 등록"""
    # 기존 키워드 로드
    keywords = load_keywords()

    # 중복 체크
    if keyword in keywords:
        return {
            "status": "already_exists",
            "keyword": keyword,
            "total_keywords": len(keywords)
        }

    # 새 키워드 추가
    keywords.append(keyword)

    # 저장
    save_keywords(keywords)

    return {
        "status": "registered",
        "keyword": keyword,
        "total_keywords": len(keywords)
    }


# 키워드 추출 헬퍼 함수
def extract_keywords_from_result(match_result: Dict[str, Any]) -> List[str]:
    """매칭 결과에서 키워드 목록을 추출"""
    if not match_result.get('success'):
        return []

    analysis_result = match_result.get('analysis_result', {})
    matched_keywords = analysis_result.get('matched_keywords', [])

    if not matched_keywords:
        return []

    # 새로운 형식: 딕셔너리 배열
    if isinstance(matched_keywords[0], dict):
        return [item.get('keyword', '') for item in matched_keywords if item.get('keyword')]
    # 기존 형식: 문자열 배열
    else:
        return matched_keywords

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
    .product-rating-container h3 {
        margin: 0 0 16px 0;
    }
    .product-rating-container p {
        margin: 4px 0;
        color: #1f2937;
    }
    .rating-card {
        background-color: #fff;
        border-radius: 14px;
        padding: 20px 24px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.04);
    }
    .rating-card .metric-label {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 4px;
    }
    .rating-card .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 8px;
    }
    .rating-card .metric-description {
        font-size: 14px;
        color: #475569;
    }
    @media (max-width: 1024px) {
        .product-rating-grid {
            grid-template-columns: 1fr;
        }
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

# 제품 정보 및 평점 계산
total_reviews = len(st.session_state.comments)
total_rating = sum([comment['rating'] for comment in st.session_state.comments])
average_rating = total_rating / total_reviews if total_reviews else 0

# 제품 정보 섹션 (최상단 이동)
st.markdown(
    f"""
    <div class="product-rating-container">
        <div class="product-rating-grid">
            <div>
                <h3>📦 상품 정보</h3>
                <p><strong>상품명:</strong> 프리미엄 무선 이어폰</p>
                <p><strong>가격:</strong> 89,000원</p>
                <p><strong>상품 설명:</strong></p>
                <p>고품질 사운드와 긴 배터리 수명을 자랑하는 프리미엄 무선 이어폰입니다. 노이즈 캔슬링 기능과 편안한 착용감을 제공합니다.</p>
            </div>
            <div class="rating-card">
                <div class="metric-label">현재 평점</div>
                <div class="metric-value">{average_rating:.1f} / 5.0</div>
                <div class="metric-description">총 {total_reviews}개 리뷰</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 키워드 관리 섹션
st.subheader("🏷️ 키워드 관리")

# 등록된 키워드 표시 및 새 키워드 등록 버튼
col1, col2 = st.columns([4, 1])

with col1:
    st.write("**등록된 키워드 (클릭하여 필터링)**")
    registered_keywords = load_keywords()

    # 선택된 키워드 세션 상태 초기화
    if "selected_keyword_filter" not in st.session_state:
        st.session_state["selected_keyword_filter"] = None

    if registered_keywords:
        # 키워드를 버튼으로 표시 (한 줄에 여러 개)
        cols = st.columns(min(8, len(registered_keywords)))
        for idx, keyword in enumerate(registered_keywords):
            with cols[idx % len(cols)]:
                is_selected = st.session_state.get("selected_keyword_filter") == keyword
                button_type = "primary" if is_selected else "secondary"
                if st.button(f"#{keyword}", key=f"keyword_filter_{keyword}", type=button_type, use_container_width=True):
                    # 토글 동작: 같은 키워드 클릭하면 선택 해제, 다른 키워드 클릭하면 선택
                    if st.session_state["selected_keyword_filter"] == keyword:
                        st.session_state["selected_keyword_filter"] = None
                    else:
                        st.session_state["selected_keyword_filter"] = keyword
                    st.rerun()
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

            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("🏷️ 등록", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ 취소", use_container_width=True)

            if submit:
                if new_keyword:
                    try:
                        with st.spinner("키워드 등록 중..."):
                            result = register_keyword(new_keyword)
                            if result.get('status') == 'already_exists':
                                st.warning(f"⚠️ 키워드 '{new_keyword}'는 이미 등록되어 있습니다.")
                            else:
                                st.success(f"✅ 키워드 '{new_keyword}' 등록 완료!")
                                st.session_state["show_keyword_modal"] = False
                                st.rerun()
                    except Exception as e:
                        st.error(f"❌ 키워드 등록 실패: {str(e)}")
                else:
                    st.error("키워드를 입력해주세요.")

            if cancel:
                st.session_state["show_keyword_modal"] = False
                st.rerun()

        st.markdown("---")

st.divider()

# 리뷰 섹션
st.subheader("📝 고객 리뷰")

# 선택된 키워드 필터 가져오기
selected_keyword = st.session_state.get("selected_keyword_filter", None)

for comment in reversed(st.session_state.comments):
    # 필터링 체크
    show_comment = True
    if selected_keyword:  # 키워드가 선택된 경우에만 필터링
        # 선택된 키워드가 있을 때만 필터링
        if comment['id'] in st.session_state.keyword_matching_results:
            result = st.session_state.keyword_matching_results[comment['id']]
            match_result = result.get('match_result', {})
            keywords = extract_keywords_from_result(match_result)
            show_comment = selected_keyword in keywords
        else:
            show_comment = False

    if show_comment:
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

                    if matched_keywords:
                        # 새로운 형식: 딕셔너리 배열
                        if isinstance(matched_keywords[0], dict):
                            for item in matched_keywords:
                                item_keyword = item.get('keyword', '')
                                original_phrase = item.get('original_phrase', '')

                                # 선택된 키워드와 일치하거나 선택 없을 때만 하이라이트
                                if (not selected_keyword or item_keyword == selected_keyword) and original_phrase:
                                    phrases_to_highlight.append(original_phrase)
                        # 기존 형식: 문자열 배열 - matched_phrases 사용
                        else:
                            if not selected_keyword:
                                phrases_to_highlight = analysis_result.get('matched_phrases', [])
                            else:
                                # 특정 키워드 선택 시, 해당 키워드의 구문만 추출
                                all_phrases = analysis_result.get('matched_phrases', [])
                                phrases_to_highlight = all_phrases  # 기존 형식에서는 전체 구문 사용

                    # 구문 하이라이트
                    for phrase in phrases_to_highlight:
                        if phrase and phrase in highlighted_content:
                            highlighted_content = highlighted_content.replace(
                                phrase,
                                f'<mark style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); color: #856404; padding: 3px 8px; border-radius: 8px; font-weight: 500; box-shadow: 0 2px 6px rgba(255, 235, 59, 0.3); border: 1px solid #ffeaa7;">{phrase}</mark>'
                            )

            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

            with col1:
                st.write(f"**{comment['author']}**")
                st.markdown(highlighted_content, unsafe_allow_html=True)

                # 발견된 키워드 표시 (분석된 경우에만)
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
                                if kw == selected_keyword and selected_keyword:
                                    keywords_html += f'<span class="keyword-badge" style="background-color: #ff9800; color: white; font-weight: bold;">{kw}</span>'
                                else:
                                    keywords_html += f'<span class="keyword-badge">{kw}</span>'
                            st.markdown(f"**발견된 키워드:** {keywords_html}", unsafe_allow_html=True)

            with col2:
                st.caption("⭐" * comment['rating'])
                st.caption(f"{comment['rating']}/5")

            with col3:
                st.caption(comment['timestamp'])

            with col4:
                # 개별 키워드 분석 버튼
                button_label = "✅ 재분석" if comment['id'] in st.session_state.keyword_matching_results else "🔍 키워드 분석"
                if st.button(button_label, key=f"search_{comment['id']}", type="primary", use_container_width=True):
                    with st.spinner("키워드 검색 중..."):
                        try:
                            match_result = search_keywords(comment['content'])
                            st.session_state.keyword_matching_results[comment['id']] = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "review_text": comment['content'],
                                "match_result": match_result
                            }
                            st.success("✅ 분석 완료!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"키워드 검색 중 오류: {str(e)}")

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
