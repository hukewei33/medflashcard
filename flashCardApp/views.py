from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login

from rest_framework import viewsets,generics, permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from .serializers import CaseSerializer,CaseResSerializer,SystemSerializer,CaseToSystemSerializer,CaseNormSerializer,CaseToCaseResSerializer,UserSerializer, RegisterSerializer,FindingSerializer1
from .models import Case,CaseRes,System,Action,Finding
import random
# Create your views here.
#logging stuff
import logging

from django.http import HttpResponse

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("This backend does not have proper views, only API endpoints")

#end of logging stuff

#to list all the cases with their System
@api_view(['GET'])
#@permission_classes((IsAuthenticated,))
def caseList(request):
	case = Case.objects.all().order_by('-id')
	serializer = CaseToSystemSerializer(case, many=True)
	return Response(serializer.data)

#for testing
#get random case    
@api_view(['GET'])
def CaseTestRandom(request):
    r = random.randrange(Case.objects.all().count())
    case = Case.objects.all()[r]
    serializer = CaseSerializer(case, many=False)
    return Response(serializer.data)

#get specific case
@api_view(['GET'])
def caseTest(request, pk):
	case = Case.objects.get(id=pk)
	serializer = CaseSerializer(case, many=False)
	return Response(serializer.data)

# create a new case
# list all examtytpes   
class SystemView(generics.ListCreateAPIView):
    serializer_class = SystemSerializer
    queryset = System.objects.all()

#create a new case and create a relationship with default Finding of each related medtest
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def caseCreate(request):
    serializer = CaseNormSerializer(data=request.data)
    if serializer.is_valid():
        newCase = serializer.save()
        #link each new case to default Finding for all of its tests
        defaultRes = list(map(lambda x: x.finding_set.filter(default =True),newCase.system.actions.all()))
        #print(defaultRes)
        for r in defaultRes:
            #check to prevent out of bound index reference and make loop safe, but it should not happen
            if len(r) !=0: 
                #CaseRes.objects.create(case = newCase,finding = r[0], req = True)
                CaseRes.objects.create(case = newCase,finding = r[0])
    
    return Response(serializer.data)

#get all related caseres for each case
@api_view(['GET'])
def caseToCaseResDetail(request, pk):
	case = Case.objects.get(id=pk)
	serializer = CaseToCaseResSerializer(case, many=False)
	return Response(serializer.data)
#edit individual caseres
@api_view(['POST','PATCH'])
def caseResUpdate(request, pk):
	caseres = CaseRes.objects.get(id=pk)
	serializer = CaseResSerializer(instance=caseres, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

#view edit and delete cases

class CaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseNormSerializer

@api_view(['DELETE','GET'])
@permission_classes((IsAuthenticated,))
def caseDelete(request, pk):
	case = Case.objects.get(id=pk)
	case.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)

#index all default findings
class FindingsList(generics.ListCreateAPIView):
    queryset = Finding.objects.filter(default=True)
    serializer_class = FindingSerializer1

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
