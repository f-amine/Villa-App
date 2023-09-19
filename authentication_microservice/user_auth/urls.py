from django.urls import path
from .views import RegisterView,LoginView,LogoutView,UserView,GetUserByEmailView,GetUserByIdView
from . import views
urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register_user'),
    path('api/login/', LoginView.as_view(), name='login_user'),
    path('api/logout/', LogoutView.as_view(), name='logout_user'),
    path('api/user/', UserView.as_view(), name='get_user_data'),
    path('api/user_by_email/<str:email>',GetUserByEmailView.as_view(),name='get_user_by_email'),
    path('api/user_by_id/<str:id>', GetUserByIdView.as_view(), name='get_user_data'),
    path('api/update_user/<str:id>/', views.update_user_id, name='update_user_data'),
]