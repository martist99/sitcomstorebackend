from rest_framework import serializers
from .models import User


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Profile
#         fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','email','first_name','last_name','password']
        extra_kwargs = {
            'password' : {'write_only': True},
            'id':{'read_only':True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user