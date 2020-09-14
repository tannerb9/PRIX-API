from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from prixapi.models import Employee
from .user import UserSerializer


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Employee
        url = serializers.HyperlinkedIdentityField(
            view_name='employee',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'company', 'is_admin')
        depth = 2


class EmployeeView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(
                employee, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        employees = Employee.objects.all()
        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)
