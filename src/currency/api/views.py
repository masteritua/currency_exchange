from rest_framework import generics, response
from currency.api.serializers import RateSerializer, ContactSerializer
from currency.models import Rate
from account.models import Contact
from datetime import datetime
from django_filters import rest_framework as filters

class RatesFilter(filters.FilterSet):
    created__gt = filters.DateTimeFilter(field_name="created", lookup_expr='gt')
    created__gte = filters.DateTimeFilter(field_name="created", lookup_expr='gte')
    created__lt = filters.DateTimeFilter(field_name="created", lookup_expr='lt')
    created__lte = filters.DateTimeFilter(field_name="created", lookup_expr='lte')
    created__exact = filters.DateTimeFilter(field_name="created", lookup_expr='exact')
    created__range = filters.DateFromToRangeFilter(field_name="created", lookup_expr='range')
    currency__exact = filters.NumberFilter(field_name="currency", lookup_expr='exact')
    source__exact = filters.NumberFilter(field_name="source", lookup_expr='exact')

    class Meta:
        model = Rate
        fields = ['id', 'created', 'currency', 'source']


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RatesFilter

class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class ContactFilter(filters.FilterSet):

    class Meta:
        model = Contact
        fields = ['email', 'title', 'body', ]

class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects
    serializer_class = ContactSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContactFilter


class ContactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer