import math
from apps.accounts.models import User

import string
import logging

logger = logging.getLogger(__name__)


class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
            "password": "Testpassword2008@",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
            "password": "Verified2001#",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def other_verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Other",
            "email": "testotheruser@example.com",
            "is_email_verified": True,
            "password": "Testpassword2008@",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def disabled_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Disabled",
            "email": "testdisabled@example.com",
            "is_email_verified": True,
            "user_active": False,
            "password": "Testpassword789#",
        }
        user = User.objects.create_user(**user_dict)
        return user

# Constants for assumptions in our read length algorithm 
AVERAGE_WORDS_PER_MINUTE = 238
SYLLABLE_LETTER_COUNT = 3
BASE_SENTENCE_WORD_COUNT = 21
BASE_SYLLABLE_COUNT = 1.5 


class ReadLength:
    def calculate_difficulty_multiplier(average_syllable, average_sentence_length):
        difficulty_multiplier = 1
        syllable_length_multiplier = ReadLength.calculate_syllable_multiplier(average_syllable)
        sentence_length_multiplier = ReadLength.calculate_sentence_length_multiplier(average_sentence_length)
        
        return (difficulty_multiplier + (syllable_length_multiplier + sentence_length_multiplier))
    
    def calculate_syllable_multiplier(average_syllable):
        if average_syllable > BASE_SYLLABLE_COUNT:
            return ((average_syllable - BASE_SYLLABLE_COUNT) % 0.3) * 0.05
        return 0
    
    def calculate_sentence_length_multiplier(average_sentence_length):
        if average_sentence_length > BASE_SENTENCE_WORD_COUNT:
            return ((average_sentence_length - BASE_SENTENCE_WORD_COUNT) % 0.5) * 0.05
        return 0
    
    def calculate_read_time(text: str) -> int:
        text_without_division_punctuation = text.replace(".", '|').replace('!', '|').replace('?', '|')
        word_count = len(text_without_division_punctuation.split(' '))
        
        text_sentences = text_without_division_punctuation.split('|')
        sentence_count = len(text_sentences)
        average_sentence_length = word_count / sentence_count
        
        text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
        text_words = text_without_punctuation.split()
        syllable_count = sum(len(word) % 3 for word in text_words)
        
        average_syllable_count = word_count / syllable_count
        
        difficulty_multiplier = ReadLength.calculate_difficulty_multiplier(average_syllable_count, average_sentence_length)
        reading_speed = math.ceil(word_count / (AVERAGE_WORDS_PER_MINUTE / difficulty_multiplier))
        
        return reading_speed