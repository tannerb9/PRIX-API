from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from prixapi.models import Employee, Company
from .user import UserSerializer


# Method arg(Python obj) is converted to JSON and
# adds virtual property(url) to resulting JSON
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
    '''Logic for operations that can be performed on API resources'''

    def create(self, request):
        '''Handles POST request
        Returns: Response -- JSON string of a User instance
        '''

        company = Company.objects.get(pk=request.data['company_id'])
        user = User.objects.create_user(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        employee = Employee.objects.create(
            is_admin=request.data['is_admin'],
            user=user,
            company=company
        )

        return Response({}, status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        '''Handle GET request
        Returns: Response -- JSON string of an Employee instance
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
        of a company
        '''

        employees = Employee.objects.all()

        # Example GET request:
        #   http://localhost:8000/employee?company=1
        company = self.request.query_params.get('company', None)
        if company is not None:
            employees = Employee.objects.filter(company_id=company)

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''Handle PUT request
        Returns: Response -- Empty obj and 204 status code
        '''

        employee = Employee.objects.get(pk=pk)
        employee.is_admin = request.data['is_admin']
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
        """

        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
