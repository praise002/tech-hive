import django_filters
from apps.content.choices import ArticleReviewStatusChoices
from apps.content.models import Article, ArticleReview, ArticleStatusChoices, Event, Job
from django_filters import rest_framework as filters


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "company": ["iexact"],
            "location": ["iexact"],
            "job_type": ["exact"],
            "work_mode": ["exact"],
            "salary": ["lte", "gte"],
            "category": ["exact"],
        }


class EventFilter(django_filters.FilterSet):
    start_date__gte = django_filters.DateFilter(
        field_name="start_date", lookup_expr="gte", label="Start Date (After or On)"
    )
    start_date__lte = django_filters.DateFilter(
        field_name="start_date", lookup_expr="lte", label="Start Date (Before or On)"
    )
    end_date__gte = django_filters.DateFilter(
        field_name="end_date", lookup_expr="gte", label="End Date (After or On)"
    )
    end_date__lte = django_filters.DateFilter(
        field_name="end_date", lookup_expr="lte", label="End Date (Before or On)"
    )
    start_date = django_filters.DateFilter(
        field_name="start_date", lookup_expr="date", label="Start Date (Exact)"
    )
    end_date = django_filters.DateFilter(
        field_name="end_date", lookup_expr="date", label="End Date (Exact)"
    )

    class Meta:
        model = Event
        fields = []


class UserArticleFilter(filters.FilterSet):
    # status = filters.ChoiceFilter(
    #     choices=[
    #         (ArticleStatusChoices.DRAFT, "Draft"),
    #         (ArticleStatusChoices.SUBMITTED_FOR_REVIEW, "Submitted for Review"),
    #         (ArticleStatusChoices.UNDER_REVIEW, "Under Review"),
    #         (ArticleStatusChoices.CHANGES_REQUESTED, "Changes Requested"),
    #         (ArticleStatusChoices.READY, "Ready for Publishing"),
    #         (ArticleStatusChoices.PUBLISHED, "Published"),
    #         (ArticleStatusChoices.REJECTED, "Rejected"),
    #     ],
    #     help_text="Filter articles by their current status",
    # )
    # TODO:
    # status = filters.ChoiceFilter(
    #     field_name="status",
    #     choices=ArticleReviewStatusChoices.choices,
    #     help_text="Filter reviews by their current status",
    # )

    status_group = filters.ChoiceFilter(
        choices=[
            ("draft", "Draft"),
            ("submitted", "Submitted (All submission statuses)"),
            ("published", "Published"),
            ("rejected", "Rejected"),
        ],
        method="filter_by_status_group",
        help_text="Filter by status group. Use 'submitted' for all submission-related statuses.",
    )

    def filter_by_status_group(self, queryset, name, value):
        if value == "submitted":
            return queryset.filter(
                status__in=[
                    ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
                    ArticleStatusChoices.UNDER_REVIEW,
                    ArticleStatusChoices.CHANGES_REQUESTED,
                    ArticleStatusChoices.READY,
                ]
            )
        elif value == "draft":
            return queryset.filter(status=ArticleStatusChoices.DRAFT)
        elif value == "published":
            return queryset.filter(status=ArticleStatusChoices.PUBLISHED)
        elif value == "rejected":
            return queryset.filter(status=ArticleStatusChoices.REJECTED)

        return queryset

    class Meta:
        model = Article
        fields = ["status"]


class ReviewListFilter(filters.FilterSet):
    """
    Allows filtering by review status and article status.
    """

    status = filters.ChoiceFilter(
        field_name="status",
        choices=ArticleReviewStatusChoices.choices,
        help_text="Filter reviews by their current status",
    )

    article_status = filters.ChoiceFilter(
        field_name="article__status",
        choices=ArticleStatusChoices.choices,
        help_text="Filter by the status of the article being reviewed",
    )

    class Meta:
        model = ArticleReview
        fields = []
