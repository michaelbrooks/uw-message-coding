from rest_framework import filters
from models import Message
from django import forms

class SelectionFilter(filters.FilterSet):
    id = filters.django_filters.MultipleChoiceFilter(lookup_type='in')
    
    class Meta:
        model = Message
        fields = {
            # 'id': ['exact', 'in'],
            'dataset': ['exact'],
            'text': ['icontains'],
            'time': ['lte', 'gte'],
            'sender': ['iexact'],
        }
        
class Selector(object):
    def __init__(self, data):
        self.data = data
    
    def filter(self, queryset):
        return SelectionFilter(data=self.data, queryset=queryset).qs

