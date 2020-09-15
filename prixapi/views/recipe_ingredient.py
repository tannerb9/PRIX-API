from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Recipe, RecipeIngredient
from prixapi.models import Ingredient, MeasurementType


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    ''' '''

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

        try:
            recipe_ingredient = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(
                recipe_ingredient, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        recipe_ingredients = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(
            recipe_ingredients, many=True, context={'request': request})
        return Response(serializer.data)
