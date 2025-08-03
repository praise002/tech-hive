import django_filters

from .models import Tag

# TODO: REMOVE LATER
class TagFilter(django_filters.FilterSet):

    class Meta:
        model = Tag
        fields = {
            "name": ["iexact"],
        }
