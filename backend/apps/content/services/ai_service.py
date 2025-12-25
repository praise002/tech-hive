import logging
from typing import Optional

from decouple import config
from django.conf import settings
from django.core.cache import caches
from groq import Groq

logger = logging.getLogger(__name__)


class GroqAIService:
    """Service for interacting with GROQ AI API"""

    def __init__(self):
        self.client = Groq(api_key=config("GROQ_API_KEY"))
        self.model = config("GROQ_MODEL")
        self.cache = caches["summaries"]

    def _get_cache_key(self, article_id: str) -> str:
        """Generate cache key for article summary"""
        return f"summary:{article_id}"

    def _clean_content(self, html_content: str) -> str:
        """Strip HTML tags and clean content for AI processing"""
        import re
        from html import unescape

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", html_content)
        # Unescape HTML entities
        text = unescape(text)
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Limit length
        max_length = settings.ARTICLE_SUMMARY_MAX_CONTENT_LENGTH
        if len(text) > max_length:
            text = text[:max_length] + "..."

        return text

    def _generate_summary_prompt(self, title: str, content: str) -> str:
        """Create the prompt for GROQ AI"""
        return f"""You are a technical content summarizer. Summarize the following article in bullet points.

                Article Title: {title}

                Article Content:
                {content}

                Requirements:
                - Provide 3-5 concise bullet points
                - Each bullet point should be one clear sentence
                - Focus on key takeaways and main ideas
                - Use technical language appropriate for developers
                - Start each bullet point with a dash (-)
                - Do not include any introduction or conclusion, just the bullet points

                Summary:"""

    def get_cached_summary(self, article_id: str) -> Optional[dict]:
        """Retrieve cached summary if available"""
        cache_key = self._get_cache_key(article_id)
        cached_data = self.cache.get(cache_key)

        if cached_data:
            logger.info(f"Cache HIT for article {article_id}")
            return cached_data

        logger.info(f"Cache MISS for article {article_id}")
        return None

    def generate_summary(
        self, article_id: str, title: str, content: str, force_regenerate: bool = False
    ) -> dict:
        """
        Generate article summary using GROQ AI

        Args:
            article_id: UUID of the article
            title: Article title
            content: Article HTML content
            force_regenerate: If True, bypass cache and regenerate

        Returns:
            dict with summary data including 'summary' and 'cached' fields
        """
        # Check cache first (unless force regenerate)
        if not force_regenerate:
            cached = self.get_cached_summary(article_id)
            if cached:
                return {**cached, "cached": True}

        # Clean the content
        clean_content = self._clean_content(content)

        if not clean_content or len(clean_content) < 50:
            raise ValueError("Article content is too short to summarize")

        # Generate prompt
        prompt = self._generate_summary_prompt(title, clean_content)

        try:
            # Call GROQ API
            logger.info(f"Calling GROQ API for article {article_id}")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.3,  # Lower temperature for more consistent summaries
                max_tokens=500,
            )

            # Extract summary
            summary = chat_completion.choices[0].message.content.strip()

            # Prepare result
            result = {
                "summary": summary,
                "article_id": article_id,
                "cached": False,
            }

            # Cache the result
            cache_key = self._get_cache_key(article_id)
            self.cache.set(
                cache_key,
                {"summary": summary, "article_id": article_id},
            )

            logger.info(
                f"Successfully generated and cached summary for article {article_id}"
            )

            return result

        except Exception as e:
            logger.error(f"Error generating summary for article {article_id}: {str(e)}")
            raise


# Singleton instance
groq_service = GroqAIService()
