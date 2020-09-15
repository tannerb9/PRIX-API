from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'first_name', 'last_name', 'email')


class UserView(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
