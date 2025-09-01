from apps.content.models import Article, ArticleStatusChoices
from django_filters import rest_framework as filters


class UserArticleFilter(filters.FilterSet):
    # status = filters.ChoiceFilter(
    #     choices=[
    #         (ArticleStatusChoices.DRAFT, "Draft"),
    #         (ArticleStatusChoices.SUBMITTED_FOR_REVIEW, "Submitted for Review"),
    #         (ArticleStatusChoices.UNDER_REVIEW, "Under Review"),
    #         (ArticleStatusChoices.CHANGES_REQUESTED, "Changes Requested"),
    #         (ArticleStatusChoices.REVIEW_COMPLETED, "Review Completed"),
    #         (ArticleStatusChoices.READY, "Ready for Publishing"),
    #         (ArticleStatusChoices.PUBLISHED, "Published"),
    #         (ArticleStatusChoices.REJECTED, "Rejected"),
    #     ],
    #     help_text="Filter articles by their current status",
    # )

    # status_group = filters.ChoiceFilter(
    #     choices=[
    #         ("draft", "Draft"),
    #         ("submitted", "Submitted (All submission statuses)"),
    #         ("published", "Published"),
    #     ],
    #     # method="filter_by_status_group",
    #     help_text="Filter by status group. Use 'submitted' for all submission-related statuses.",
    # )

    # def filter_by_status_group(self, queryset, name, value):
    #     if value == "submitted":
    #         return queryset.filter(
    #             status__in=[
    #                 ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
    #                 ArticleStatusChoices.UNDER_REVIEW,
    #                 ArticleStatusChoices.CHANGES_REQUESTED,
    #                 ArticleStatusChoices.REVIEW_COMPLETED,
    #                 ArticleStatusChoices.READY,
    #             ]
    #         )
    #     elif value == "draft":
    #         return queryset.filter(status=ArticleStatusChoices.DRAFT)
    #     elif value == "published":
    #         return queryset.filter(status=ArticleStatusChoices.PUBLISHED)

    #     return queryset

    class Meta:
        model = Article
        fields = ["status"]
