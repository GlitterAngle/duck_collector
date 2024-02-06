from rest_framework import serializers
from .models import Duck, Feeding, Feather

class FeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feather
        fields = '__all__'


class DuckSerializer(serializers.ModelSerializer):
    fed_for_today = serializers.SerializerMethodField()
    fethers = FeatherSerializer(many=True, read_only=True)
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


