import logging
import math
import re
from typing import Dict

from django.core.cache import caches
from django.db import models

logger = logging.getLogger(__name__)

class ArticleStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED_FOR_REVIEW = "submitted_for_review", "Submitted for Review"
    UNDER_REVIEW = "under_review", "Under Review"
    CHANGES_REQUESTED = "changes_requested", "Changes Requested"
    READY = "ready_for_publishing", "Ready for Publishing"
    PUBLISHED = "published", "Published"
    REJECTED = "rejected", "Rejected"
    # ARCHIVED = "archived", "Archived"


class ReadabilityMetrics:

    @staticmethod
    def count_syllables(word: str) -> int:
        syllable_count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            syllable_count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                syllable_count += 1

        if word.endswith("e"):
            syllable_count -= 1
        if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1
        if syllable_count == 0:
            syllable_count += 1
        return syllable_count

    @staticmethod
    def analyze_text(text: str) -> Dict[str, float]:
        """Extract basic text metrics."""
        # Clean text
        text_clean = re.sub(r"```[\s\S]*?```", "", text)
        text_clean = re.sub(r"!\[.*?\]\(.*?\)", "", text_clean)

        # Count sentences
        sentence_pattern = r"[.!?]+(?:\s+|$)"
        sentences = [
            s.strip() for s in re.split(sentence_pattern, text_clean) if s.strip()
        ]
        sentence_count = max(1, len(sentences))

        # Count words
        words = text_clean.split()
        word_count = len(words)

        if word_count == 0:
            return {"words": 0, "sentences": 0, "syllables": 0}

        # Count syllables
        text_no_punct = re.sub(r"[^\w\s]", "", text_clean)
        clean_words = text_no_punct.split()
        syllable_count = sum(ReadabilityMetrics.count_syllables(w) for w in clean_words)

        return {
            "words": word_count,
            "sentences": sentence_count,
            "syllables": syllable_count,
            "avg_syllables_per_word": syllable_count / word_count,
            "avg_words_per_sentence": word_count / sentence_count,
        }

    @staticmethod
    def method_hybrid(text: str, base_wpm: int = 265) -> Dict[str, any]:
        """
        FLESCH READING EASE METHOD
        Formula: 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
        Score:
        - 90-100(very easy)
        - 80-89(easy)
        - 70-79(fairly easy)
        - 60-69(standard)
        - 50-59(fairly difficult)
        - 30-49(difficult)
        - 0-29(very confusing)

        - 70-100(fairly easy - very easy)
        - 60-69(standard)
        - 30-59(difficult - fairly difficult)
        - 0-29(very confusing)
        """

        metrics = ReadabilityMetrics.analyze_text(text)

        if metrics["words"] == 0:
            return {"method": "Hybrid", "minutes": 0, "seconds": 0}

        # 1. Calculate Flesch Reading Ease
        asl = metrics["avg_words_per_sentence"]
        asw = metrics["avg_syllables_per_word"]
        flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)
        flesch_score = max(0, min(100, flesch_score))

        # 2. Base speed adjustment from Flesch
        if flesch_score >= 70:
            base_multiplier = 1.1
        elif flesch_score >= 60:
            base_multiplier = 1.0
        elif flesch_score >= 30:
            base_multiplier = 0.85
        else:
            base_multiplier = 0.7

        # 3. Fine-tune with custom thresholds
        fine_tune = 1.0

        # Very long sentences slow reading
        if asl > 30:
            fine_tune *= 0.95
        elif asl > 25:
            fine_tune *= 0.9

        # Very complex words slow reading
        if asw > 2.5:
            fine_tune *= 0.95
        elif asw > 2.0:
            fine_tune *= 0.9

        # 4. Content type adjustments
        image_count = len(re.findall(r"!\[.*?\]\(.*?\)", text))
        code_block_count = len(re.findall(r"```[\s\S]*?```", text))

        image_time = 0
        for i in range(image_count):
            time_for_image = max(3, 12 - i)  # Start at 12, decrease by 1, minimum 3
            image_time += time_for_image

        code_time = code_block_count * 20  # 20 seconds per code block

        # 5. Calculate final reading time
        adjusted_wpm = base_wpm * base_multiplier * fine_tune
        text_time = (metrics["words"] / adjusted_wpm) * 60
        total_seconds = text_time + image_time + code_time

        return math.ceil(total_seconds)

# Not needed because once article is published it can't be updated
def invalidate_article_summary_cache(article_id: str):
    """
    Invalidate cached summary for an article
    
    Usage:
        When article is updated
        invalidate_article_summary_cache(str(article.id))
    """
    cache = caches['summaries']
    cache_key = f"summary:{article_id}"
    cache.delete(cache_key)
    logger.info(f"Invalidated summary cache for article {article_id}")    