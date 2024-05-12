from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class Property_list(generics.ListAPIView):
    queryset=properties.objects.all()
    serializer_class= Alldata


class PropertyDetail(generics.RetrieveAPIView):
    queryset = properties.objects.all()
    serializer_class = Alldata
    lookup_field = 'id'  # Specify the field to use for the lookup (in this case, 'id')

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def home(request):
    permission_classes = [IsAuthenticated]
    # Retrieve the user based on the username
    # user = NewUser.objects.get(username="anuj")
    # user = NewUser.objects.all()
    # prop = Property.objects.filter(user=user)
    prop = properties.objects.all()
    serializer = AlldataSerializer(prop, many=True,context={'request': request})
    return Response({"value": serializer.data})




@api_view(['GET'])
def User_based_data(request):
        permission_classes = [IsAuthenticated]
        user = request.user
        print(user)
        prop = properties.objects.filter(user=user)
        serializer = AlldataSerializer(prop, many=True,context={'request': request})
        return Response ({'data':serializer.data, })
    
class User_Create_API(APIView):
    def get(self,request):
        user = NewUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response ({'data':serializer.data})
        
    def post(self, request):
        data = request.data
        Login_data = data.get('values')
        print(Login_data)
        if Login_data:
                name = Login_data.get('name')
                email = Login_data.get('email')
                password = Login_data.get('password')    
                newdata = {
                                'username': name,  # Assuming 'username' corresponds to 'name'
                                'email': email,
                                'password':password,
                            }
                serializer = UserSerializer(data=newdata)
                print(newdata)
        if serializer.is_valid():
            serializer.save()
            user= NewUser.objects.get(username=serializer.data['username'])
            token,_ = Token.objects.get_or_create(user=user)

            return Response({"status":200,'message':"User created successfully",'token':str(token) })
        return Response({'error': serializer.errors}, status=400)

# @method_decorator(csrf_exempt, name='dispatch')
class User_Login_API(APIView):
    def get(self,request):
        user = NewUser.objects.all()
        serializer = LoginSerializer(user, many=True)
        return Response ({'data':serializer.data})
    
    def post(self, request):
        data = request.data
        print(data)
        data = data.get('values')
        # print(data.get('email'))
        if data:
            email = data.get('email')
            password = data.get('password') 
            print(password)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                    login(request, user)
                    #   new_user = NewUser.objects.get(username=request.user)
                    #   prop = Property.objects.filter(user=new_user)
                    #   serializer = UserPropertySerializer(prop, many=True)
                    new_user = NewUser.objects.get(username=user.username)
                    prop = Property.objects.filter(user=new_user)
                    serializer = UserPropertySerializer(prop, many=True)
                    token,_ = Token.objects.get_or_create(user=new_user)
                    print(serializer.data)
                    return Response({'message': 'Login successful' ,"user":user.username, "data":serializer.data,'token':str(token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


##Creating manual JWT token to control what to send to the token
class Loginview(TokenObtainPairView):
        serializer_class=MyTokenObtainPairSerializer




#CRUDE for user added properties
class Prop_create(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self,request):
        prop = Property.objects.all()
        serializer = UserPropertySerializer(prop, many=True)
        return Response({"value": serializer.data})

    # def post(self, request):
    #     try:
    #         propertyImage1 = request.FILES.get('propertyImage1')
    #         propertyImage2 = request.FILES.get('propertyImage2')
    #         propertyImage3 = request.FILES.get('propertyImage3')
    #         propertyName = request.POST.get('propertyName')
    #         location = request.POST.get('location')
    #         propertyType = request.POST.get('propertyType')
    #         daleyName = request.POST.get('daleyName')
    #         daleyImage = request.FILES.get('daleyImage')
    #         daleyPhone = request.POST.get('daleyPhone')
    #         price = request.POST.get('price')
    #         bedroom =request.POST.get('Bedroom')
    #         BikeParking =request.POST.get('BikeParking')
    #         CarParking =request.POST.get('CarParking')
    #         AttachedBathroom =request.POST.get('AttachedBathroom')
    #         Kitchen =request.POST.get('Kitchen')
    #         user=request.user
            
    #         print(propertyImage1,propertyImage2, propertyImage3, propertyName,location, propertyType,daleyName,daleyImage,daleyPhone,price)
    #         add_data = properties(img1=propertyImage1,
    #                               img2=propertyImage2,
    #                               img3=propertyImage3,
    #                               name=propertyName,
    #                               type=propertyType,
    #                               location=location,
    #                               price=price,
    #                               daley_number=daleyPhone,
    #                               daley_name=daleyName,
    #                               daley_image=daleyImage,
    #                               Bedroom=bedroom,
    #                               BikeParking=BikeParking,
    #                               CarParking=CarParking,
    #                               AttachedBathroom=AttachedBathroom,
    #                               Kitchen=Kitchen,
    #                               user=user)
            
    #         if add_data:
    #             add_data.save()
    #             return Response({'message': 'Property created successfully'}, status=201)
    #         return Response({'message': 'Some data is missing'}, status=400)

    #     except:
    #         return Response({'error': 'Error in fetching data'}, status=401)

    def post(self, request):
            data = {
    "img1": request.FILES.get('propertyImage1'),
    "img2": request.FILES.get('propertyImage2'),
    "img3": request.FILES.get('propertyImage3'),
    "name": request.POST.get('propertyName'),
    "type": request.POST.get('propertyType'),
    "location": request.POST.get('location'),
    "price": request.POST.get('price'),
    "daley_number": request.POST.get('daleyPhone'),
    "daley_name": request.POST.get('daleyName'),
    "daley_image": request.FILES.get('daleyImage'),
    "Bedroom": request.POST.get('Bedroom'),
    "BikeParking": request.POST.get('BikeParking'),
    "CarParking": request.POST.get('CarParking'),
    "AttachedBathroom": request.POST.get('AttachedBathroom'),
    "Kitchen": request.POST.get('Kitchen')
}
            print(data)
            serializer = PropertySerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)         
    
    def put(self, request, pk):
        try:
            print(request.data)
            property_instance = properties.objects.get(id = pk)
            print(property_instance.id)
            data = {
    "img1": request.FILES.get('propertyImage1'),
    "img2": request.FILES.get('propertyImage2'),
    "img3": request.FILES.get('propertyImage3'),
    "name": request.POST.get('propertyName'),
    "type": request.POST.get('propertyType'),
    "location": request.POST.get('location'),
    "price": request.POST.get('price'),
    "daley_number": request.POST.get('daleyPhone'),
    "daley_name": request.POST.get('daleyName'),
    "daley_image": request.FILES.get('daleyImage'),
    "Bedroom": request.POST.get('Bedroom'),
    "BikeParking": request.POST.get('BikeParking'),
    "CarParking": request.POST.get('CarParking'),
    "AttachedBathroom": request.POST.get('AttachedBathroom'),
    "Kitchen": request.POST.get('Kitchen')
}
            serializer = PropertySerializer(instance=property_instance, data=data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Property updated successfully', "data":serializer.data}, status=200)
            return Response(serializer.errors, status=400)
        except properties.DoesNotExist:
            return Response({'error': 'Property does not exist'}, status=404)
      
    
    def delete(self, request, pk):
        try:
            property_instance = properties.objects.get(id=pk)
        except Property.DoesNotExist:
            return Response({'error': 'Property does not exist'}, status=status.HTTP_404_NOT_FOUND)

        property_instance.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'Property deleted successfully'})