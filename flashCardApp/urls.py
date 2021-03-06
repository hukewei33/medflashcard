
from django.urls import path,include
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()

# router.register(r'systems', views.SystemView)

urlpatterns = [
    path('', views.index, name='index'),

#    path('', include(router.urls)),
    
    path('systems/', views.SystemView.as_view(),name = "system-list"),
    
    path('case-list/', views.caseList, name="case-list"),
    path('caserand/', views.CaseTestRandom, name="case-rand"),
    path('case-detail/<str:pk>/', views.caseTest, name="case-detail"),
    path('caseupdate/<str:pk>/', views.CaseDetail.as_view(), name ="case-update"),
    path('casedel/<str:pk>/', views.caseDelete, name="case-delete"),
    
    path('findings/', views.FindingsList.as_view(),name = "def-finding-list"),

	path('case-create/', views.caseCreate, name="case-create"),
    path('case-res/<str:pk>/', views.caseToCaseResDetail, name="case-res"),
    path('case-res-update/<str:pk>/', views.caseResUpdate, name="case-res-update"),
    
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    ]
#urlpatterns = format_suffix_patterns(urlpatterns)