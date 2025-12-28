import logging
import math
import re
from typing import Dict

from apps.accounts.utils import UserRoles
from apps.content.choices import ArticleStatusChoices
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


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


def assign_reviewer():
    """
    Auto-assign reviewer using least-busy algorithm
    Returns: User object or None
    """
    from apps.content.models import ArticleReview

    reviewers = User.objects.filter(groups__name=UserRoles.REVIEWER, is_active=True)

    if not reviewers.exists():
        return None

    # Count active reviews per reviewer
    reviewer_workload = []
    for reviewer in reviewers:
        active_count = ArticleReview.objects.filter(
            reviewed_by=reviewer, is_active=True, status__in=["pending", "in_progress"]
        ).count()
        reviewer_workload.append((reviewer, active_count))

    # Sort by workload (ascending)
    reviewer_workload.sort(key=lambda x: x[1])

    # Return reviewer with least workload
    return reviewer_workload[0][0]


def assign_editor():
    """
    Auto-assign editor using least-busy algorithm
    Returns: User object or None
    """
    from apps.content.models import Article

    editors = User.objects.filter(groups__name=UserRoles.EDITOR, is_active=True)

    if not editors.exists():
        return None

    # Count active assignments per editor
    editor_workload = []
    for editor in editors:
        active_count = Article.objects.filter(
            assigned_editor=editor, status=ArticleStatusChoices.READY
        ).count()
        editor_workload.append((editor, active_count))

    # Sort by workload (ascending)
    editor_workload.sort(key=lambda x: x[1])

    # Return editor with least workload
    return editor_workload[0][0]


def get_liveblocks_permissions(user, article):
    """
    Determine Liveblocks room access level
    Returns: "WRITE", "READ", or "NONE"
    """

    # WRITE ACCESS - Can edit content
    if article.status in [
        ArticleStatusChoices.DRAFT,
        ArticleStatusChoices.CHANGES_REQUESTED,
        ArticleStatusChoices.REJECTED,
    ]:
        if article.author == user:
            return "WRITE"

    elif article.status == ArticleStatusChoices.UNDER_REVIEW:
        if article.assigned_reviewer == user:
            return "WRITE"

    elif article.status == ArticleStatusChoices.READY:
        if article.assigned_editor == user:
            return "WRITE"

    # READ ACCESS - Can view and comment
    if article.status == ArticleStatusChoices.PUBLISHED:
        # Published articles are read-only for everyone
        return "READ"

    # Allow read access to people in the workflow
    if user in [article.author, article.assigned_reviewer, article.assigned_editor]:
        return "READ"

    # NO ACCESS
    return "NONE"


# TODO:
def create_liveblocks_token(user, article, permission_level):
    pass


def sync_content_from_liveblocks(article):
    """
    Fetch latest content from Liveblocks and save to Django
    Called before critical workflow transitions
    """
    import requests
    from django.utils import timezone

    room_id = f"article-{article.id}"

    try:
        # Fetch document from Liveblocks
        response = requests.get(
            f"https://api.liveblocks.io/v2/rooms/{room_id}/storage",
            headers={"Authorization": f"Bearer {settings.LIVEBLOCKS_SECRET_KEY}"},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()

            # TODO: FIX LATER
            # Extract content (format depends on Liveblocks storage structure)
            # This will need adjustment based on actual Liveblocks data format
            # Assume the frontend stores the article content under the key "articleBody".
            # This key MUST match what your frontend code is using.
            content = data.get("articleBody", "")

            # Update article
            article.content = content
            article.content_last_synced_at = timezone.now()
            article.save(update_fields=["content", "content_last_synced_at"])

            return True
        else:
            print(f"Failed to fetch Liveblocks content: {response.status_code}")
            return False

    except Exception as e:
        print(f"Error syncing from Liveblocks: {str(e)}")
        return False


def create_workflow_history(article, from_status, to_status, changed_by, notes=None):
    """
    Create workflow history entry
    """
    from apps.content.models import ArticleWorkflowHistory

    ArticleWorkflowHistory.objects.create(
        article=article,
        from_status=from_status,
        to_status=to_status,
        changed_by=changed_by,
        notes=notes,
    )
