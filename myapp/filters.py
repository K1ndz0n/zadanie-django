import django_filters
from django.db.models import Q
from .models import Task

class TaskFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_filter")
    status = django_filters.CharFilter(field_name="status")
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    user_id = django_filters.CharFilter(method="user_id_filter")

    class Meta:
        model = Task
        fields = "__all__"

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    def user_id_filter(self, queryset, name, value):
        if value == "null":
            return queryset.filter(user_id__isnull=True)
        else:
            try:
                return queryset.filter(user_id=int(value))
            except ValueError:
                return queryset.none()

class TaskHistoryFilter(django_filters.FilterSet):
    history_id = django_filters.NumberFilter(field_name="history_id", lookup_expr="exact")
    history_user = django_filters.NumberFilter(field_name="history_user", lookup_expr="exact")
    history_date_after = django_filters.DateTimeFilter(field_name="history_date", lookup_expr="gte")
    history_date_before = django_filters.DateTimeFilter(field_name="history_date", lookup_expr="lte")
    history_date_at = django_filters.CharFilter(field_name="history_date", lookup_expr="icontains")

    class Meta:
        model = Task.history.model
        fields = "__all__"