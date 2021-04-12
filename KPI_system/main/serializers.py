from django.contrib.auth.models import User
from rest_framework import serializers, fields
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name', ]


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    dept = DepartmentSerializer()

    class Meta:
        model = Employees
        fields = ['user', 'name', 'dept', 'position', 'manager']


class IssuesSerializer(serializers.ModelSerializer):
    emp = EmployeeSerializer()

    class Meta:
        model = Issues
        fields = ['name', 'status', 'start_date', 'end_date', 'emp']