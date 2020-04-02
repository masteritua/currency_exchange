from rest_framework import generics, response
from currency.api.serializers import RateSerializer
from currency.models import Rate
from account.models import Contact
from datetime import datetime
from account.tasks import send_create_api


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects
    serializer_class = RateSerializer

    def list(self, request):

        get = request.GET
        string_query = ''

        if get.get('created__lt'):

            string_query = f"created__lt='{datetime.strptime(get.get('created__lt'), '%m/%d/%Y')}'"

        elif get.get('created__lte'):

            string_query = f"created__lte={datetime.strptime(get.get('created__lte'), '%m/%d/%Y')}"

        elif get.get('created__exact'):

            string_query = f"created__exact={datetime.strptime(get.get('created__exact'), '%m/%d/%Y')}"

        elif get.get('created__gt'):

            string_query = f"created__gt={datetime.strptime(get.get('created__gt'), '%m/%d/%Y')}"

        elif get.get('created__gte'):

            string_query = f"created__gte={datetime.strptime(get.get('created__gte'), '%m/%d/%Y')}"

        elif get.get('created__range'):

            string_query = f"created__gte={datetime.strptime(get.get('created__range'), '%m/%d/%Y')}"

        elif get.get('currency__exact'):

            string_query = f"currency__exact={get.get('currency__exact')}"

        elif get.get('source__exact'):

            string_query = f"source__exact={get.get('source__exact')}"


        if string_query:

            queryset = self.queryset.filter(string_query)

        else:

            queryset = self.queryset.all()

        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data)


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects
    serializer_class = ContactSerializer

    def list(self, request):

        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data)

    def perform_create(self, serializer):
        send_create_api.delay()

class ContactsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer