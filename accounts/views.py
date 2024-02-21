# Create your views here.
from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.response import Response

from utils.views import GetBaseModelViewSet
# from utils.views import SilkyModelViewSet
from .models import User
from .permissions import UserViewPermission
from .serializers import UserSerializer

BaseModelViewSet_user = GetBaseModelViewSet("user")


class UserViews(BaseModelViewSet_user):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser | UserViewPermission]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(Q(email__exact=request.data['email']) | Q(
                username__exact=request.data['username']))
            if user:
                return Response({
                    "detail": "Username or email already exists."
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            new = User.objects.create_user(**request.data)
            serialized_data = UserSerializer(new).data

            return Response(serialized_data, status=status.HTTP_201_CREATED)
