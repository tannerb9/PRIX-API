from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from prixapi.models import Employee
from .user import UserSerializer


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    '''METHOD ARG(PYTHON OBJ) IS CONVERTED TO JSON
    AND ADDS VIRTUAL PROPERTY(URL) TO RESULTING JSON
    '''

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
    '''LOGIC FOR OPERATIONS THAT CAN BE PERFORMED ON RESOURCE IN API'''

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

    def update(self, request, pk=None):

        employee = Employee.objects.get(pk=pk)
        print("before", employee.user.first_name)  # Tanner
        employee.user.first_name = request.data['first_name']
        print("after", employee.user.first_name)  # Jake
        employee.user.last_name = request.data['last_name']
        employee.user.email = request.data['email']
        employee.is_admin = request.data['is_admin']
        employee.save()

        # user = self.request.auth.user

        # user = User.objects.get(pk=user_id)
        # user = User.objects.get(user=request.data.user)
        #user = User.objects.get(pk=request.data['user_id'])
        #user = User.objects.get(pk=request.data['id'])
        # print("user", user)
        current_user = Employee.objects.get(user=request.auth.user)
        print(current_user.first_name)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
