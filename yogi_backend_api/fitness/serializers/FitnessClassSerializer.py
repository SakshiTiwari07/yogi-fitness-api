from rest_framework import serializers
from fitness.models.FitnessClassModel import FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'


