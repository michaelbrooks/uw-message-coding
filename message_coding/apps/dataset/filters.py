# Stuff for filtering Messages in support of dataset selection objects

from rest_framework import filters

class AbstractFilter(object):
    def __init__(self, data=None, query_params=None):
        """Create filter from filter data or query_params"""
        if data is None and query_params is not None:
            data = self.parse_query_params(query_params)
        elif data is None:
            raise ValueError("Filter data or query params must be provided.")

        self.data = self.clean_data(data)

    def parse_query_params(self, params):
        """Load filter data from URL query params"""
        return params

    def clean_data(self, data):
        """Return a cleaned data object"""
        return data

    def filter(self, queryset):
        """Return a filtered queryset"""

        if self.is_noop():
            return queryset

        return self._filter(queryset)

    def is_noop(self):
        """Return true if the filter doesn't do anything"""
        return False

    def _filter(self, queryset):
        """Override this to actually filter the queryset"""
        return queryset


class BasicDjangoFilter(AbstractFilter):
    """
    A filter that assumes it receives a flat dictionary of
    key-value pairs that are all valid queryset filter parameters
    for the target class.
    """

    # Dictionary that builds a list of filter parameters.
    # Keys should be model fields, values
    # should be lists of queryset lookup types
    # https://docs.djangoproject.com/en/dev/ref/models/querysets/#id4
    allowed_params = {
        'id': ['exact', 'in'],
        'pk': ['exact', 'in'],
        'text': ['icontains', 'contains'],
        'sender': ['exact', 'iexact'],
        'time': ['lt', 'gt', 'lte', 'gte'],
        'dataset': ['exact'],
        'dataset_id': ['exact'],
    }

    def get_allowed_params(self):
        allowed = []
        for field, lookups in self.allowed_params.iteritems():
            for lookup in lookups:
                if lookup == 'exact':
                    param = field
                else:
                    param = "%s__%s" % (field, lookup)
                allowed.append(param)
        return allowed

    def parse_query_params(self, params):
        """Get the filter data from the request"""
        filter_data = {}
        for key in params.keys():
            if key.endswith("__in"):
                value = params.getlist(key)
            else:
                value = params.get(key)

            filter_data[key] = value
        return filter_data

    def is_noop(self):
        return len(self.data) == 0

    def clean_data(self, data):
        # A default value
        if data is None:
            return {}

        # Make sure it's a dictionary
        if not isinstance(data, (dict,)):
            raise ValueError("Filter data must be a dictionary.")

        clean = {}
        simple_types = (basestring, float, int,)
        allowed_params = self.get_allowed_params()

        # Make sure it is a flat dictionary (but it can include arrays)
        for key, value in data.iteritems():

            # Skip invalid parameters
            if key not in allowed_params:
                continue

            # Is it an array?
            if isinstance(value, (list, tuple,)):

                # It's values should all be simple
                for el in value:
                    if not isinstance(el, simple_types):
                        raise ValueError("Array value for filter data %s contains an invalid value." % key)

            # Then it must be simple
            elif not isinstance(value, simple_types):
                raise ValueError("Filter data value %s is invalid." % key)

            # It's good
            clean[key] = value

        return super(BasicDjangoFilter, self).clean_data(clean)

    def _filter(self, queryset):
        return queryset.filter(**self.data)


class MessageFilter(object):
    """
    A generic message filter object that looks
    up the proper filter implementation based on
    the given filter type.
    """

    default_filter_type = 'json'
    filter_class_by_type = {
        "json": BasicDjangoFilter,
    }

    def __init__(self, type, data=None, query_params=None, *args, **kwargs):
        """
        Use 'type' to select which type of filter to create.
        Either the data and query_params argument should be provided
        to initialize the filter.
        """

        self.type = type

        filter_class = self.filter_class_by_type[type]
        self._filter = filter_class(data=data, query_params=query_params, *args, **kwargs)

    def get_filter_data(self):
        return self._filter.data

    def __call__(self, queryset=None):
        if self._filter is not None:
            return self._filter.filter(queryset=queryset)
        else:
            return queryset


class MessageFilterBackend(filters.BaseFilterBackend):
    """
    A basic filter backend for Django Rest Framework
    http://www.django-rest-framework.org/api-guide/filtering/
    """

    def filter_queryset(self, request, queryset, view):
        filter_type = MessageFilter.default_filter_type
        filter_fn = MessageFilter(filter_type, query_params=request.query_params)

        result = filter_fn(queryset)
        return result


