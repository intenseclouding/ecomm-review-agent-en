import logging
import os
from datetime import datetime
from string import Template
from typing import Any, Dict, List, Literal, Optional

from PIL.Image import Image as PILImage
from pydantic import BaseModel, Field
from strands import Agent, tool

from .tools import check_image_product_match, check_profanity, check_rating_consistency

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)


# Unified Review Moderation Agent System Prompt
UNIFIED_MODERATOR_PROMPT = """
    You are a review moderation expert for an e-commerce platform.

    <main_role>
    Please perform moderation in the following three categories.
    - Check the review text for profanity/inappropriate expressions -> check_profanity
    - Analyze the consistency between the rating and review content -> check_rating_consistency
    - Verify the relevance between the uploaded image and the product (only when an image is present.) -> check_image_product_match
    </main_role>

    <guidelines>
    - Recognize subtle differences in Korean emotional expressions
    - Make comprehensive judgments considering the overall context
    </guidelines>

    <overall_status_rules>
    - If profanity_check is FAIL, overall_status must be set to "FAIL"
    - If profanity_check is PASS, overall_status is set to "PASS" even if rating_consistency or image_match is FAIL
    - In other words, only the profanity/inappropriate content check determines the overall pass/fail of the moderation
    </overall_status_rules>

    <output_format>
    After performing all checks, please respond with the following JSON schema. Do not include any other explanations or backticks (```json), etc.:

    {
        "profanity_check": {
            "status": "PASS|FAIL|SKIP",
            "reason": "Specific basis for judgment (required)",
            "confidence": 0.0-1.0
        },
        "rating_consistency": {
            "status": "PASS|FAIL|SKIP",
            "reason": "Specific basis for judgment (required)",
            "confidence": 0.0-1.0
        },
        "image_match": {
            "status": "PASS|FAIL|SKIP",
            "reason": "Specific basis for judgment (required)",
            "confidence": 0.0-1.0
        },
        "overall_status": "PASS|FAIL",
        "failed_checks": ["List of failed check items"]
    }

    </output_format>
"""

USER_PROMPT_TEMPLATE = Template(
    """
    Please comprehensively moderate the following review:

    Review content: $review_content
    Rating: $rating points (1-5 scale)
    Product: $product
    Category: $category
    Image: $has_image ($image_path)
    """
)


class CheckResult(BaseModel):
    """Individual check result"""

    status: Literal["PASS", "FAIL", "SKIP"] = Field(description="Check status")
    reason: str = Field(description="Specific basis for judgment (required)")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence (0.0-1.0)")


class ReviewModerationResult(BaseModel):
    """Review moderation analysis result"""

    profanity_check: CheckResult = Field(description="Profanity/swear word check result")
    rating_consistency: CheckResult = Field(description="Rating-content consistency check result")
    image_match: CheckResult = Field(description="Image-content relevance check result")
    overall_status: Literal["PASS", "FAIL"] = Field(description="Overall moderation pass/fail status")
    failed_checks: List[str] = Field(description="List of failed check items")


@tool
def moderate_review(
    review_content: str,
    rating: int,
    product_data: Dict[str, Any],
    image_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main function to comprehensively moderate a review

    Args:
        review_content (str): Review content
        rating (int): Rating (1-5)
        product_data (Dict[str, Any]): Product information including name, category, etc.
        image_path (Optional[str]): Uploaded image path

    Returns:
        Dict[str, Any]: Moderation result
    """

    # Create unified moderation Agent
    unified_moderator = Agent(
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        tools=[check_profanity, check_rating_consistency, check_image_product_match],
        callback_handler=None,
        system_prompt=UNIFIED_MODERATOR_PROMPT,
    )

    # Generate user prompt
    user_prompt = USER_PROMPT_TEMPLATE.substitute(
        review_content=review_content,
        rating=rating,
        product=product_data.get("name", "Unknown"),
        category=product_data.get("category", "unknown"),
        has_image="present" if image_path else "none",
        image_path=image_path if image_path else "none",
    )

    # Run unified moderation Agent
    unified_response = unified_moderator(user_prompt)

    # Structured Output
    moderated_result = unified_moderator.structured_output(
        ReviewModerationResult, "Structure the model's comprehensive review moderation result."
    )

    return {
        "success": True,
        "moderation_result": moderated_result,
        "raw_response": str(unified_response),
    }
