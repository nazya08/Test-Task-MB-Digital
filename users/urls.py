from django.urls import path

from users.views import users


urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg'),
    path('users/me/', users.MeView.as_view(), name='me'),
    path('users/change-passwd/', users.ChangePasswordView.as_view(), name='change_passwd'),
    path('users/search/', users.UserListSearchView.as_view(), name='users-search'),
    path('users/delete/<int:pk>/', users.UserDeleteView.as_view(), name='user-delete'),
]
