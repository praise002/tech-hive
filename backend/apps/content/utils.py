import math
import string

from django.db import models


class ArticleStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED_FOR_REVIEW = "submitted_for_review", "Submitted for Review"
    UNDER_REVIEW = "under_review", "Under Review"
    CHANGES_REQUESTED = "changes_requested", "Changes Requested"
    REVIEW_COMPLETED = "review_completed", "Review Completed"
    READY = "ready_for_publishing", "Ready for Publishing"
    PUBLISHED = "published", "Published"
    REJECTED = "rejected", "Rejected"
    # ARCHIVED = "archived", "Archived"


# Constants for assumptions in our read length algorithm
AVERAGE_WORDS_PER_MINUTE = 238
SYLLABLE_LETTER_COUNT = 3
BASE_SENTENCE_WORD_COUNT = 21
BASE_SYLLABLE_COUNT = 1.5


class ReadLength:
    def calculate_difficulty_multiplier(average_syllable, average_sentence_length):
        difficulty_multiplier = 1
        syllable_length_multiplier = ReadLength.calculate_syllable_multiplier(
            average_syllable
        )
        sentence_length_multiplier = ReadLength.calculate_sentence_length_multiplier(
            average_sentence_length
        )

        return difficulty_multiplier + (
            syllable_length_multiplier + sentence_length_multiplier
        )

    def calculate_syllable_multiplier(average_syllable):
        if average_syllable > BASE_SYLLABLE_COUNT:
            return ((average_syllable - BASE_SYLLABLE_COUNT) % 0.3) * 0.05
        return 0

    def calculate_sentence_length_multiplier(average_sentence_length):
        if average_sentence_length > BASE_SENTENCE_WORD_COUNT:
            return ((average_sentence_length - BASE_SENTENCE_WORD_COUNT) % 0.5) * 0.05
        return 0

    def calculate_read_time(text: str) -> int:
        text_without_division_punctuation = (
            text.replace(".", "|").replace("!", "|").replace("?", "|")
        )
        word_count = len(text_without_division_punctuation.split(" "))

        text_sentences = text_without_division_punctuation.split("|")
        sentence_count = len(text_sentences)
        average_sentence_length = word_count / sentence_count

        text_without_punctuation = text.translate(
            str.maketrans("", "", string.punctuation)
        )
        text_words = text_without_punctuation.split()
        syllable_count = sum(len(word) % 3 for word in text_words)

        average_syllable_count = word_count / syllable_count

        difficulty_multiplier = ReadLength.calculate_difficulty_multiplier(
            average_syllable_count, average_sentence_length
        )
        reading_speed = math.ceil(
            word_count / (AVERAGE_WORDS_PER_MINUTE / difficulty_multiplier)
        )

        return reading_speed
