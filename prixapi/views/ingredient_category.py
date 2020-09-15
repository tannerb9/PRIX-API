from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from prixapi.models import IngredientCategory


class IngredientCategorySerializer(serializers.HyperlinkedModelSerializer):
    '''JSON SERIALIZER FOR INGREDIENT CATEGORIES
    ARG: USES HYPERLINKS(NOT PKS) TO REPRESENT RELATIONS
    '''

    class Meta:
        model = IngredientCategory
        url = serializers.HyperlinkedIdentityField(
            view_name='ingredient category',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class IngredientCategoryView(ViewSet):
    '''PRIX INGREDIENT CATEGORY'''

    def create(self, request):
        '''CREATES INSTANCE OF INGREDIENT CATEGORY AND SAVES TO DB'''

        ingreadient_category = IngredientCategory()
        ingreadient_category.name = request.data['name']
        ingreadient_category.save()

        serializer = IngredientCategorySerializer(
            ingreadient_category, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''HANDLE GET REQUEST FOR SINGLE INGREDIENT CATEGORY
        RETURNS: RESPONSE -- JSON STRING OF INGREDIENT CATEGORY INSTANCE
        '''

        try:
            ingredient_category = IngredientCategory.objects.get(pk=pk)
            serializer = IngredientCategorySerializer(
                ingredient_category, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        '''HANDLE GET REQUEST FOR ALL INGREDIENT CATEGORIES
        RETURNS: RESPONSE -- JSON STRING OF ALL INGREDIENT CATEGORY INSTANCES
        '''

        ingredient_categories = IngredientCategory.objects.all()
        serializer = IngredientCategorySerializer(
            ingredient_categories, many=True, context={'request': request})
        return Response(serializer.data)
