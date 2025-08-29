from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Exam


class GenerateExamTokenaSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    valid_minutes = serializers.IntegerField(min_value=1)


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["title", "start_time", "end_time"]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["name", "email"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class AccessExamSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            "exam": ExamSerializer(instance.exam).data,
            "student": UserSerializer(instance.student).data,
        }
