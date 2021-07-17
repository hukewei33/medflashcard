from rest_framework import serializers
from .models import Case,CaseRes,ExamType,MedTest,Result
from django.contrib.auth.models import User

#user account serializer
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

#model serializer
class CaseResSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseRes
        fields = "__all__"

class CaseResSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CaseRes
        exclude = ['case']
        depth = 3

class CaseSerializer(serializers.ModelSerializer):
    caseres_set = CaseResSerializer2(many=True)
    
    class Meta:
        model = Case
        fields = ('id','name','gender','age','caseres_set','diagnosis')
        depth = 3


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ('name','id')
        
class CaseToExamTypeSerializer(serializers.ModelSerializer):
    examtype = ExamTypeSerializer()
    class Meta:
        model = Case
        fields = "__all__"

class CaseNormSerializer(serializers.ModelSerializer):
    #examtype = ExamTypeSerializer()
    class Meta:
        model = Case
        fields = "__all__"

class MedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedTest
        fields = ('name','testcat','result_set')
        depth = 1      

class ResultSerializer(serializers.ModelSerializer):
    medTest = MedTestSerializer()
    class Meta:
        model = Result
        fields = "__all__"

class CaseResSerializer1(serializers.ModelSerializer):
    
    result = ResultSerializer()
    class Meta:
        model = CaseRes
        exclude = ['case']
        depth = 3    

class CaseToCaseResSerializer(serializers.ModelSerializer):
    caseres_set = CaseResSerializer1(many=True)
    class Meta:
        model=Case
        fields = ("caseres_set",)