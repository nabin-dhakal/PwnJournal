from rest_framework import serializers
from core.models import Writeup, UserProfile, Comments
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class WriteupSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Writeup
        fields = '__all__'
        read_only_fields=['author','post','update']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    DP = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'username', 'email', 'contact', 'DP']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comments
        fields ='__all__'
        read_only_fields=['author','onwriteup']