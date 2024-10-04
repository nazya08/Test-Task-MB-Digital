from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='User Registration', tags=['Authentication & Authorization']),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializer,
        summary='Password Change', tags=['Authentication & Authorization']),
)
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request):
        user = self.get_object()
        serializer = user_s.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='User Profile', tags=['Users']),
    put=extend_schema(summary='Change User Profile', tags=['Users']),
    patch=extend_schema(summary='Change User Profile Partially', tags=['Users']),
)
class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer
    http_method_names = ('get', 'patch')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.MeUpdateSerializer
        return user_s.MeSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    delete=extend_schema(summary='Delete User', tags=['Users']),
)
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_superuser:
            return Response({"error": "Cannot delete superuser."}, status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(summary='Users List Search', tags=['Users']),
)
class UserListSearchView(generics.ListAPIView):
    queryset = User.objects.exclude(
        Q(is_superuser=True)
    )
    serializer_class = user_s.UserSearchListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('last_name', 'email', 'username',)
