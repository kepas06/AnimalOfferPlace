from django.contrib.auth.models import User
from offers.models import Question, Offer, Category
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstname', 'username', 'email', 'groups')