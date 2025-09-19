import streamlit as st
from datetime import datetime
import json
import os
from PIL import Image
import base64
from io import BytesIO
import sys
sys.path.append('.')

# 감정 분석 에이전트 import 시도
try:
    from agent.sentiment_analyzer.agent import sentiment_analyzer_agent, analyze_review
    from agent.sentiment_analyzer.tools import llm_sentiment, dict_sentiment
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Sentiment Analyzer Agent import 실패: {e}")
    AGENT_AVAILABLE = False

st.set_page_config(
    page_title="댓글 분석 테스트",
    page_icon="🛍️",
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

# 감정 분석 결과 저장용 session state
if 'sentiment_analysis_results' not in st.session_state:
    st.session_state.sentiment_analysis_results = {}

# 메인 콘텐츠 영역
st.title("🛍️ 상품 댓글 분석")

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

st.subheader("💬 댓글 목록")

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
            if st.button("😍 감정분석", key=f"review_{comment['id']}", type="primary", use_container_width=True):
                if AGENT_AVAILABLE:
                    with st.spinner("감정 분석 중..."):
                        try:
                            # 감정 분석 실행
                            sentiment_result = analyze_review(comment['content'], debug_mode=True)

                            if sentiment_result['success']:
                                sentiment_data = sentiment_result['sentiment_result']

                                # 감정 분석 결과를 comment별로 저장
                                st.session_state.sentiment_analysis_results[comment['id']] = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "label": sentiment_data['label'],
                                    "score": sentiment_data['score'],
                                    "rationale": sentiment_data['rationale'],
                                    "route": sentiment_data['route'],
                                    "confidence_explanation": sentiment_data.get('confidence_explanation', ''),
                                    "review_text": comment['content'],
                                    "raw_response": sentiment_result.get('raw_response', '')
                                }
                            else:
                                # 실패한 경우도 결과 저장 (폴백 결과)
                                sentiment_data = sentiment_result['sentiment_result']
                                st.session_state.sentiment_analysis_results[comment['id']] = {
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "label": sentiment_data['label'],
                                    "score": sentiment_data['score'],
                                    "rationale": sentiment_data['rationale'],
                                    "route": sentiment_data['route'],
                                    "confidence_explanation": sentiment_data.get('confidence_explanation', ''),
                                    "review_text": comment['content'],
                                    "raw_response": sentiment_result.get('raw_response', ''),
                                    "error": sentiment_result.get('error', '')
                                }

                        except Exception as e:
                            import traceback
                            error_details = traceback.format_exc()
                            print(f"=== 감정 분석 에러 디버깅 ===")
                            print(f"에러 메시지: {str(e)}")
                            print(f"상세 스택 트레이스:")
                            print(error_details)
                            print(f"===================")

                            st.error(f"감정 분석 중 오류가 발생했습니다: {str(e)}")
                            with st.expander("상세 에러 정보"):
                                st.code(error_details)
                else:
                    st.warning("감정 분석 에이전트를 사용할 수 없습니다.")

        # 감정 분석 결과가 있으면 펼치기/접기 메뉴 표시
        if comment['id'] in st.session_state.sentiment_analysis_results:
            sentiment_result = st.session_state.sentiment_analysis_results[comment['id']]
            label = sentiment_result.get('label', '중립')
            score = sentiment_result.get('score', 0.5)
            route = sentiment_result.get('route', 'unknown')

            # 감정에 따른 아이콘 선택
            if label == '긍정':
                status_icon = "😊"
                status_color = "#22c55e"
            elif label == '부정':
                status_icon = "😞"
                status_color = "#ef4444"
            else:
                status_icon = "😐"
                status_color = "#6b7280"

            with st.expander(f"{status_icon} 감정분석 결과 - {label} ({score:.3f})", expanded=False):
                # 분석 시간
                st.write(f"**분석 시간:** {sentiment_result['timestamp']}")

                # 감정 분석 결과
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"<div style='text-align: center; padding: 20px; background-color: {status_color}15; border-radius: 10px; border: 2px solid {status_color}40;'>"
                               f"<div style='font-size: 48px;'>{status_icon}</div>"
                               f"<div style='font-size: 24px; font-weight: bold; color: {status_color}; margin-top: 10px;'>{label}</div>"
                               f"<div style='font-size: 16px; color: {status_color}; margin-top: 5px;'>점수: {score:.3f}</div>"
                               f"</div>", unsafe_allow_html=True)

                with col2:
                    st.write("**분석 근거:**")
                    st.write(sentiment_result.get('rationale', '근거 없음'))

                    st.write("**분석 경로:**")
                    route_descriptions = {
                        "llm": "Claude 3.7 LLM 분석",
                        "llm→dict": "LLM 분석 후 사전 기반 재분석",
                        "dict_fallback": "사전 기반 폴백 분석"
                    }
                    st.write(route_descriptions.get(route, route))

                    st.write("**신뢰도 설명:**")
                    st.write(sentiment_result.get('confidence_explanation', '설명 없음'))

                # 오류 정보 (있는 경우)
                if 'error' in sentiment_result and sentiment_result['error']:
                    st.error(f"분석 중 오류: {sentiment_result['error']}")

                # 원본 리뷰 텍스트
                with st.expander("원본 리뷰 텍스트", expanded=False):
                    st.code(sentiment_result.get('review_text', '텍스트 없음'), language='text')

                # 에이전트 디버깅 정보
                if 'raw_response' in sentiment_result and sentiment_result['raw_response']:
                    with st.expander("에이전트 디버깅 정보", expanded=False):
                        st.write("**에이전트 원본 응답:**")
                        st.code(sentiment_result.get('raw_response', '응답 없음'), language='text')

        st.markdown("---")

st.markdown("---")

st.subheader("✍️ 새 댓글 작성")

with st.form("comment_form"):
    col1, col2 = st.columns([3, 1])

    with col1:
        author_name = st.text_input("작성자명", placeholder="이름을 입력하세요")
        comment_content = st.text_area("댓글 내용", placeholder="상품에 대한 의견을 남겨주세요", height=100)

        uploaded_images = st.file_uploader(
            "이미지 첨부 (선택사항)",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="최대 5개의 이미지를 업로드할 수 있습니다."
        )

    with col2:
        rating = st.selectbox("평점", [5, 4, 3, 2, 1], format_func=lambda x: f"⭐ {x}점")

    submitted = st.form_submit_button("댓글 등록", type="primary")

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
            st.success("댓글이 등록되었습니다!")

            # 자동 감정 분석 수행 (AGENT_AVAILABLE인 경우)
            if AGENT_AVAILABLE:
                with st.spinner("새 댓글 자동 감정 분석 중..."):
                    try:
                        # 감정 분석 실행
                        sentiment_result = analyze_review(comment_content, debug_mode=False)

                        if sentiment_result['success']:
                            sentiment_data = sentiment_result['sentiment_result']

                            # 감정 분석 결과를 comment별로 저장
                            st.session_state.sentiment_analysis_results[new_comment['id']] = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "label": sentiment_data['label'],
                                "score": sentiment_data['score'],
                                "rationale": sentiment_data['rationale'],
                                "route": sentiment_data['route'],
                                "confidence_explanation": sentiment_data.get('confidence_explanation', ''),
                                "review_text": comment_content
                            }

                    except Exception as e:
                        st.error(f"자동 감정 분석 중 오류가 발생했습니다: {str(e)}")

            st.rerun()
        else:
            st.error("작성자명과 댓글 내용을 모두 입력해주세요.")

st.markdown("---")
