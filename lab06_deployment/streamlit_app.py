import streamlit as st
from datetime import datetime
import json
import os
from PIL import Image
import base64
from io import BytesIO
import sys
sys.path.append('.')

# 종합 분석 오케스트레이터 import 시도
try:
    from agent.orchestrator.agent import comprehensive_analyzer
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Comprehensive Analyzer Agent import 실패: {e}")
    AGENT_AVAILABLE = False

st.set_page_config(
    page_title="종합 리뷰 분석 시스템",
    page_icon="🔬",
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
    .keyword-badges {
        margin-top: 24px;
    }
    .keyword-badges h3 {
        margin-bottom: 12px;
    }
    .keyword-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 999px;
        background-color: rgba(79, 70, 229, 0.12);
        color: #4338ca;
        font-size: 13px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-weight: 500;
        letter-spacing: -0.01em;
    }
    .keyword-badge::before {
        content: "#";
        margin-right: 2px;
    }
    .analysis-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .status-approved {
        border-left: 4px solid #10b981;
        background: #ecfdf5;
    }
    .status-rejected {
        border-left: 4px solid #ef4444;
        background: #fef2f2;
    }
    .highlight-box {
        background: #f8fafc;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #6366f1;
    }
    @media (max-width: 1024px) {
        .product-rating-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def base64_to_image(img_str):
    img_data = base64.b64decode(img_str)
    img = Image.open(BytesIO(img_data))
    return img

if 'comments' not in st.session_state:
    # 이미지 미리 로드
    flower_img_base64 = ""
    earphone_img_base64 = ""

    try:
        flower_img = Image.open("images/flower.webp")
        flower_img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        flower_img_base64 = image_to_base64(flower_img)
    except:
        pass

    try:
        earphone_img = Image.open("images/earphone.png")
        earphone_img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        earphone_img_base64 = image_to_base64(earphone_img)
    except:
        pass

    st.session_state.comments = [
        {
            "id": 1,
            "author": "김민수",
            "rating": 5,
            "content": "이 제품 정말 좋아요! 음질도 훌륭하고 배터리도 오래 갑니다.",
            "timestamp": "2024-01-15 14:30",
            "images": []
        },
        {
            "id": 2,
            "author": "이영희",
            "rating": 1,
            "content": "완전 쓰레기네요. 돈 아까워요.",
            "timestamp": "2024-01-14 10:20",
            "images": []
        },
        {
            "id": 3,
            "author": "박철수",
            "rating": 5,
            "content": "별로예요. 기대했는데 실망이에요.",
            "timestamp": "2024-01-13 16:45",
            "images": []
        },
        {
            "id": 4,
            "author": "최지훈",
            "rating": 4,
            "content": "이어폰 디자인이 깔끔하고 착용감도 편해요. 음질은 가격대비 괜찮은 것 같아요. 아침에 운동할 때 써봤는데 떨어지지도 않고 좋네요!",
            "timestamp": "2024-01-12 09:15",
            "images": [earphone_img_base64] if earphone_img_base64 else []
        },
        {
            "id": 5,
            "author": "정수연",
            "rating": 3,
            "content": "이어폰 만만세",
            "timestamp": "2024-01-11 16:22",
            "images": [flower_img_base64] if flower_img_base64 else []
        }
    ]

# 종합 분석 결과 저장용 session state
if 'comprehensive_analysis_results' not in st.session_state:
    st.session_state.comprehensive_analysis_results = {}

# 메인 콘텐츠 영역
st.title("🔬 종합 리뷰 분석 시스템")

total_reviews = len(st.session_state.comments)
total_rating = sum([comment['rating'] for comment in st.session_state.comments])
average_rating = total_rating / total_reviews if total_reviews else 0

keywords = ["가성비", "배송", "재질", "음질", "디자인", "편의성"]
keywords_html = "".join(f'<span class="keyword-badge">{kw}</span>' for kw in keywords)

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
            <div>
                <div class="rating-card">
                    <div class="metric-label">현재 평점</div>
                    <div class="metric-value">{average_rating:.1f} / 5.0</div>
                    <div class="metric-description">총 {total_reviews}개 리뷰</div>
                </div>
                <div class="keyword-badges">
                    <h3>🏷️ 검색 키워드</h3>
                    {keywords_html}
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("💬 리뷰 목록 및 종합 분석")

for comment in reversed(st.session_state.comments):
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.write(f"**{comment['author']}**")
            st.write(comment['content'])

            if 'images' in comment and comment['images']:
                st.write("📷 **첨부된 이미지:**")
                img_cols = st.columns(min(len(comment['images']), 3))
                for idx, img_str in enumerate(comment['images']):
                    with img_cols[idx % 3]:
                        try:
                            img = base64_to_image(img_str)
                            st.image(img, width=150, caption=f"이미지 {idx+1}")
                        except Exception as e:
                            st.error(f"이미지를 불러올 수 없습니다: {e}")

        with col2:
            # 통일된 스타일의 별점 표시
            stars_html = ""
            for i in range(5):
                if i < comment['rating']:
                    stars_html += '<span style="color: #fbbf24; font-size: 18px;">★</span>'
                else:
                    stars_html += '<span style="color: #d1d5db; font-size: 18px;">★</span>'

            st.markdown(stars_html, unsafe_allow_html=True)
            st.caption(f"{comment['rating']}/5")

        with col3:
            st.caption(comment['timestamp'])

        with col4:
            if st.button("🔬 종합분석", key=f"comprehensive_analysis_{comment['id']}", type="primary", use_container_width=True):
                if AGENT_AVAILABLE:
                    with st.spinner("종합 리뷰 분석 중..."):
                        try:
                            # 리뷰 데이터 준비
                            review_data = {
                                "review_id": comment['id'],
                                "content": comment['content'],
                                "rating": comment['rating'],
                                "author": comment['author'],
                                "timestamp": comment['timestamp'],
                                "images": comment.get('images', [])
                            }

                            # 종합 분석 실행
                            analysis_result = comprehensive_analyzer(review_data)

                            # 결과를 session state에 저장
                            st.session_state.comprehensive_analysis_results[comment['id']] = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "analysis_result": analysis_result,
                                "review_data": review_data
                            }

                        except Exception as e:
                            import traceback
                            error_details = traceback.format_exc()
                            print(f"=== 종합 분석 에러 디버깅 ===")
                            print(f"에러 메시지: {str(e)}")
                            print(f"상세 스택 트레이스:")
                            print(error_details)
                            print(f"===================")

                            st.error(f"종합 분석 중 오류가 발생했습니다: {str(e)}")
                            with st.expander("상세 에러 정보"):
                                st.code(error_details)
                else:
                    st.warning("종합 분석 에이전트를 사용할 수 없습니다.")

        # 종합 분석 결과가 있으면 표시
        if comment['id'] in st.session_state.comprehensive_analysis_results:
            result_data = st.session_state.comprehensive_analysis_results[comment['id']]
            analysis = result_data.get('analysis_result', {})

            # ReviewAnalysis 구조에 따른 결과 표시
            moderation_result = analysis.get('moderation_result', {})
            is_approved = moderation_result.get('approved', False)

            # 검수 결과에 따른 상태 표시
            if is_approved:
                status_class = "status-approved"
                status_icon = "✅"
                status_text = "검수 통과"
            else:
                status_class = "status-rejected"
                status_icon = "❌"
                status_text = "검수 실패"

            with st.expander(f"{status_icon} 종합 분석 결과 - {status_text}", expanded=True):
                # 분석 시간
                st.write(f"**분석 시간:** {result_data['timestamp']}")

                # 1. 검수 결과
                st.markdown("### 1️⃣ 리뷰 검수 결과")
                with st.container():
                    st.markdown(f'<div class="analysis-card {status_class}">', unsafe_allow_html=True)

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"**상태:** {status_text}")
                        if 'confidence' in moderation_result:
                            st.markdown(f"**신뢰도:** {moderation_result['confidence']:.3f}")

                    with col2:
                        st.markdown("**검수 사유:**")
                        if 'reason' in moderation_result:
                            st.write(moderation_result['reason'])
                        else:
                            st.write("검수 사유 정보 없음")

                    st.markdown('</div>', unsafe_allow_html=True)

                # 검수 실패 시 이후 단계 생략
                if not is_approved:
                    st.warning("⚠️ 리뷰가 검수를 통과하지 못하여 이후 분석 단계가 생략되었습니다.")
                else:
                    # 2. 키워드 분석 결과
                    st.markdown("### 2️⃣ 키워드 분석 결과")
                    keyword_highlights = analysis.get('keyword_highlighted_list', [])

                    if keyword_highlights:
                        for highlight in keyword_highlights:
                            keyword = highlight.get('keyword', '')
                            sentences = highlight.get('sentences', [])

                            st.markdown(f'<div class="highlight-box">', unsafe_allow_html=True)
                            st.markdown(f"**키워드:** `{keyword}`")
                            st.markdown("**관련 문장들:**")
                            for sentence in sentences:
                                st.markdown(f"• {sentence}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("추출된 키워드가 없습니다.")

                    # 3. 감정 분석 결과
                    st.markdown("### 3️⃣ 감정 분석 결과")
                    sentiment = analysis.get('sentiment', '정보 없음')

                    # 감정에 따른 색상 및 아이콘
                    if '긍정' in sentiment:
                        sentiment_color = "#22c55e"
                        sentiment_icon = "😊"
                    elif '부정' in sentiment:
                        sentiment_color = "#ef4444"
                        sentiment_icon = "😞"
                    else:
                        sentiment_color = "#6b7280"
                        sentiment_icon = "😐"

                    st.markdown(f'<div class="analysis-card" style="border-left: 4px solid {sentiment_color};">', unsafe_allow_html=True)
                    st.markdown(f"{sentiment_icon} **감정:** {sentiment}")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 4. 자동 응답 결과
                    st.markdown("### 4️⃣ 자동 응답")
                    auto_response = analysis.get('auto_response', '응답 생성 정보 없음')

                    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                    st.markdown("**생성된 셀러 응답:**")
                    st.markdown(f'<div style="background: #f8fafc; padding: 16px; border-radius: 8px; border-left: 3px solid #3b82f6;">{auto_response}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # 원본 데이터
                with st.expander("📋 원본 리뷰 데이터", expanded=False):
                    st.json(result_data.get('review_data', {}))

                # 전체 분석 결과 (디버깅용)
                with st.expander("🔧 전체 분석 결과 (디버깅)", expanded=False):
                    st.json(analysis)

        st.markdown("---")

st.markdown("---")

st.subheader("✍️ 새 리뷰 작성")

with st.form("comment_form"):
    col1, col2 = st.columns([3, 1])

    with col1:
        author_name = st.text_input("작성자명", placeholder="이름을 입력하세요")
        comment_content = st.text_area("리뷰 내용", placeholder="상품에 대한 의견을 남겨주세요", height=100)

        uploaded_images = st.file_uploader(
            "이미지 첨부 (선택사항)",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="최대 5개의 이미지를 업로드할 수 있습니다."
        )

    with col2:
        rating = st.selectbox("평점", [5, 4, 3, 2, 1], format_func=lambda x: f"⭐ {x}점")

    submitted = st.form_submit_button("리뷰 등록", type="primary")

    if submitted:
        if author_name and comment_content:
            images_base64 = []

            if uploaded_images:
                if len(uploaded_images) > 5:
                    st.error("최대 5개의 이미지만 업로드할 수 있습니다.")
                    st.stop()

                for uploaded_file in uploaded_images:
                    try:
                        image = Image.open(uploaded_file)

                        max_size = (800, 600)
                        image.thumbnail(max_size, Image.Resampling.LANCZOS)

                        img_base64 = image_to_base64(image)
                        images_base64.append(img_base64)
                    except Exception as e:
                        st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")
                        st.stop()

            new_comment = {
                "id": len(st.session_state.comments) + 1,
                "author": author_name,
                "rating": rating,
                "content": comment_content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "images": images_base64
            }
            st.session_state.comments.append(new_comment)
            st.success("리뷰가 등록되었습니다!")

            # 자동 종합 분석 수행 (AGENT_AVAILABLE인 경우)
            if AGENT_AVAILABLE:
                with st.spinner("새 리뷰 자동 종합 분석 중..."):
                    try:
                        # 리뷰 데이터 준비
                        review_data = {
                            "review_id": new_comment['id'],
                            "content": comment_content,
                            "rating": rating,
                            "author": author_name,
                            "timestamp": new_comment['timestamp'],
                            "images": images_base64
                        }

                        # 종합 분석 실행
                        analysis_result = comprehensive_analyzer(review_data)

                        # 결과를 session state에 저장
                        st.session_state.comprehensive_analysis_results[new_comment['id']] = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "analysis_result": analysis_result,
                            "review_data": review_data
                        }

                        st.success("자동 종합 분석이 완료되었습니다!")

                    except Exception as e:
                        st.error(f"자동 종합 분석 중 오류가 발생했습니다: {str(e)}")

            st.rerun()
        else:
            st.error("작성자명과 리뷰 내용을 모두 입력해주세요.")

st.markdown("---")