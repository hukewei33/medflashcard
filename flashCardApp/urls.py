
from django.urls import path
from knox import views as knox_views
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    
    path('case-list/', views.caseList, name="case-list"),
    path('caserand/', views.CaseViewRandom, name="case-rand"),
    path('case-detail/<str:pk>/', views.caseDetail, name="case-detail"),

	path('case-create/', views.caseCreate, name="case-create"),
    path('case-res/<str:pk>/', views.caseToCaseResDetail, name="case-res"),
    path('case-res-update/<str:pk>/', views.caseResUpdate, name="case-res-update"),
    
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    ]