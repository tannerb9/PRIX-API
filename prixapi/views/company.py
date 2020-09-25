from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        url = serializers.HyperlinkedIdentityField(
            view_name='company',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'employee')


class CompanyView(ViewSet):
    '''PRIX Client'''

    def create(self, request):
        '''Creates instance of company and saves to DB

        Example POST request:
        http://localhost:8000/company
        '''

        company = Company()
        company.name = request.data["name"]
        company.save()

        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Handle GET request for a company instance
        Returns: Response -- JSON string of company instance

        Example GET request:
        http://localhost:8000/company/1
        '''

        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(
                company, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''Handle GET request for all company instances
        Returns: Response -- JSON string of all company instances

        Example GET request:
        http://localhost:8000/company
        '''

        companies = Company.objects.all()
        serializer = CompanySerializer(
            companies, many=True, context={'request': request})
        return Response(serializer.data)
