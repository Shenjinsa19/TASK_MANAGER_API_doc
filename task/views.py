from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import (RegisterSerializer,LoginSerializer,TaskSerializer)
from django.contrib.auth import authenticate,login
from rest_framework import generics, permissions,status
from .models import Task
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password
            )   
            token=Token.objects.create(user=user)
            return Response({'token':token.key},status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']
            user=authenticate(username=username, password=password)
            if user:
                token,created=Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error':'invalid credentials'},status=400)
        return Response(serializer.errors,status=400)
    



# class LogoutView(APIView):
#     authentication_classes = []  
#     permission_classes = []
#     def post(self, request):
#         token_key = request.data.get('token')
#         if not token_key:
#             return Response({"error": "token required "}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             token = Token.objects.get(key=token_key)
#             token.delete()
#             return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]  # use session, no token needed here
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.user.auth_token
            token.delete()
        except:
            pass
        from django.contrib.auth import logout
        logout(request)
        return Response({"message": "Logged out successfully."})




               #just view   
# class TaskListCreateView(generics.ListCreateAPIView):
#     serializer_class = TaskSerializer
#     permission_classes=[permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Task.objects.all()
#         return Task.objects.filter(owner=user)

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
    



class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TaskSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(owner=user)



               #cache
from django.core.cache import cache
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class=TaskSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        cache_key=f'task_list_user_{user.id}'
        task_list=cache.get(cache_key)
        if task_list is not None:
            print("fetching from cache")
        else:
            print("fetching from db")
            if user.is_staff:
                task_list=Task.objects.all()
            else:
                task_list=Task.objects.filter(owner=user)
            cache.set(cache_key, task_list, timeout=60) 
        return task_list
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.delete(f'task_list_user_{self.request.user.id}')
        print(" Cache cleared after task creation")

