from rest_framework import serializers
from .models import Student, Coach, Tag, Team
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'tagname')

class  StudentSerializer(serializers.ModelSerializer):
    # tagname = serializers.RelatedField(read_only=True)
    tag = TagSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'user', 'tag')

class  CoachSerializer(serializers.ModelSerializer):
    # tagname = serializers.RelatedField(read_only=True)
    tag = TagSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'user', 'tag')

class TeamSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True, many=True)
    coach = CoachSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = ('id', 'coach', 'student')