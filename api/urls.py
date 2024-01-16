from django .urls import path,include
from .views import CustomLoginView,RegisterUserAPIView,ListUserView, UpdateUserView

urlpatterns =[
    path('api/login/',CustomLoginView.as_view(),name='custom-login'),
    path('register/',RegisterUserAPIView.as_view()),
    path('view/',ListUserView.as_view(),name = 'view'),
    path('update/<int:pk>/', UpdateUserView.as_view(),name = 'update'),
    path('api/reset_password/', include('django_rest_passwordreset.urls',namespace='reset_password')),

]
