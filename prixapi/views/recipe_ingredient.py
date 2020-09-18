from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Recipe, RecipeIngredient
from prixapi.models import Ingredient, MeasurementType


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeIngredient
        url = serializers.HyperlinkedIdentityField(
            view_name='recipe ingredient',
            lookup_field='id'
        )
        fields = ('id', 'url', 'quantity', 'recipe',
                  'ingredient', 'measurement_type')
        depth = 2


class RecipeIngredientView(ViewSet):

    def create(self, request):
        '''Handles POST request
        Returns: Response -- JSON string of RecipeIngredient instance
        '''

        recipe = Recipe.objects.get(pk=request.data['recipe_id'])
        ingredient = Ingredient.objects.get(
            pk=request.data['ingredient_id'])
        measurement_type = MeasurementType.objects.get(
            pk=request.data['measurement_type_id'])

        recipe_ingredient = RecipeIngredient()
        recipe_ingredient.quantity = request.data['quantity']
        recipe_ingredient.measurement_type = measurement_type
        recipe_ingredient.ingredient = ingredient
        recipe_ingredient.recipe = recipe
        recipe_ingredient.save()

        serializer = RecipeIngredientSerializer(
            recipe_ingredient, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''Handles GET request
        Returns: Respone -- JSON string of RecipeIngredient instance

        Example GET request:
        http://localhost:8000/recipeingredient/1
        '''

        try:
            recipe_ingredient = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(
                recipe_ingredient, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''Handles GET request
        Returns: Response -- JSON string of all RecipeIngredient
        instances of a recipe

        Example GET request:
        http://localhost:8000/recipeingredient?recipe=1
        '''

        recipe_ingredients = RecipeIngredient.objects.all()
        recipe = self.request.query_params.get('recipe', None)

        if recipe is not None:

            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe_id=recipe)

        serializer = RecipeIngredientSerializer(
            recipe_ingredients, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''Handles PUT request
        Returns: Response -- Empty obj and 204 status code

        Example PUT request:
        http://localhost:8000/recipeingredient/1
        '''

        recipe = Recipe.objects.get(pk=request.data['recipe_id'])
        ingredient = Ingredient.objects.get(
            pk=request.data['ingredient_id'])
        measurement_type = MeasurementType.objects.get(
            pk=request.data['measurement_type_id'])

        recipe_ingredient = RecipeIngredient.objects.get(pk=pk)
        recipe_ingredient.quantity = request.data['quantity']
        recipe_ingredient.measurement_type = measurement_type
        recipe_ingredient.ingredient = ingredient
        recipe_ingredient.recipe = recipe
        recipe_ingredient.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request
        Returns: Response -- 204 or 404 status code

        Example DELETE request:
        http://localhost:8000/recipeingredient/1
        """

        try:
            recipe_ingredient = RecipeIngredient.objects.get(pk=pk)
            recipe_ingredient.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RecipeIngredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
