from rest_framework import serializers

class AppealSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=20, required=True)
    title = serializers.CharField(max_length=60, required=True)
    text = serializers.CharField(max_length=1488, required=True)