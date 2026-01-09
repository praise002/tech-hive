from unittest.mock import patch

from apps.content.models import Article, ArticleStatusChoices, Category

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# TODO: FIX ISSUE WITH FAKE REDIS
# TODO: FIX SOME ERRORS OR WARNINGS IN THE TERMINAL E.G VALUEERROR


# python manage.py test apps.content.tests.TestContents -k thread_replies
# python manage.py test apps.content.tests.TestContents.test_comment_like_toggle_unauthenticated
# python manage.py test apps.content.tests.TestArticleReactions.test_toggle_reaction_unauthenticated
# python manage.py test apps.content.tests.TestArticleReactions.test_toggle_reaction_unauthenticated

