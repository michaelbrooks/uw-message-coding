from rest_framework import filters
from models import Message
from django import forms


class MultipleOpenEndedField(forms.MultipleChoiceField):
    """A multiple choice field that doesn't check against a list of valid choices."""
    def valid_value(self, value):
        return True


class MultipleOpenEndedFilter(filters.django_filters.MultipleChoiceFilter):
    """
    A filter whose value is an array, such as id__in,
    but unlike a MultipleChoiceFilter, there is no "choices" list.
    """

    field_class = MultipleOpenEndedField
    always_filter = False

    def filter(self, qs, value):
        value = value or ()  # Make sure we have an iterable

        if self.is_noop(qs, value):
            return qs

        # Even though not a noop, no point filtering if empty
        if not value:
            return qs

        param = '%s__%s' % (self.name, self.lookup_type)
        return qs.filter(**{param: value}).distinct()


class SelectionFilter(filters.FilterSet):
    filter_version = 1.0

    id__in = MultipleOpenEndedFilter(name='id', lookup_type='in')
    pk__in = MultipleOpenEndedFilter(name='pk', lookup_type='in')

    class Meta:
        model = Message
        fields = {
            'id': ['exact', 'in'],
            'dataset': ['exact'],
            'text': ['icontains'],
            'time': ['lte', 'gte'],
            'sender': ['exact', 'iexact'],
        }
