from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login

from rest_framework import viewsets,generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from .serializers import CaseSerializer,CaseResSerializer,ExamTypeSerializer,CaseNormSerializer,CaseToCaseResSerializer,UserSerializer, RegisterSerializer
from .models import Case,CaseRes,ExamType,MedTest
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
    # Send the Test!! log message to standard out
    logger.error("This backend does not have proper views, only API endpoints")
    return HttpResponse("This backend does not have proper views, only API endpoints")

#end of logging stuff

@api_view(['GET'])
def CaseViewRandom(request):
    r = random.randrange(Case.objects.all().count())
    case = Case.objects.all()[r]
    serializer = CaseSerializer(case, many=False)
    return Response(serializer.data)

# class CaseViewRandom(viewsets.ModelViewSet):
#     serializer_class = CaseSerializer
#     def get_queryset(self):
#         r = random.randrange(Case.objects.all().count())
#         return [Case.objects.all()[r]]
    
class ExamTypeView(viewsets.ModelViewSet):
    serializer_class = ExamTypeSerializer
    queryset = ExamType.objects.all()


@api_view(['GET'])

def caseDetail(request, pk):
	case = Case.objects.get(id=pk)
	serializer = CaseSerializer(case, many=False)
	return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def caseCreate(request):
	serializer = CaseNormSerializer(data=request.data)
	if serializer.is_valid():
         newCase = serializer.save()
         #link each new case to default result for all of its tests
         defaultRes = list(map(lambda x: x.result_set.filter(default =True),newCase.examtype.medtests.all()))
         for r in defaultRes:
             CaseRes.objects.create(case = newCase,result = r[0], req = False)

	return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((IsAuthenticated,))
def caseList(request):
	case = Case.objects.all().order_by('-id')
	serializer = CaseNormSerializer(case, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def caseToCaseResDetail(request, pk):
	case = Case.objects.get(id=pk)
	serializer = CaseToCaseResSerializer(case, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def caseResUpdate(request, pk):
	caseres = CaseRes.objects.get(id=pk)
	serializer = CaseResSerializer(instance=caseres, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

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
