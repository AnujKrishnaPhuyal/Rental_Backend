from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','username','email','password']

    def validate(self, data):
           
        username = data.get('username')
        print(username)
        email = data.get('email')
        # Check if username is unique
        if NewUser.objects.filter(username=username).exists():
            return Response({"status":401,'error':"Username already in use"})
        
        # Check if email is unique
        if NewUser.objects.filter(email=email).exists():
            return Response({"status":402,'error':"email already in use"})
        
        return data    

    def create(self, validated_data):
        user = NewUser.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class New_user(serializers.ModelSerializer):
     class Meta:
        model = NewUser
        fields = ['id','username','email']


class Alldata(serializers.ModelSerializer):
    class Meta:
        model = properties
        exclude = ('user',)



class UserPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        property_instance = Property.objects.create(user=user, **validated_data)
        return property_instance
     
    def update(self, instance, validated_data):
        print(validated_data)
        print(instance.name, instance.img1, instance.description)      
        for attr, value in validated_data.items():
                setattr(instance, attr, value)
        instance.save()
        return instance

class AlldataSerializer(serializers.ModelSerializer):
    img1 = serializers.SerializerMethodField()
    img2 = serializers.SerializerMethodField()
    img3 = serializers.SerializerMethodField()
    daley_image = serializers.SerializerMethodField()

    class Meta:
        model = properties
        # fields = '__all__'
        exclude=('user',)

    def get_img1(self, obj):
        return self.get_full_url(obj.img1)

    def get_img2(self, obj):
        return self.get_full_url(obj.img2)

    def get_img3(self, obj):
        return self.get_full_url(obj.img3)

    def get_daley_image(self, obj):
        return self.get_full_url(obj.daley_image)

    def get_full_url(self, image):
        if image:
            return self.context['request'].build_absolute_uri(image.url)
        return None
    

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = properties
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        property_instance = properties.objects.create(user=user, **validated_data)
        return property_instance
     
    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        for attr, value in validated_data.items():
                setattr(instance, attr, value)
        instance.save()
        return instance
    # def save(self, **kwargs):
    #         # Override the save method to handle file uploads
    #         property_instance = super().save(**kwargs)
            
    #         # Handle file uploads if provided
    #         propertyImage1 = self.validated_data.get('propertyImage1')
    #         propertyImage2 = self.validated_data.get('propertyImage2')
    #         propertyImage3 = self.validated_data.get('propertyImage3')
    #         daleyImage = self.validated_data.get('daleyImage')
            
    #         if propertyImage1:
    #             property_instance.propertyImage1 = propertyImage1
    #         if propertyImage2:
    #             property_instance.propertyImage2 = propertyImage2
    #         if propertyImage3:
    #             property_instance.propertyImage3 = propertyImage3
    #         if daleyImage:
    #             property_instance.daleyImage = daleyImage
            
    #         property_instance.save()
    #         return property_instance
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email','password']

   
  
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # def validate(self,attrs):
    #     print(attrs)
    #     return ("token pair is running ")
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        token['email'] = user.email
        token['password'] = user.password

        return token
    