from django.urls import path
from user_management.views import CreateUserAPIView, MyTokenObtainPairView

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
