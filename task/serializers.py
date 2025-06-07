from rest_framework import serializers
from task.models import Task
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'  
        read_only_fields=['owner']  



class RegisterSerializer(serializers.ModelSerializer):
        username=serializers.CharField()
        email=serializers.CharField()
        password=serializers.CharField()
        class Meta:
            model=User
            fields=("username","email","password")
        def create(self,validated_data):
            user=User.objects.create_user(**validated_data)
            return()


class LoginSerializer(serializers.ModelSerializer):
        username=serializers.CharField()
        password=serializers.CharField(write_only=True)
        class Meta:
             model=User
             fields=("username","password")
        def create(self,validated_data):
             user=User.objects.create_user(**validated_data)
             return("login success")


