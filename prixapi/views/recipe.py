from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import Recipe, RecipeCategory
from prixapi.models import RecipeIngredient, Employee


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    ''' '''
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
    ''' '''

    def create(self, request):

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

        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request})
        return Response(serializer.data)
