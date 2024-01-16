from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['id','username','email']
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required =True,validators = [UniqueValidator(User.objects.all())])
    password = serializers.CharField(write_only = True,required= True,validators =[validate_password])
    repeat_password = serializers.CharField(write_only = True,required= True)
    class Meta:
        model = User
        fields =['username','email','password','repeat_password']

        extra_kwargs = {
            'username':{'required': True}
        }
    
    def validate(self,attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError('Password do not match!')
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

     
    

#class UserLoginSerializer(serializers.Serializer):
   # username = serializers.CharField(required = True)
    #password = serializers.CharField(required = True)

# serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)
    


