import logging
import os
from datetime import datetime
from string import Template
from typing import Any, Dict, List, Literal, Optional

from PIL.Image import Image as PILImage
from pydantic import BaseModel, Field
from strands import Agent

from .tools import check_image_product_match, check_profanity, check_rating_consistency

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)


# Unified review moderation Agent system prompt
UNIFIED_MODERATOR_PROMPT = """
    You are a review moderation expert for an e-commerce platform.

    <main_role>
    Perform moderation across the following three categories:
    - Check the review text for profanity/inappropriate expressions -> check_profanity
    - Analyze the consistency between the rating and review content -> check_rating_consistency
    - Verify the relevance between the uploaded image and the product (only if an image is present) -> check_image_product_match
    </main_role>

    <guidelines>
    - Recognize subtle differences in emotional expressions
    - Make comprehensive judgments considering the overall context
    </guidelines>

    <output_format>
    After performing all moderation checks, you must respond with the following JSON schema. Do not include any other explanations or backticks (```json), etc.:

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
        "failed_checks": ["List of failed moderation checks"]
    }

    </output_format>
"""

USER_PROMPT_TEMPLATE = Template(
    """
    Please comprehensively moderate the following review:

    Review content: $review_content
    Rating: $rating stars (1-5 scale)
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

    profanity_check: CheckResult = Field(description="Profanity/slang check result")
    rating_consistency: CheckResult = Field(description="Rating-content consistency check result")
    image_match: CheckResult = Field(description="Image-content relevance check result")
    overall_status: Literal["PASS", "FAIL"] = Field(description="Overall moderation pass/fail")
    failed_checks: List[str] = Field(description="List of failed check items")


def moderate_review(
    review_content: str,
    rating: int,
    product_data: Dict[str, Any],
    image: Optional[PILImage] = None,
) -> Dict[str, Any]:
    """
    Main function to comprehensively moderate a review

    Args:
        review_content (str): Review content
        rating (int): Rating (1-5)
        product_data (Dict[str, Any]): Product information such as name, category, etc.
        image (Optional[PILImage]): Uploaded image (PIL Image object)

    Returns:
        Dict[str, Any]: Moderation result
    """
    image_path = None
    if image:
        image_path = save_image(image)

    # Create unified moderation Agent
    unified_moderator = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[check_profanity, check_rating_consistency, check_image_product_match],
        system_prompt=UNIFIED_MODERATOR_PROMPT,
    )

    # Create user prompt
    user_prompt = USER_PROMPT_TEMPLATE.substitute(
        review_content=review_content,
        rating=rating,
        product=product_data.get("name", "Unknown"),
        category=product_data.get("category", "unknown"),
        has_image="present" if image else "none",
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


def save_image(
    image: PILImage, images_folder: str = "lab03_review_moderator/images"
) -> str:
    """
    Saves an image to the images folder and returns the path.

    Args:
        image (PILImage): PIL Image object to save
        images_folder (str): Folder path to save to (default: "images")

    Returns:
        str: Path of the saved image
    """
    os.makedirs(images_folder, exist_ok=True)

    image_format = image.format if image.format else "PNG"
    extension = image_format.lower()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"review_image_{timestamp}.{extension}"
    filepath = os.path.join(images_folder, filename)

    image.save(filepath, format=image_format)

    return filepath
