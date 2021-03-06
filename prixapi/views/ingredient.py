from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Ingredient, Company, Employee
from prixapi.models import MeasurementType, IngredientCategory


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    ''' '''

    class Meta:

        model = Ingredient
        url = serializers.HyperlinkedIdentityField(
            view_name='ingredient',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'purchase_price',
                  'purchase_quantity', 'measurement_type',
                  'measurement_type_id', 'employee',
                  'ingredient_category', 'ingredient_category_id')
        depth = 2


class IngredientView(ViewSet):

    def create(self, request):
        '''Handles POST request
        Returns: Reseponse -- JSON string of Ingredient instance
        '''

        # Gets current user and finds associated employee
        user = request.auth.user
        employee = Employee.objects.filter(user=user)[0]

        # Gets measurement_type.id that's sent with request
        measurement_type = MeasurementType.objects.get(
            pk=request.data['measurement_type_id'])

        # Gets ingredient_category.id that's sent with request
        ingredient_category = IngredientCategory.objects.get(
            pk=request.data['ingredient_category_id'])

        # Instantiates and saves Ingredient instance
        ingredient = Ingredient()
        ingredient.name = request.data['name']
        ingredient.purchase_price = request.data['purchase_price']
        ingredient.purchase_quantity = request.data['purchase_quantity']
        ingredient.measurement_type = measurement_type
        ingredient.ingredient_category = ingredient_category
        ingredient.employee = employee
        ingredient.save()

        serializer = IngredientSerializer(
            ingredient, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Handles GET request
        Returns: Response -- JSON string of an Ingredient instance

        Example GET request:
        http://localhost:8000/ingredient/1
        '''

        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(
                ingredient, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''Handles GET request
        Returns: Response -- JSON string of all Ingredient
        instances of logged-in user's company

        Example GET requests:
        http://localhost:8000/ingredient
        http://localhost:8000/ingredient?ingredientCategory=2
        '''

        user = request.auth.user
        employee = Employee.objects.filter(user=user)[0]
        company = Company.objects.filter(id=employee.company_id)[0]
        ingredients = Ingredient.objects.filter(
            employee__company=company)

        ingredient_category = self.request.query_params.get(
            'ingredientCategory', None)

        if ingredient_category is not None:
            ingredients = Ingredient.objects.filter(
                ingredient_category_id=ingredient_category)

        serializer = IngredientSerializer(
            ingredients, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''Handles PUT request
        Returns: Response -- Empty obj and 204 status code

        Example PUT request:
        http://localhost:8000/ingredient/1
        '''

        user = request.auth.user
        employee = Employee.objects.filter(user=user)[0]

        measurement_type = MeasurementType.objects.get(
            pk=request.data['measurement_type_id'])
        ingredient_category = IngredientCategory.objects.get(
            pk=request.data['ingredient_category_id'])

        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.name = request.data['name']
        ingredient.purchase_price = request.data['purchase_price']
        ingredient.purchase_quantity = request.data['purchase_quantity']
        ingredient.measurement_type = measurement_type
        ingredient.ingredient_category = ingredient_category
        ingredient.employee = employee
        ingredient.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request
        Returns: Response -- 204 or 404 status code

        Example DELETE request:
        http://localhost:8000/ingredient/1
        """

        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
