# views.py
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.serializers import ValidationError
from .serializers import RegisterSerializer,UserSerializer, ChangePasswordSerializer

class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def get_queryset(self):
        queryset= User.objects.all()
        return queryset
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = RegisterSerializer.create(self,validated_data=serializer.validated_data)
            token = AuthToken.objects.create(user)[1]
            serialized_user = UserSerializer(user, context=self.get_serializer_context()).data

            return Response({
                'user': serialized_user,
                'token': token
            })
        else:
            return Response(serializer.errors)

#class UserLoginView(KnoxLoginView):
 #   permission_classes = [ AllowAny]
  #  def post(self,request,format=None):
   #     serializer = AuthTokenSerializer(data=request.data)
    #    if serializer.is_valid():
     #       user = serializer.validated_data['user']
      #      login(request,user)
       #     return super(UserLoginView,self).post(request,format=None)
      #  else:
       #     raise ValidationError

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomAuthTokenSerializer
from rest_framework.authtoken.models import Token

class CustomLoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})



class ListUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUserView(generics.UpdateAPIView):
  
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes =[IsAuthenticated,]

    def get_object(self,queryset = None):
        obj = self.request.user
        return obj
    def update(self,request,**args):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':{'Wrong Password!'}},status= status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({
               'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password Updated Successfully!',
                'data' :[]
            })
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

