import django_filters
from apps.content.models import Event, Job


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
