from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('AllData/', Property_list.as_view()),
    path('AllData/<int:id>/', PropertyDetail.as_view()),
    path('home/',home ,  ),
    path('Users/', User_Create_API.as_view()),
    path('login/', User_Login_API.as_view()),
    path('Loginview/', Loginview.as_view()),
    path('property/', Prop_create.as_view()),
    path('User_based_data/', User_based_data),
    path('property/<int:pk>/', Prop_create.as_view()),
    path('property/<int:pk>/delete', Prop_create.as_view()),
]
