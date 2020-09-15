from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import MeasurementType


class MeasurementTypeSerializer(serializers.HyperlinkedModelSerializer):
    ''' '''

    class Meta:
        model = MeasurementType
        url = serializers.HyperlinkedIdentityField(
            view_name='measurement type',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class MeasurementTypeView(ViewSet):
    ''' '''

    def create(self, request):

        measurement_type = MeasurementType()
        measurement_type.name = request.data['name']
        measurement_type.save()

        serializer = MeasurementTypeSerializer(
            measurement_type, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ''' '''

        try:
            measurement_type = MeasurementType.objects.get(pk=pk)
            serializer = MeasurementTypeSerializer(
                measurement_type, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        measurement_types = MeasurementType.objects.all()
        serializer = MeasurementTypeSerializer(
            measurement_types, many=True, context={'request': request})
        return Response(serializer.data)
