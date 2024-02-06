from rest_framework import serializers
from .models import Duck, Feeding

class DuckSerializer(serializers.ModelSerializer):
    fed_for_today = serializers.SerializerMethodField()
    class Meta:
        model = Duck
        fields = '__all__'

    def get_fed_for_today(self, obj):
        return obj.fed_for_today()

class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = '__all__'
        read_only_fields = ('duck',)

