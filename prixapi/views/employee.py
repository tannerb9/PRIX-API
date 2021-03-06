from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from prixapi.models import Employee, Company
from .user import UserSerializer
from rest_framework.authtoken.models import Token
from .company import CompanySerializer


# Method arg(Python obj) is converted to JSON and
# adds virtual property(url) to resulting JSON
class EmployeeSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()
    company = CompanySerializer()

    class Meta:
        model = Employee
        url = serializers.HyperlinkedIdentityField(
            view_name='employee',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'company', 'is_admin')
        depth = 2


class EmployeeView(ViewSet):
    '''Logic for operations that can be performed on API resources'''

    def create(self, request):
        '''Handles POST request
        Returns: Response -- JSON string of a User instance

        Example POST request
        http://localhost:8000/employee
        '''

        user = request.auth.user
        employee = Employee.objects.filter(user=user)[0]
        company = Company.objects.filter(id=employee.company_id)[0]

        new_user = User.objects.create_user(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        employee = Employee.objects.create(
            is_admin=request.data['is_admin'],
            user=new_user,
            company=company
        )

        token = Token.objects.create(user=new_user)

        return Response({}, status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        '''Handle GET request
        Returns: Response -- JSON string of an Employee instance

        Example GET request
        http://localhost:8000/employee/1
        '''

        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(
                employee, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''Handles GET request
        Returns: Response -- JSON string of all Employee instances
        of logged-in user's company

        Example GET request:
        http://localhost:8000/employee
        '''

        # user = request.auth.user
        employee = Employee.objects.get(user=request.auth.user)
        company = Company.objects.filter(id=employee.company_id)[0]
        employees = Employee.objects.filter(company_id=company)

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''Handle PUT request
        Returns: Response -- Empty obj and 204 status code

        Example PUT request
        http://localhost:8000/employee/1
        '''

        adminStatus = request.data['is_admin']
        if adminStatus == "true":
            adminStatus = True
        else:
            adminStatus = False

        employee = Employee.objects.get(pk=pk)
        employee.is_admin = adminStatus
        employee.save()

        user = User.objects.get(pk=employee.user.id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.email = request.data['email']
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request
        Returns:
            Response -- 200 or 404 status code

        Example DELETE request
        http://localhost:8000/employee/1
        """

        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
