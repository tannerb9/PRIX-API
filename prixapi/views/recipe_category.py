from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from prixapi.models import RecipeCategory


class RecipeCategorySerializer(serializers.HyperlinkedModelSerializer):
    ''' '''

    class Meta:

        model = RecipeCategory
        url = serializers.HyperlinkedIdentityField(
            view_name='recipe category',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class RecipeCategoryView(ViewSet):
    ''' '''

    def create(self, request):
        ''' '''
        recipe_category = RecipeCategory()
        recipe_category.name = request.data['name']
        recipe_category.save()

        serializer = RecipeCategorySerializer(
            recipe_category, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ''' '''
        try:
            recipe_category = RecipeCategory.objects.get(pk=pk)
            serializer = RecipeCategorySerializer(
                recipe_category, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        recipe_categories = RecipeCategory.objects.all()
        serializer = RecipeCategorySerializer(
            recipe_categories, many=True, context={'request': request})
        return Response(serializer.data)
