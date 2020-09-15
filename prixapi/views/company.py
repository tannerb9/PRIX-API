from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from prixapi.models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    '''JSON SERIALIZER FOR COMPANIES
    ARG: USES HYPERLINKS(NOT PKs) TO REPRESENT RELATIONS
    '''

    class Meta:
        model = Company
        url = serializers.HyperlinkedIdentityField(
            view_name='company',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class CompanyView(ViewSet):
    '''CLIENT OF PRIX'''

    def create(self, request):
        '''CREATES INSTANCE OF COMPANY AND SAVES TO DB'''

        company = Company()
        company.name = request.data["name"]
        company.save()

        serializer = CompanySerializer(company, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''HANDLE GET REQUEST FOR SINGLE COMPANY
        RETURNS: RESPONSE -- JSON STRING OF COMPANY INSTANCE
        '''

        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(
                company, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        companies = Company.objects.all()
        serializer = CompanySerializer(
            companies, many=True, context={'request': request})
        return Response(serializer.data)
