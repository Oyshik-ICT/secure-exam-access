from rest_framework import serializers

class GenerateExamTokenaSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    valid_minutes = serializers.IntegerField(min_value=1)
