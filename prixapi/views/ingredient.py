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
                  'purchase_quantity', 'measurement_type', 'ingredient_category')
        depth = 2


class IngredientView(ViewSet):

    def create(self, request):

        # GETS EMPLOYEE THAT'S SENT WITH REQUEST
        employee = Employee.objects.get(pk=request.data['employee_id'])

        # GETS MEASUREMENT TYPE THAT'S SENT WITH REQUEST
        measurement_type = MeasurementType.objects.get(
            pk=request.data['measurement_type_id'])
        # GETS INGREDIENT CATEGORY THAT'S SENT WITH REQUEST
        ingredient_category = IngredientCategory.objects.get(
            pk=request.data['ingredient_category_id'])

        # INSTANTIATES AND SAVES INGREDIENT INSTANCE
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

        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(
                ingredient, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        ingredients = Ingredient.objects.all()

        # Example GET request:
        #   http://localhost:8000/ingredient?company=1
        company = self.request.query_params.get('company', None)
        if company is not None:

            ingredients = Ingredient.objects.filter(
                employee__company_id=company)

        serializer = IngredientSerializer(
            ingredients, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

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
        ingredient.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
