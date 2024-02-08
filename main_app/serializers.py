from rest_framework import serializers
from .models import Duck, Feeding, Feather
# beacuse user is not made the same way you import it like this
from django.contrib.auth.models import User

class FeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feather
        fields = '__all__'


class DuckSerializer(serializers.ModelSerializer):
    fed_for_today = serializers.SerializerMethodField()
    fethers = FeatherSerializer(many=True, read_only=True)
    # add the user field to the duck serializer
    user = serializers.PrimaryKeyRelatedField(read_only=True)
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


class UserSerializer(serializers.ModelSerializer):
    # Add a password field, make it write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )

      return user