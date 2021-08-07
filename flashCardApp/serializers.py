from rest_framework import serializers
from .models import Case,CaseRes,System,Action,Finding
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


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('name','id')
        
class CaseToSystemSerializer(serializers.ModelSerializer):
    system = SystemSerializer()
    class Meta:
        model = Case
        fields = "__all__"

class CaseNormSerializer(serializers.ModelSerializer):
    #System = SystemSerializer()
    class Meta:
        model = Case
        fields = "__all__"

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('name','finding_set',"loc")
        depth = 1      

class FindingSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    class Meta:
        model = Finding
        fields = "__all__"
class FindingSerializer1(serializers.ModelSerializer):
    #action = ActionSerializer()
    class Meta:
        model = Finding
        fields = "__all__"
        depth = 2   
class CaseResSerializer1(serializers.ModelSerializer):
    
    finding = FindingSerializer()
    class Meta:
        model = CaseRes
        exclude = ['case']
        depth = 3    

class CaseToCaseResSerializer(serializers.ModelSerializer):
    caseres_set = CaseResSerializer1(many=True)
    class Meta:
        model=Case
        fields = ("caseres_set","name","gender","diagnosis","age","system",'id')