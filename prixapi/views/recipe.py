from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Recipe, RecipeCategory, Employee


# Uses hyperlinks(not pks) to represent relations
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        url = serializers.HyperlinkedIdentityField(
            view_name='recipe',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'servings_per_batch', 'batch_sale_price',
                  'serving_sale_price', 'recipe_category', 'employee')
        depth = 2


class RecipeView(ViewSet):
    '''Logic for operations that can be performed on API resources'''

    def create(self, request):
        '''Handles POST request
        Returns: Response -- JSON string of a Recipe instance
        '''

        employee = Employee.objects.get(pk=request.data['employee_id'])

        recipe_category = RecipeCategory.objects.get(
            pk=request.data['recipe_category_id'])

        recipe = Recipe()
        recipe.name = request.data['name']
        recipe.servings_per_batch = request.data['servings_per_batch']
        recipe.batch_sale_price = request.data['batch_sale_price']
        recipe.serving_sale_price = request.data['serving_sale_price']
        recipe.recipe_category = recipe_category
        recipe.employee = employee
        recipe.save()

        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Handle GET request
        Returns: Response -- JSON string of a Recipe instance
        '''

        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''Handles GET request
        Returns: Response -- JSON string of all Recipe instances
        of a company
        '''

        recipes = Recipe.objects.all()

        # Example GET request:
        #   http://localhost:8000/recipe?company=1
        company = self.request.query_params.get('company', None)
        if company is not None:

            # Uses one table(employee) to filter on query param(company)
            recipes = Recipe.objects.filter(employee__company_id=company)

        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''Handles PUT request
        Returns: Response -- Empty obj and 204 status code
        '''

        employee = Employee.objects.get(pk=request.data['employee_id'])

        recipe_category = RecipeCategory.objects.get(
            pk=request.data['recipe_category_id'])

        recipe = Recipe.objects.get(pk=pk)
        recipe.name = request.data['name']
        recipe.servings_per_batch = request.data['servings_per_batch']
        recipe.batch_sale_price = request.data['batch_sale_price']
        recipe.serving_sale_price = request.data['serving_sale_price']
        recipe.recipe_category = recipe_category
        recipe.employee = employee
        recipe.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request
        Returns: Response -- 200 or 404 status code
        """

        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
